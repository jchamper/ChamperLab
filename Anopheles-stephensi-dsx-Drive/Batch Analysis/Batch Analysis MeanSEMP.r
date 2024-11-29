#install.packages("lme4")
#install.packages("emmeans")
library(lme4)
library(emmeans)


# Configuration parameters
data_file = "combined.csv"
expectation_value = 0.5
output_conf_intervals_and_coefs = FALSE  # Takes much longer to run.


# Read the combined CSV file
combined_data <- read.csv(data_file, as.is = TRUE, header = TRUE, check.names = FALSE,
                          na.strings = "", blank.lines.skip = TRUE)

# Extract unique experiment names
experiments <- unique(combined_data$Experiment)

# Loop through each experiment
for (experiment in experiments) {
  # Subset the data for the current experiment
  cur_data <- subset(combined_data, Experiment == experiment)
  group = NULL
  drive = NULL
  model = NULL
  dataframe = NULL
  for (i in 1:nrow(cur_data)) {
    dr = cur_data[i, 1]
    res = cur_data[i, 2]
    dr_vial = rep(i - 1, dr)
    res_vial = rep(i - 1, res)
    dr_inds = rep(1, dr)
    res_inds = rep(0, res)
    group = c(group, dr_vial, res_vial)
    drive =  c(drive, dr_inds, res_inds)
  }
  dataframe <- data.frame(group, drive)
  model <- glmer(drive ~ 1 + (1 | group), data = dataframe, family = binomial, nAGQ = 25)
  print(summary(model))
  outfile <- file(paste(experiment, "_analysis.txt", sep = ""), "w")
  sink(outfile)
  print("Model summary:")
  print(summary(model))
  writeLines("\n\nCalculate expected value:")
  print(emmeans(model, ~1, type="response"))
  writeLines("\n\nCompare the experiment to a null expectation value.")
  print(test(emmeans(model, ~1), null = qlogis(expectation_value)))
  
  if (output_conf_intervals_and_coefs) {
    writeLines("\n\nModel confidence intervals:")
    print(confint(model))
    writeLines("\n\nModel coefficients:")
    print(coef(model))
  }
  sink()
  close(outfile)
}

if (length(experiments) > 1) {
  group = NULL
  drive = NULL
  Experiment = NULL
  model = NULL
  dataframe = NULL
  for (i in 1:nrow(combined_data)) {
    dr = combined_data[i, 1]
    res = combined_data[i, 2]
    exp = combined_data[i, 3]
    dr_vial = rep(i - 1, dr)
    res_vial = rep(i - 1, res)
    dr_inds = rep(1, dr)
    res_inds = rep(0, res)
    exp_dr = rep(exp, dr)
    exp_res = rep(exp, res)
    group = c(group, dr_vial, res_vial)
    drive = c(drive, dr_inds, res_inds)
    Experiment = c(Experiment, exp_dr, exp_res)
  }
  dataframe <- data.frame(group, drive, as.factor(Experiment))
  model <- glmer(drive ~Experiment + (1 | group), data = dataframe, family = binomial, nAGQ = 25)
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
  print(test(emmeans(model, ~Experiment), null = qlogis(expectation_value)))
  
  if (output_conf_intervals_and_coefs) {
    writeLines("\n\nModel confidence intervals:")
    print(confint(model))
    writeLines("\n\nModel coefficients:")
    print(coef(model))
  }
  sink()
  close(outfile)
}
print("Finished!")
