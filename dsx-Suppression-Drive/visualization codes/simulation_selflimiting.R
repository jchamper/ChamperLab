library(tidyverse)
library(openxlsx)


setwd("/Users/weizhechen/Documents/Champerlab/DSX_RIDD/Modeling5/rerun0415_selflimit")

#读取所有simulation csv并整合成规定格式(100组)
data=data.frame()
fe_pop=list()
drive_rate=list()
for (i in c(0:19)){ #99
  k=paste("/Users/weizhechen/Documents/Champerlab/DSX_RIDD/Modeling5/rerun0415_selflimit/RIDD",i,".csv",sep="")
  icsv=data.frame(read_csv(k))
  icsv=icsv[1:nrow(icsv),]
  icsv[,1]=icsv[,1]
  icsv$num=c(rep(i+1,each=nrow(icsv))) #RIDD0.csv has mark as 1
  data=rbind(data,icsv) 
  fe_pop[[i+1]]=icsv$female
  drive_rate[[i+1]]=icsv$drive_carrier
  }



#fly_has_drive图
data1=data.frame(x = data[,1], y = data[,2], group = data[,7])
pdf(file = "sumulation-drive.pdf", width = 11, height =4.5)
ggplot(data1,aes(x = x, y = y, color = factor(group))) +
  #geom_line(meandata,aes(x = x, y = y, color = "pink"))+
  geom_line(size=1)+
  #geom_point(shape = 16,size=1) +
  labs(x = "Weeks", y = "Drive", color = "cage") +
  ylim(0, 1)+
  scale_x_continuous(limits = c(0, 90), breaks = seq(0, 90, by = 5))+
  theme_classic(base_size = 18)+
  theme(axis.text = element_text(size = 20))+
  theme(legend.position = "none")+
  scale_color_manual(values = c(rep(c("#BCBDDC"),each=20),"#1D91C0","#E31A1C","#737373"))+ #100
  scale_size_manual(values = c(rep(0.5,each=10),4,4,4))
dev.off()


#fertile female population图
data2=data.frame(x = data[,1], y = data[,4], group = data[,7])
pdf(file = "sumulation-pop.pdf", width = 11, height = 4.5)
ggplot(data2, aes(x = x, y = y, color = factor(group))) +
  geom_line(linewidth=1)+
  #geom_point(shape = 16,size=1) +
  labs(x = "Weeks", y = "Female population", color = "cage") +
  #xlim(0,80)+
  ylim(0, 1200)+
  scale_x_continuous(limits = c(0, 90), breaks = seq(0, 90, by = 5))+
  theme_classic(base_size = 18)+
  theme(axis.text = element_text(size = 20))+
  theme(legend.position = "none")+
  scale_color_manual(values = c(rep(c("#BCBDDC"),each=20),"#1D91C0","#E31A1C","black")) #100
dev.off()

