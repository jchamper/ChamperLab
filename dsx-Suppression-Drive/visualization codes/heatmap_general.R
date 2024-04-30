library(ggplot2)
library(dplyr)
library(RColorBrewer)

setwd("/Users/weizhechen/Documents/Champerlab/DSX_RIDD/Modeling6/FINAL\ data2")

mycolorsA=c("#08306B","#08519C","#4292C6","#9ECAE1","white")
mycolorsB=c("white", "#FDD49E", "#EF6548", "#D7301F")
mycolorsE=c("white", "#FDD49E", "#EF6548", "#D7301F", "#A50F15","#7F0000","#67000D")
mycolorsD=c("white", "#C7E9C0", "#41AB5D", "#006D2C")
mycolorsC=c("white","#9ECAE1","#4292C6","#08519C","#08306B")
"#D53E4F" "#F46D43" "#FDAE61" "#FEE08B" "#FFFFBF" "#E6F598" "#ABDDA4" "#66C2A5" "#3288BD"
"#B2182B" "#D6604D" "#F4A582" "#FDDBC7" "#FFFFFF" "#E0E0E0" "#BABABA" "#878787" "#4D4D4D"
"#FFF7EC" "#FEE8C8" "#FDD49E" "#FDBB84" "#FC8D59" "#EF6548" "#D7301F" "#B30000" "#7F0000"
"#FFF5F0" "#FEE0D2" "#FCBBA1" "#FC9272" "#FB6A4A" "#EF3B2C" "#CB181D" "#A50F15" "#67000D"
"#FCFBFD" "#EFEDF5" "#DADAEB" "#BCBDDC" "#9E9AC8" "#807DBA" "#6A51A3" "#54278F" "#3F007D"

####RIDL
fRIDL <- data.frame(read.csv("fsRIDL0403.csv"))
# 对20次重复求平均
fRIDLaverages1 <- fRIDL %>%
  group_by(group = gl(n()/20, 20)) %>%
  summarise(across(everything(), mean)) %>%
  select(-group)
fRIDLaverages1=data.frame(fRIDLaverages1)

# 对20次重复求平均，若有0值(suppress)，则剔除后求平均（针对人口数的计算）
fRIDLaverages2 <- fRIDL %>%
  group_by(group = rep(1:41, each = 20)) %>%  # 每组20行，共10组
  summarise(across(everything(), function(x) mean(x[x != 0]))) %>%
  select(-group)  # 移除用于分组的列
fRIDLaverages2=cbind(fRIDLaverages2[,1:8],fRIDLaverages1[,9:10])

# 对20次重复求平均，若有100000值(suppress)，则剔除后求平均（针对gen_suppressed数据收集）
fRIDLaverages3 <- fRIDL %>%
  group_by(group = rep(1:41, each = 20)) %>%  # 每组20行，共10组
  summarise(across(everything(), function(x) mean(x[x != 10000]))) %>%
  select(-group)  # 移除用于分组的列
fRIDLaverages3=data.frame(fRIDLaverages3)

# 1. 热图 successful suppressed rate； 用averages1
fRIDL1=ggplot(data = fRIDLaverages1, aes(x = NA, y = release)) +
  geom_tile(aes(fill = suppressed), color =NA) +
  scale_fill_gradientn(colours=mycolorsD,limits = c(0,1), name=" ")+theme_classic()+ 
  scale_y_continuous(limits = c(-0.1, 4.1), breaks = seq(0, 4, by = 0.25))+
  theme(aspect.ratio = 3, plot.margin = margin(0.2, 0.2, 0.2, 0.2, unit = "cm"),
        legend.position = "none",  # 隐藏图例  
        axis.title.x = element_blank(),   # 去掉X轴坐标标题
        axis.title.y = element_blank(),
        axis.text.x = element_blank())+
  coord_fixed(ratio = 3)   # 设置纵横比为1

