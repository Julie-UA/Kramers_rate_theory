# Kramers' rate theory

Step-by-step desciption to reweight ligand binding kinetics from enhanced sampling molecular dynamics simulations (MD) using Kramers' rate theory. This workflow is applied on the output of LiGaMD simulations on the Trypsin_Benzamidine complex.

## PMF free energy profiles of the un- and reweighted LiGaMD Simulations 
A toolkit of python scripts "PyReweighting" is provided to facilitate the reweighting of accelerated molecular dynamics (aMD) simulations. 
For each run do: 

> python PyReweighting-1D.py -input tmp.txt -T 300 -cutoff 75 -Xdim %d %d -disc 1 -Emax 20 -job amdweight_CE -weight processed.gamd.txt

< pmf-c2-tmp.txt.xvg

and 
> python PyReweighting-1D.py -input tmp.txt -T 300 -cutoff 75 -Xdim %d %d -disc 1 -Emax 20 -job noweight -weight processed.gamd.txt

< pmf-c2-tmp.txt.xvg

plot reweighted PMF's

Based on analysis take average and standard deviation of un- and reweighted simulation PMF's and plot these. 
Identify the reaction coordinate of the bound and unbound state as well as of the barrier.
Fill these values and coresponding PMF value in the designated cells in the excel files.


## Curvatures of the PMF free energy profiles of the un- and reweighted LiGaMD Simulations 
Change the data and indexes of the reaction coordinates in both scripts and run these.
> python second_der.py

<img width="386" height="90" alt="image" src="https://github.com/user-attachments/assets/5156934f-1d12-4c1d-83f8-4c4a6069ffcb" />

> python second_der_mod.py

<img width="386" height="90" alt="image" src="https://github.com/user-attachments/assets/5156934f-1d12-4c1d-83f8-4c4a6069ffcb" />

Fill these values in the designated cells in the excel files.

## Calculation of the survival function using a Smoluchowski equation solved
The survival function ln[S(t)] can be obtained using a Smoluchowski equation solver coded in C++ (“smol_solver” shared by Prof. Donald Hamelberg).

> smol_solver pmf.dat $xmin $xmax $bc $dx $dt $nsteps

Paste the values of the four data files in the designated tab in the excel file. 


# Citations
https://github.com/MiaoLab20/pyreweighting/tree/main

https://github.com/MiaoLab20/smol_solver



