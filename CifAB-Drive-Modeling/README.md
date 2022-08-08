[TOC]

# mathematical models and data

All data are in the same folder as the MATLAB scripts, and can be used to make plots directly. You can delete the "tempdata" files to recollect data. Number of points in the heatmap can be adjusted by changing the "precision" parameter. 

Files that end with "odeplot.m" contain the ordinary differential equations for panmictic scenarios. Files that start with "spread1D" contain the partial differential equations for spatial scenarios. 

## cifAB together

Scenarios where CifA and CifB are in the same genetic construct. All files are for panmictic 1-deme scenarios, except for "a05_migration_intro.m" which models a panmictic 2-deme scenario. The script "cifAB_together_plot.m" contains difference equations for the discrete-generation math model. 

## 1-locus

Scenarios where CifA and CifB share the same locus. 

**a07:** Homozygote release, CifA and CifB needed for toxin effect. CifA homozygotes and CifB homozygotes released at different frequencies. 

**a08:** Homozygote release, CifA and CifB needed for toxin effect. CifA homozygotes and CifB homozygotes released at the same frequency.  

**a09:** Heterozygote release, CifA and CifB needed for toxin effect. 

**a10:** Heterozygote release, CifB needed for toxin effect. 

## 2-locus

Scenarios where CifA and CifB are on two separate loci. Double homozygotes (CifA/CifA CifB/CifB) are released. 

**a12:** Double homozygote release, CifA and CifB needed for toxin effect. 

**a13:** Double homozygote release, CifB needed for toxin effect. 

## spatial

Partial 

**a00, a01, a02, a06:** Measurement of wave speed. 

**a03:** Uniform radial drop.

**a04:** Linear radial drop.

**a05:** Ring drop. 

# simulation models and data

Contains SLiM code for simulation models, python code for running simulations, MATLAB code for making plots, and data in ".csv" format collected from the supercomputing cluster. 