# 2. 热图 suppressed_gen；用averages3
fRIDL2=ggplot(data = fRIDLaverages3, aes(x = NA, y = release)) +
  geom_tile(aes(fill = gen_suppressed), color = NA) +
  scale_fill_gradientn(colours=mycolorsC,limits = c(20, 267), name=" ")+theme_classic() +
  scale_y_continuous(limits = c(-0.1, 4.1), breaks = seq(0, 4, by = 0.5))+
  theme(aspect.ratio = 3, plot.margin = margin(0.2, 0.2, 0.2, 0.2, unit = "cm"),  
        legend.position = "none",  # 隐藏图例
        axis.title.x = element_blank(),   # 去掉X轴坐标标题
        axis.title.y = element_blank(),
        axis.text = element_text(size = 16),
        axis.line = element_line(linewidth  = 0.9),
        axis.text.x = element_blank())
  
# 3. 热图 equilibrium size；用averages2
#fertile female
fRIDL3=ggplot(data = fRIDLaverages2, aes(x = NA, y = release)) +
  geom_tile(aes(fill = fertile_fe), color =NA) +
  scale_fill_gradientn(colours=mycolorsB,limits = c(1, 51000), name=" ")+theme_classic()+
  scale_y_continuous(limits = c(-0.1, 4.1), breaks = seq(0, 4, by = 0.5))+
  theme(aspect.ratio = 3, plot.margin = margin(0.2, 0.2, 0.2, 0.2, unit = "cm"),  
        legend.position = "none",  # 隐藏图例
        axis.title.x = element_blank(),   # 去掉X轴坐标标题
        axis.title.y = element_blank(),
        axis.text = element_text(size = 16),
        axis.line = element_line(linewidth  = 0.9),
        axis.text.x = element_blank())

#female
fRIDL4=ggplot(data = fRIDLaverages2, aes(x = NA, y = release)) +
  geom_tile(aes(fill = adult_fe), color =NA) +
  scale_fill_gradientn(colours=mycolorsB,limits = c(1, 100000), name=" ")+theme_classic()+
  scale_y_continuous(limits = c(-0.1, 4.1), breaks = seq(0, 4, by = 0.5))+
  theme(aspect.ratio = 3, plot.margin = margin(0.2, 0.2, 0.2, 0.2, unit = "cm"),  
        legend.position = "none",  # 隐藏图例
        axis.title.x = element_blank(),   # 去掉X轴坐标标题
        axis.title.y = element_blank(),
        axis.text.x = element_blank())

#adults
fRIDL5=ggplot(data = fRIDLaverages2, aes(x = NA, y = release)) +
  geom_tile(aes(fill = adult), color =NA) +
  scale_fill_gradientn(colours=mycolorsB,limits = c(1, 300000), name=" ")+theme_classic()+
  scale_y_continuous(limits = c(-0.1, 4.1), breaks = seq(0, 4, by = 0.5))+
  theme(aspect.ratio = 3, plot.margin = margin(0.2, 0.2, 0.2, 0.2, unit = "cm"),  
        legend.position = "none",
        axis.text.x = element_blank())





####SIT
SIT <- data.frame(read.csv("SIT0403.csv"))
# 对20次重复求平均
SITaverages1 <- SIT %>%
  group_by(group = gl(n()/20, 20)) %>%
  summarise(across(everything(), mean)) %>%
  select(-group)
SITaverages1=data.frame(SITaverages1)

# 对20次重复求平均，若有0值(suppress)，则剔除后求平均（针对人口数的计算）
SITaverages2 <- SIT %>%
  group_by(group = rep(1:41, each = 20)) %>%  
  summarise(across(everything(), function(x) mean(x[x != 0]))) %>%
  select(-group)  # 移除用于分组的列
SITaverages2=cbind(SITaverages2[,1:8],SITaverages1[,9:10])

# 对20次重复求平均，若有0值(suppress)，则剔除后求平均（针对代数的计算）
SITaverages3 <- SIT %>%
  group_by(group = rep(1:41, each = 20)) %>%  
  summarise(across(everything(), function(x) mean(x[x != 10000]))) %>%
  select(-group)  # 移除用于分组的列
SITaverages3=data.frame(SITaverages3)

