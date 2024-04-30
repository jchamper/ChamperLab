library(tidyverse)
library(openxlsx)
library(RColorBrewer)

setwd("/Users/weizhechen/Documents/Champerlab/DSX_RIDD/Modeling5/rerun0423")

#读取所有simulation csv并整合成规定格式(100组)
data=data.frame()
frfe_pop=list()
drive_rate=list()
for (i in c(0:19)){ #99
  k=paste("/Users/weizhechen/Documents/Champerlab/DSX_RIDD/Modeling5/rerun0423/RIDD",i,".csv",sep="")
  icsv=data.frame(read_csv(k))
  icsv=icsv[11:nrow(icsv),]
  icsv[,1]=icsv[,1]-10
  icsv$num=c(rep(i+1,each=nrow(icsv))) #RIDD0.csv has mark as 1
  data=rbind(data,icsv) 
  frfe_pop[[i+1]]=icsv$female/icsv$pop_size
  drive_rate[[i+1]]=icsv$drive_carrier
  }

#读取实验 csv并整合成规定格式(2组)
exp_frfe_pop=list()
exp_drive_rate=list()
for (i in c(21,22)){ #101 102
  if (i==21)
    k=paste("/Users/weizhechen/Documents/Champerlab/DSX_RIDD/Modeling5/rerun0423/RIDDA.csv",sep="")
  if (i==22)
    k=paste("/Users/weizhechen/Documents/Champerlab/DSX_RIDD/Modeling5/rerun0423/RIDDB.csv",sep="")
  ex_csv=data.frame(read_csv(k))
  ex_csv$num=c(rep(i,each=nrow(ex_csv)))
  data=rbind(data,ex_csv)
  exp_frfe_pop[[i-20]]=ex_csv$female/ex_csv$pop_size
  exp_drive_rate[[i-20]]=ex_csv$drive_carrier
}

data$female_ratio=data$female/data$population
data$sem_drive=rep(0,nrow(data))
data$sem_female=rep(0,nrow(data))
names(data)[1] <- "week"
write_csv(data,"cage0424.csv")

data=read.csv("cage0424sem.csv")



#fly_has_drive图
data1=data.frame(x = data[,1], y = data[,6], group = data[,8])
pdf(file = "sumulation-drive.pdf", width = 12, height =5.5)
ggplot(data1,aes(x = x, y = y, color = factor(group))) +
  geom_line(size=1)+
  labs(x = "Weeks", y = "Drive", color = "cage") +
  geom_errorbar(aes(ymin=data[,6]-data[,9],ymax=data[,6]+data[,9]),lwd=0.7,width=0.4,color=c("#969696"),cex=1)+
  scale_x_continuous(breaks=seq(0, 38, by = 2))+
  theme_classic(base_size = 20)+
  theme(legend.position = "right")+
  scale_color_manual(values = c(rep(c("#F1E2CC"),each=20),"#1D91C0","#E31A1C"))+ #100
  scale_size_manual(values = c(rep(0.5,each=10),4,4,4))
dev.off()

#population图
data2=data.frame(x = data[,1], y = data[,7], group = data[,8])
#meanfemale1=data.frame(x = 0:(nrow(Meanfemale)-1), y = Meanfemale[,1], group=rep(33, nrow(Meanfemale))) #103
#dataplot2=rbind(data2,meanfemale1)
pdf(file = "sumulation-pop.pdf", width = 10, height = 5.5)
ggplot(data2, aes(x = x, y = y, color = factor(group))) +
  geom_line(linewidth=1)+
  #geom_point(shape = 16,size=1) +
  labs(x = "Weeks", y = "Female population", color = "cage") +
  geom_errorbar(aes(ymin=data[,7]-data[,10],ymax=data[,7]+data[,10]),lwd=0.7,width=0.4,color=c("#969696"),cex=1)+
  xlim(0,38)+ylim(0, 1600)+
  scale_x_continuous(breaks=seq(0, 38, by = 2))+
  scale_y_continuous(breaks=seq(0, 1200, by = 200))+
  theme_classic(base_size = 20)+
  theme(legend.position = "none")+
  scale_color_manual(values = c(rep(c("#F1E2CC"),each=20),"#1D91C0","#E31A1C")) #100
dev.off()

"#FFFFFF" "#F0F0F0" "#D9D9D9" "#BDBDBD" "#969696" "#737373" "#525252" "#252525" "#000000"
"#B3E2CD" "#FDCDAC" "#CBD5E8" "#F4CAE4" "#E6F5C9" "#FFF2AE" "#F1E2CC" "#CCCCCC"
"#FBB4AE" "#B3CDE3" "#CCEBC5" "#DECBE4" "#FED9A6" "#FFFFCC" "#E5D8BD" "#FDDAEC" "#F2F2F2"
"#A6CEE3" "#1F78B4" "#B2DF8A" "#33A02C" "#FB9A99" "#E31A1C" "#FDBF6F" "#FF7F00" "#CAB2D6"
"#FCFBFD" "#EFEDF5" "#DADAEB" "#BCBDDC" "#9E9AC8" "#807DBA" "#6A51A3" "#54278F" "#3F007D"
"#F7FCF5" "#E5F5E0" "#C7E9C0" "#A1D99B" "#74C476" "#41AB5D" "#238B45" "#006D2C" "#00441B"
"#FFFFCC" "#FFEDA0" "#FED976" "#FEB24C" "#FD8D3C" "#FC4E2A" "#E31A1C" "#BD0026" "#800026"
"#A6CEE3" "#1F78B4" "#B2DF8A" "#33A02C" "#FB9A99" "#E31A1C" "#FDBF6F" "#FF7F00" "#CAB2D6" "#6A3D9A" "#FFFF99"
