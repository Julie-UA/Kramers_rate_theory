# Kramers' rate theory

Step-by-step desciption to reweight ligand binding kinetics from enhanced sampling molecular dynamics simulations (MD) using Kramers' rate theory. This workflow is applied on the output of LiGaMD simulations on the Trypsin_Benzamidine complex.

## PMF free energy profiles of the un- and reweighted LiGaMD Simulations 
A toolkit of python scripts "PyReweighting" is provided to facilitate the reweighting of accelerated molecular dynamics (aMD) simulations.  https://github.com/MiaoLab20/pyreweighting/tree/main

Modify the (No_)Reweight_1D.sh script:
  - path of gamd.log file (line 6)
  - path of trajectory file (line 7)
  - path to reweight.py script (line 11)
  - path of prmtop file (line 12)
  - set RESID of ligand molecule (line 13)

Modify the (no_)reweight.py script:
  - set path to call cpptraj (line 16)
  - Section Calculate distance with cpptraj (line 297)
      - adapt resid protein to get distance between COM ligand and COM active site 

For each run do: 

> ./Reweight_1D.sh 

< pmf-c2-tmp.txt.xvg

and 
> ./No_Reweight_1D.sh 

< pmf-tmp.txt.xvg

Plot the reweighted PMF's

Based on analysis take average and standard deviation of un- and reweighted simulation PMF's and plot these. 
Identify the reaction coordinate of the bound and unbound state as well as of the barrier.
Fill these values and coresponding PMF and STD value in the designated cells in the excel files:
  - Tab Kramers' rate theory cells B2:B7 & D2:D7 & F2:F7


## Curvatures of the PMF free energy profiles of the un- and reweighted LiGaMD Simulations 
Fill with your data for the reaction coordinate, PMF values and STD (lines 7, 8 and 9) for the un- and reweighted values in the respective scripts. Specify the indexes of the reaction coordinates (lines 15, 18, 21) in both scripts and run these.

> python second_der_reweighted.py

<img width="349" height="88" alt="image" src="https://github.com/user-attachments/assets/d2ad02f7-9c04-458c-9814-663aeee21c32" />


> python second_der_unreweighted.py

<img width="345" height="81" alt="image" src="https://github.com/user-attachments/assets/5d43df5b-044b-42f3-bcaf-8f0691d481e5" />

Fill these values in the designated cells (M4:R4 & M5:R5) in the excel files.

## Calculation of the survival function using a Smoluchowski equation solver
The survival function ln[S(t)] can be obtained using a Smoluchowski equation solver coded in C++ (“smol_solver” shared by Prof. Donald Hamelberg). https://github.com/MiaoLab20/smol_solver

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


# Citations
https://github.com/MiaoLab20/pyreweighting/tree/main

https://github.com/MiaoLab20/smol_solver