# 2. 热图 successful suppressed rate； 用averages1
SIT1=ggplot(data = SITaverages1, aes(x = NA, y = release)) +
  geom_tile(aes(fill = suppressed), color =NA) +
  scale_fill_gradientn(colours=mycolorsD,limits = c(0,1),name=" ")+theme_classic()+
  scale_y_continuous(limits = c(-0.1, 8.1), breaks = seq(0, 8, by = 0.5))+
  ylab("Release ratio")+
  theme(aspect.ratio = 3, plot.margin = margin(0.2, 0.2, 0.2, 0.2, unit = "cm"), 
        legend.position = "none",
        axis.title.x = element_blank(),   # 去掉X轴坐标标题
        axis.title.y = element_blank(),
        axis.text.x = element_blank())
  

# 3. 热图 suppressed_gen；用averages3
SIT2=ggplot(data = SITaverages3, aes(x = NA, y = release)) +
  geom_tile(aes(fill = gen_suppressed), color = NA) +
  scale_fill_gradientn(colours=mycolorsC,limits = c(20, 267),name=" ")+theme_classic() +
  scale_y_continuous(limits = c(-0.1, 8.1), breaks = seq(0, 8, by = 1),
                     labels = function(x) sprintf("%.1f", x))+
  theme(aspect.ratio = 3, plot.margin = margin(0.2, 0.2, 0.2, 0.2, unit = "cm"), 
        legend.position = "none",
        axis.title.x = element_blank(),   # 去掉X轴坐标标题
        axis.title.y = element_blank(),
        axis.text = element_text(size = 16),
        axis.line = element_line(linewidth  = 0.9),
        axis.text.x = element_blank())

# 4. 热图 equilibrium size；用averages2
#fertile female
SIT3=ggplot(data = SITaverages2, aes(x = NA, y = release)) +
  geom_tile(aes(fill = fertile_fe), color =NA) +
  scale_fill_gradientn(colours=mycolorsE,limits = c(1, 102000),name=" ")+theme_classic()+
  scale_y_continuous(limits = c(-0.1, 8.1), breaks = seq(0, 8, by = 1),
                     labels = function(x) sprintf("%.1f", x))+
  theme(aspect.ratio = 3, plot.margin = margin(0.2, 0.2, 0.2, 0.2, unit = "cm"),  
        legend.position = "none",  # 隐藏图例
        axis.title.x = element_blank(),   # 去掉X轴坐标标题
        axis.title.y = element_blank(),
        axis.text = element_text(size = 16),
        axis.line = element_line(linewidth  = 0.9),
        axis.text.x = element_blank())

#female
SIT4=ggplot(data = SITaverages2, aes(x = NA, y = release)) +
  geom_tile(aes(fill = adult_fe), color =NA) +
  scale_fill_gradientn(colours=mycolorsE,limits = c(1, 100000),name=" ")+theme_classic()+
  scale_y_continuous(limits = c(-0.1, 8.1), breaks = seq(0, 8, by = 0.5))+
  theme(aspect.ratio = 3, plot.margin = margin(0.2, 0.2, 0.2, 0.2, unit = "cm"),  
        legend.position = "none",  # 隐藏图例
        axis.title.x = element_blank(),   # 去掉X轴坐标标题
        axis.title.y = element_blank(),
        axis.text.x = element_blank())

#adults
SIT5=ggplot(data = SITaverages2, aes(x = NA, y = release)) +
  geom_tile(aes(fill = adult), color =NA) +
  scale_fill_gradientn(colours=mycolorsE,limits = c(1, 600000),name=" ")+theme_classic()+
  scale_y_continuous(limits = c(-0.1, 8.1), breaks = round(seq(0, 8, by = 1), 1))+
  theme(aspect.ratio = 3, plot.margin = margin(0.2, 0.2, 0.2, 0.2, unit = "cm"),  
        legend.position = "none",  # 隐藏图例
        axis.title.x = element_blank(),  
        axis.title.y = element_blank(),
        axis.text.x = element_blank())




##RIDDsplit
datasplit <- data.frame(read.csv("RIDDsplit0410.csv"))
# 对20次重复求平均
RIDDsplit_averages1 <- datasplit %>%
  group_by(group = gl(n()/20, 20)) %>%
  summarise(across(everything(), mean)) %>%
  select(-group)
RIDDsplit_averages1=data.frame(RIDDsplit_averages1)

