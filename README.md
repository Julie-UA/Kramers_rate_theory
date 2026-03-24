# Kramers' rate theory

Step-by-step desciption to reweight ligand binding kinetics from enhanced sampling molecular dynamics simulations (MD) using Kramers' rate theory. This workflow is applied on the output of LiGaMD simulations on the Trypsin_Benzamidine complex.

## PMF free energy profiles of the un- and reweighted LiGaMD Simulations 
For each run do: 

> python PyReweighting-1D.py -input tmp.txt -T 300 -cutoff 75 -Xdim %d %d -disc 1 -Emax 20 -job amdweight_CE -weight processed.gamd.txt

< pmf-c2-tmp.txt.xvg

and 
> python PyReweighting-1D.py -input tmp.txt -T 300 -cutoff 75 -Xdim %d %d -disc 1 -Emax 20 -job noweight -weight processed.gamd.txt

< pmf-c2-tmp.txt.xvg

plot reweighted PMF's

Based on analysis take average and standard deviation of un- and reweighted simulation PMF's and plot these. 
Identify the reaction coordinate of the bound and unbound state as well as of the barrier.


## Curvatures of the PMF free energy profiles of the un- and reweighted LiGaMD Simulations 
Change the data and indexes of the reaction coordinates in both scripts and run these.
> python second_der.py
> python second_der_mod.py 




