library(ggplot2)
library(dplyr)
library(ggpubr)

setwd("/Users/weizhechen/Documents/Champerlab/DSX_RIDD/Modeling6/FINAL\ data2")
df <- data.frame(read.csv("migrationfull0410.csv"))



# 1.每个参数组合跑20次, 对20次求平均
averages <- df %>%
  group_by(group = gl(n()/20, 20)) %>%
  summarise(across(everything(), mean)) %>%
  select(-group)
averages=data.frame(averages)

mycolorsD=c("white", "#F7FCF5", "#E5F5E0", "#C7E9C0","#A1D99B","#74C476","#41AB5D","#238B45","#006D2C","#00441B")
mycolorsB=c("white", "#FDD49E", "#EF6548", "#D7301F")
mycolorsC=c("white","#9ECAE1","#4292C6","#08519C","#08306B")

# 2. 热图 neighbor
neighbor_freq=ggplot(data = averages, aes(x = release, y = migration)) +
  geom_tile(aes(fill = max_has_dr2), color = NA) +
  scale_fill_gradientn(colours=mycolorsD,limits = c(0, 0.2),name=" ")+theme_classic() +
  scale_y_continuous(limits = c(-0.005, 0.105), breaks = seq(0.00, 0.1, by = 0.01)) + 
  scale_x_continuous(limits = c(-0.1, 2.1), breaks = seq(0.0, 2.0, by = 0.2))  +
  theme(aspect.ratio = 1, plot.margin = margin(0.2, 0.2, 0.2, 0.2, unit = "cm"),
        legend.position = "none",  # 隐藏图例
        axis.title.x = element_blank(),   # 去掉X轴坐标标题
        axis.title.y = element_blank(),
        axis.text = element_text(size = 16),
        panel.grid = element_blank(), axis.text.x = element_text(angle = 45, hjust = 1))  

neighbor_fefemale=ggplot(data = averages, aes(x = release, y = migration)) +
  geom_tile(aes(fill = min_fertile_fe2), color =NA) +
  scale_fill_gradientn(colours=mycolorsB,limits = c(0, 60000),name=" ")+theme_classic() +
  scale_y_continuous(limits = c(-0.005, 0.105), breaks = seq(0.00, 0.1, by = 0.01)) + 
  scale_x_continuous(limits = c(-0.1, 2.1), breaks = seq(0.0, 2.0, by = 0.2))  +
  theme(aspect.ratio = 1, plot.margin = margin(0.2, 0.2, 0.2, 0.2, unit = "cm"),
        legend.position = "none",  # 隐藏图例
        axis.title.x = element_blank(),   # 去掉X轴坐标标题
        axis.title.y = element_blank(),
        axis.text = element_text(size = 16),
        panel.grid=element_blank(),axis.text.x = element_text(angle = 45, hjust = 1))  

# 3. 热图 target
target_gensuppress=ggplot(data = averages, aes(x = release, y = migration)) +
  geom_tile(aes(fill = gen_suppressed), color =NA) +
  scale_fill_gradientn(colours=mycolorsC,limits = c(0, 266),name=" ")+theme_classic() +
  scale_y_continuous(limits = c(-0.005, 0.105), breaks = seq(0.00, 0.1, by = 0.01)) + 
  scale_x_continuous(limits = c(-0.1, 2.1), breaks = seq(0.0, 2.0, by = 0.2))  +
  theme(aspect.ratio = 1, plot.margin = margin(0.2, 0.2, 0.2, 0.2, unit = "cm"),
        legend.position = "none",  # 隐藏图例
        axis.title.x = element_blank(),   # 去掉X轴坐标标题
        axis.title.y = element_blank(),
        axis.text = element_text(size = 16),
        panel.grid = element_blank(),axis.text.x = element_text(angle = 45, hjust = 1)) 

target_fefertile=ggplot(data = averages, aes(x = release, y = migration)) +
  geom_tile(aes(fill = avg_fertile_fe), color = NA) +
  scale_fill_gradientn(colours=mycolorsB,limits = c(1, 60000),name=" ")+theme_classic() +
  scale_y_continuous(limits = c(-0.005, 0.105), breaks = seq(0.00, 0.1, by = 0.01)) + 
  scale_x_continuous(limits = c(-0.1, 2.1), breaks = seq(0.0, 2.0, by = 0.2))  +
  theme(aspect.ratio = 1, plot.margin = margin(0.2, 0.2, 0.2, 0.2, unit = "cm"),
        legend.position = "none",  # 隐藏图例
        axis.title.x = element_blank(),   # 去掉X轴坐标标题
        axis.title.y = element_blank(),
        axis.text = element_text(size = 16),
        panel.grid = element_blank(), axis.text.x = element_text(angle = 45, hjust = 1))  

plots <- ggarrange(target_gensuppress,neighbor_freq,target_fefertile,neighbor_fefemale,ncol =2, nrow = 2)
plots

ggsave("migration.jpg", plot = plots, width = 10, height = 10, units = "in")