# 对20次重复求平均，若有0值(suppress)，则剔除后求平均（针对人口数的计算）
RIDDsplit_averages2 <- datasplit %>%
  group_by(group = rep(1:(nrow(datasplit)/20), each = 20)) %>%  # 每组20行，共10组
  summarise(across(everything(), function(x) mean(x[x != 0]))) %>%
  select(-group)  # 移除用于分组的列
RIDDsplit_averages2=cbind(RIDDsplit_averages2[,1:8],RIDDsplit_averages1[,9:10])

# 对20次重复求平均，若有0值(suppress)，则剔除后求平均（针对weeks的计算）
RIDDsplit_averages3 <- datasplit %>%
  group_by(group = rep(1:(nrow(datasplit)/20), each = 20)) %>%  # 每组20行，共10组
  summarise(across(everything(), function(x) mean(x[x != 10000]))) %>%
  select(-group)  # 移除用于分组的列
RIDDsplit_averages3=data.frame(RIDDsplit_averages3)

# 1. 热图 successful suppressed rate； 用averages1
split1=ggplot(data = RIDDsplit_averages1, aes(x = drive_conversion, y = release)) +
  geom_tile(aes(fill = suppressed), color =NA) +
  scale_fill_gradientn(colours=mycolorsD,limits = c(0,1),name=" ")+theme_classic()+ 
  scale_y_continuous(limits = c(-0.1, 2.1), breaks = seq(0, 2, by = 0.2))+
  scale_x_continuous(limits = c(-0.05, 1.05), breaks = seq(0, 1, by = 0.1))+  
  theme(aspect.ratio = 1, plot.margin = margin(0.2, 0.2, 0.2, 0.2, unit = "cm"),
        legend.position = "none",  # 隐藏图例
        axis.title.x = element_blank(),   # 去掉X轴坐标标题
        axis.title.y = element_blank(),
        axis.text.x = element_text(angle = 45, hjust = 1))+
  coord_fixed(ratio = 1)   # 设置纵横比为1

# 2. 热图 suppressed_gen；用averages3
split2=ggplot(data = RIDDsplit_averages3, aes(x = drive_conversion, y = release)) +
  geom_tile(aes(fill = gen_suppressed), color = NA) +
  scale_fill_gradientn(colours=mycolorsC,limits = c(20, 267),name=" ")+theme_classic() +
  scale_y_continuous(limits = c(-0.1, 2.1), breaks = seq(0, 2, by = 0.2))+
  scale_x_continuous(limits = c(-0.05, 1.05), breaks = seq(0, 1, by = 0.1))+  
  theme(aspect.ratio = 1, plot.margin = margin(0.2, 0.2, 0.2, 0.2, unit = "cm"),
        legend.position = "none",  # 隐藏图例
        axis.title.x = element_blank(),   # 去掉X轴坐标标题
        axis.title.y = element_blank(),
        axis.text = element_text(size = 14),
        axis.line = element_line(linewidth  = 0.7),
        axis.text.x = element_text(angle = 45, hjust = 1))

# 3. 热图 equilibrium size；用averages2
#fertile female
split3=ggplot(data = RIDDsplit_averages2, aes(x = drive_conversion, y = release)) +
  geom_tile(aes(fill = fertile_fe), color =NA) +
  scale_fill_gradientn(colours=mycolorsB,limits = c(0, 51000),name=" ")+theme_classic()+
  scale_y_continuous(limits = c(-0.1, 2.1), breaks = seq(0, 2, by = 0.2))+
  scale_x_continuous(limits = c(-0.05, 1.05), breaks = seq(0, 1, by = 0.1))+  
  theme(aspect.ratio = 1, plot.margin = margin(0.2, 0.2, 0.2, 0.2, unit = "cm"),
        legend.position = "none",  # 隐藏图例
        axis.title.x = element_blank(),   # 去掉X轴坐标标题
        axis.title.y = element_blank(),
        axis.text = element_text(size = 14),
        axis.line = element_line(linewidth  = 0.7),
        axis.text.x = element_text(angle = 45, hjust = 1))

