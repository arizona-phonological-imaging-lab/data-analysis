library(gss)
library(ggplot2)

filePath <- '/home/josh/git/Autotrace/under-development/analysis/ssanova/minimal_working_examples/ssanova_ready_achlais.txt'

mydata <- read.table(filePath,h=T)
colnames(mydata)<-c("word","token","x","y")
head(mydata)

fit<-ssanova(y~word*x,data=mydata)
summary(fit)

grid <- expand.grid(RTime = seq(0, 1, length = 100), LDur = c("Long", "Short"))

grid$fit <- predict(fit, newdata = grid, se = F)
grid$se <- predict(fit, newdata = grid, se = T)$se.fit

summary(fit)
ggplot(fit)
