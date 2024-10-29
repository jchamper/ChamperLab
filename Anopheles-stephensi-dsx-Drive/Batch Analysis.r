#install.packages("lme4")
#install.packages("emmeans")
library(lme4)
library(emmeans)

files <- list.files(path='.',pattern='\\.csv$')
files

for (f in files) {
  file = read.csv(f,as.is=T,header = T,check.names=F,na.strings="",blank.lines.skip=T)
  data = file
  Group = NULL
  Drive = NULL
  Experiment = NULL
  model = NULL
  dat = NULL
  for (i in 1:nrow(data)) {
    dr = data[i, 1]
    res = data[i, 2]
    exp = data[i, 3]
    dr_vial = rep(i - 1, dr)
    res_vial = rep(i - 1, res)
    dr_inds = rep(1, dr)
    res_inds = rep(0, res)
    exp_dr = rep(exp, dr)
    exp_res = rep(exp, res)
    Group = c(Group, dr_vial, res_vial)
    Drive = c(Drive, dr_inds, res_inds)
    Experiment = c(Experiment, exp_dr, exp_res)
  }
  dat <- data.frame(Group, Drive, as.factor(Experiment))
  model <- glmer(Drive ~Experiment + (1 | Group), data = dat, family = binomial, nAGQ = 25)
  print(summary(model))
  outfile <- file(paste(f, "_analysis.txt", sep=""), "w")
  sink(outfile)
  print("Model summary:")
  print(summary(model))
  writeLines("\n\nJoint test to see if there's any difference between any pairs of experiments.")
  print(joint_tests(model))
  writeLines("\n\nCalculate expected value for each experiment:")
  print(emmeans(model, ~Experiment, type="response"))
  writeLines("\n\nCompare expected values for each experiment to one another as odds ratios.")
  print(emmeans(model, pairwise~Experiment, type="response"))
  writeLines("\n\nShow diferences as a difference in proportions")
  print(emmeans(model, pairwise~Experiment, regrid="response"))
  writeLines("\n\nCompare each experiment to a null expectation value.")
  print(test(emmeans(model, ~Experiment), null = qlogis(0.5)))

  # FYI the following code takes much longer to run than the rest - comment it out if you don't need it.
  writeLines("\n\nModel confidence intervals:")
  print(confint(model))
  writeLines("\n\nModel coefficients:")
  print(coef(model))
  sink()
  close(outfile)
}
print("Finished!")