#female
split4=ggplot(data = RIDDsplit_averages2, aes(x = drive_conversion, y = release)) +
  geom_tile(aes(fill = adult_fe), color =NA) +
  scale_fill_gradientn(colours=mycolorsB,limits = c(1, 100000),name=" ")+theme_classic()+
  scale_y_continuous(limits = c(-0.1, 2.1), breaks = seq(0, 2, by = 0.2))+
  scale_x_continuous(limits = c(-0.05, 1.05), breaks = seq(0, 1, by = 0.1))+  
  theme(aspect.ratio = 1, plot.margin = margin(0.2, 0.2, 0.2, 0.2, unit = "cm"),
        legend.position = "none",  # 隐藏图例
        axis.title.x = element_blank(),   # 去掉X轴坐标标题
        axis.title.y = element_blank(),
        axis.text.x = element_text(angle = 45, hjust = 1))
#adults
split5=ggplot(data = RIDDsplit_averages2, aes(x = drive_conversion, y = release)) +
  geom_tile(aes(fill = adult), color =NA) +
  scale_fill_gradientn(colours=mycolorsB,limits = c(1, 300000),name=" ")+theme_classic()+
  scale_y_continuous(limits = c(-0.1, 2.1), breaks = seq(0, 2, by = 0.2))+
  scale_x_continuous(limits = c(-0.05, 1.05), breaks = seq(0, 1, by = 0.1))+  
  theme(aspect.ratio = 1, plot.margin = margin(0.2, 0.2, 0.2, 0.2, unit = "cm"),
        legend.position = "none",  # 隐藏图例
        axis.title.x = element_blank(),   # 去掉X轴坐标标题
        axis.title.y = element_blank(),
        axis.text.x = element_text(angle = 45, hjust = 1))



##RIDDfull
datafull <- data.frame(read.csv("RIDDfull0409.csv"))
# 对20次求平均
RIDDfull_averages1 <- datafull %>%
  group_by(group = gl(n()/20, 20)) %>%
  summarise(across(everything(), mean)) %>%
  select(-group)
RIDDfull_averages1=data.frame(RIDDfull_averages1)

# 对20次求平均，若有0值，则剔除后求平均（针对人口数的计算）
RIDDfull_averages2 <- datafull %>%
  group_by(group = rep(1:(nrow(datafull)/20), each = 20)) %>%  # 每组20行，共10组
  summarise(across(everything(), function(x) mean(x[x != 0]))) %>%
  select(-group)  
RIDDfull_averages2=cbind(RIDDfull_averages2[,1:8],RIDDfull_averages1[,9:10])

# 对20次求平均，若有10000值，则剔除后求平均（针对gen_suppressed数据收集）
RIDDfull_averages3 <- datafull %>%
  group_by(group = rep(1:(nrow(datafull)/20), each = 20)) %>% 
  summarise(across(everything(), function(x) mean(x[x != 10000]))) %>%
  select(-group)  
RIDDfull_averages3=data.frame(RIDDfull_averages3)

# 1. 热图 successful suppressed rate； 用averages1
full1=ggplot(data = RIDDfull_averages1, aes(x = drive_conversion, y = release)) +
  geom_tile(aes(fill = suppressed), color =NA) +
  scale_fill_gradientn(colours=mycolorsD,limits = c(0,1),name=" ")+theme_classic()+ 
  scale_y_continuous(limits = c(-0.1, 2.1), breaks = seq(0, 2, by = 0.2))+
  scale_x_continuous(limits = c(-0.05, 1.05), breaks = seq(0, 1, by = 0.1))+  
  theme(aspect.ratio = 1, plot.margin = margin(0.2, 0.2, 0.2, 0.2, unit = "cm"),
        legend.position = "none",  # 隐藏图例
        axis.title.x = element_blank(),   # 去掉X轴坐标标题
        axis.title.y = element_blank(),
        axis.text.x = element_text(angle = 45, hjust = 1))+
  coord_fixed(ratio = 1)   # 设置纵横比为1

# 2. 热图 suppressed_gen；用averages3
full2=ggplot(data = RIDDfull_averages3, aes(x = drive_conversion, y = release)) +
  geom_tile(aes(fill = gen_suppressed), color = NA) +
  scale_fill_gradientn(colours=mycolorsC,limits = c(20, 267),name=" ")+theme_classic() +
  scale_y_continuous(limits = c(-0.1, 2.1), breaks = seq(0, 2, by = 0.2))+
  scale_x_continuous(limits = c(-0.05, 1.05), breaks = seq(0, 1, by = 0.1))+  
  theme(aspect.ratio = 1, plot.margin = margin(0.2, 0.2, 0.2, 0.2, unit = "cm"),
        legend.position = "none",  # 隐藏图例
        axis.title.x = element_blank(),   # 去掉X轴坐标标题
        axis.title.y = element_blank(),
        axis.text = element_text(size = 14),
        axis.line = element_line(linewidth  = 0.7),
        axis.text.x = element_text(angle = 45, hjust = 1))

