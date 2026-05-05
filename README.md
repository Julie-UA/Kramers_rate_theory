# Kramers' rate theory

Step-by-step desciption to reweight ligand binding kinetics from enhanced sampling molecular dynamics simulations (MD) using Kramers' rate theory. This workflow is applied on the output of LiGaMD_Dual simulations on the trypsin-benzamidine complex.

## PMF free energy profiles of the un- and reweighted LiGaMD Simulations 
A toolkit of python scripts "PyReweighting" is used to facilitate the reweighting of accelerated molecular dynamics (aMD) simulations.  This script is provided by Miao, Y., et al. https://github.com/MiaoLab20/pyreweighting/tree/main. We auto;ated several steps using a shell script:

Modify the (no_)reweight_1D.sh scripts:
  - path of gamd.log file (line 6)
  - path of trajectory file (line 7)
  - path to reweight.py script (line 11)
  - path of prmtop file (line 12)
  - set RESID of ligand molecule (line 13)

Modify the (no_)reweight.py scripts:
  - set path to call cpptraj (line 16)
  - Section Calculate distance with cpptraj (line 446)
      - adapt resid protein to get distance between COM ligand and COM active site
      - modified to only included frames of LiGaMD_prod, ensure length gamd.log is the same as trajectory file 

For each run do: 

> ./Reweight_1D.sh 

< pmf-c2-tmp.txt.xvg

and 
> ./No_Reweight_1D.sh 

< pmf-tmp.txt.xvg

Plot the reweighted PMF's

Based on analysis take average and standard deviation of the useable un- and reweighted simulation PMF's and plot these (Tabs PMF_reweighted and PMF_no_reweighted). For the determination of the useable PMF's please refer to the education tutorial article. Identify the reaction coordinate of the bound and unbound state as well as of the barrier. Fill these values and coresponding PMF and STD value in the designated cells in the excel files:
  - Tab Kramers' rate theory cells B2:B7 & D2:D7 & F2:F7


## Curvatures of the PMF free energy profiles of the un- and reweighted LiGaMD Simulations 
Fill your data for the reaction coordinate, PMF values and STD (under # --- Data ---) for the un- and reweighted values in the respective scripts. Specify the indexes of the reaction coordinates (lines 126, 138, 144) in both scripts and run these.

> python second_der_reweighted.py

> python second_der_unreweighted.py

Fill the obtained values in the designated cells (M4:R4 & M5:R5) in the excel files.

## Calculation of the survival function using a Smoluchowski equation solver
The survival function S(t) can be obtained using a Smoluchowski equation solver coded in C++ (“smol_solver” shared by Prof. Donald Hamelberg). https://github.com/MiaoLab20/smol_solver

Compile:
> ./make.sh

Prepare the data-pmf-1D-dist-lig-host-Tryp-BEN.dat file. This file should contain 6 columns with folowwing header:

#RC	PMF(kcal/mol)	STDEV	#RC	PMF(kcal/mol)	STDEV

LiGaMD_Dual_reweight		STDEV	LiGaMD_Dual_no_reweight		STDEV


Adapt the values (lines 3, 4, 5, 7, 8, 12, 13, 20, and 21)  required in the script and run it: 
> ./run.sh

< St_smol-Tryp-BEN-igamd11-reweightedno-binding.dat

< St_smol-Tryp-BEN-igamd11-reweightedno-unbinding.dat

< St_smol-Tryp-BEN-igamd11-reweightedyes-binding.dat

< St_smol-Tryp-BEN-igamd11-reweightedyes-unbinding.dat

Paste the values of the four data files in the designated columns in the Smol tab in the excel file. 

## Kramers' acceleration rates and reweighted ligand binding kinetics 
All Kramers' rate constants, acceleration rates and reweighted ligand binding kinetics are automatically calculated in the excel file. In addition the kD and binding free energy is calculated. For the explenation how these terms are computed please refer to the education tutorial article.

# Citations
https://github.com/MiaoLab20/pyreweighting/tree/main

https://github.com/MiaoLab20/smol_solver

# Notes
It is important to not move cells in the excel file. Doing so will lead to incorrect implementation of the formulas.


The trajectory files of the production are avaible upon request due to large size.