# 3. 热图 equilibrium size；用averages2
#fertile female
full3=ggplot(data = RIDDfull_averages2, aes(x = drive_conversion, y = release)) +
  geom_tile(aes(fill = fertile_fe), color =NA) +
  scale_fill_gradientn(colours=mycolorsB,limits = c(0, 51000),name=" ")+theme_classic()+
  scale_y_continuous(limits = c(-0.1, 2.1), breaks = seq(0, 2, by = 0.2))+
  scale_x_continuous(limits = c(-0.05, 1.05), breaks = seq(0, 1, by = 0.1))+  
  theme(aspect.ratio = 1, plot.margin = margin(0.2, 0.2, 0.2, 0.2, unit = "cm"),
        legend.position = "none",  # 隐藏图例
        axis.title.x = element_blank(),   # 去掉X轴坐标标题
        axis.title.y = element_blank(),
        axis.text = element_text(size = 14),
        axis.line = element_line(linewidth  = 0.7),
        axis.text.x = element_text(angle = 45, hjust = 1))

#female
full4=ggplot(data = RIDDfull_averages2, aes(x = drive_conversion, y = release)) +
  geom_tile(aes(fill = adult_fe), color =NA) +
  scale_fill_gradientn(colours=mycolorsB,limits = c(1, 100000),name=" ")+theme_classic()+
  scale_y_continuous(limits = c(-0.1, 2.1), breaks = seq(0, 2, by = 0.2))+
  scale_x_continuous(limits = c(-0.05, 1.05), breaks = seq(0, 1, by = 0.1))+  
  theme(aspect.ratio = 1, plot.margin = margin(0.2, 0.2, 0.2, 0.2, unit = "cm"),
        legend.position = "none",  # 隐藏图例
        axis.title.x = element_blank(),   # 去掉X轴坐标标题
        axis.title.y = element_blank(),
        axis.text.x = element_text(angle = 45, hjust = 1))
#adults
full5=ggplot(data = RIDDfull_averages2, aes(x = drive_conversion, y = release)) +
  geom_tile(aes(fill = adult), color =NA) +
  scale_fill_gradientn(colours=mycolorsB,limits = c(1, 300000),name=" ")+theme_classic()+
  scale_y_continuous(limits = c(-0.1, 2.1), breaks = seq(0, 2, by = 0.2))+
  scale_x_continuous(limits = c(-0.05, 1.05), breaks = seq(0, 1, by = 0.1))+  
  theme(aspect.ratio = 1, plot.margin = margin(0.2, 0.2, 0.2, 0.2, unit = "cm"),
        legend.position = "none",  # 隐藏图例
        axis.title.x = element_blank(),   # 去掉X轴坐标标题
        axis.title.y = element_blank(),
        axis.text.x = element_text(angle = 45, hjust = 1))



suppressedrate_up <- ggarrange(SIT1,fRIDL1,ncol =2, nrow = 1,align="v")
suppressedrate_up
suppressedrate_down <- ggarrange(full1,split1,ncol =2, nrow = 1,align="v")
suppressedrate_down
ggsave("suppressedrate_up.jpg", plot = suppressedrate_up, width = 8, height = 6, units = "in")
ggsave("suppressedrate_down.jpg", plot = suppressedrate_down, width = 8, height = 6, units = "in")


fig6_up <- ggarrange(SIT2,fRIDL2,SIT3,fRIDL3,ncol =4, nrow = 1,align="v")
fig6_up
fig6_down <- ggarrange(full2,split2,full3,split3,ncol =4, nrow = 1,align="v")
fig6_down
ggsave("fig6_up.jpg", plot = fig6_up, width = 8, height = 4, units = "in")
ggsave("fig6_down.jpg", plot = fig6_down, width = 15, height = 4, units = "in")


