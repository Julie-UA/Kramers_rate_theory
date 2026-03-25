#!/bin/bash

sys=Tryp #protein
ligand=BEN #ligand name
igamd=11 #enhanced sampling algoritm used during simulation see Amber manual 11=LiGaMD_Dual

T=300 #temprature
dx=1 #bin size of the PMF profile
for trans in binding unbinding ; do
for reweighted in yes no ; do

if [ $trans == "binding" ]; then
xmin=1 #the range of reaction coordinate that covers an energy barrier crossing event (e.g., ligand binding or unbinding)
xmax=7 #the range of reaction coordinate that covers an energy barrier crossing event (e.g., ligand binding or unbinding)
bc=4 #flag for setting boundary conditions of Smoluchowski equation solver: 4: left absorbing/right reflective
nsteps=1000000 #the total number of steps used to output the time-dependent survival function S(t)
dt=0.00001 #time step used to output the time-dependent survival function S(t)

elif [ $trans == "unbinding" ]; then
xmin=6 #the range of reaction coordinate that covers an energy barrier crossing event (e.g., ligand binding or unbinding)
xmax=10 #the range of reaction coordinate that covers an energy barrier crossing event (e.g., ligand binding or unbinding)
bc=3 # flag for setting boundary conditions of Smoluchowski equation solver: 3: left reflective/right absorbing
nsteps=1000000 #the total number of steps used to output the time-dependent survival function S(t)
dt=0.0001 #time step used to output the time-dependent survival function S(t)

fi # trans
if [ $igamd == 0 ]; then
grep -v "#" data-pmf-1D-dist-lig-host-$sys-$ligand.dat | grep -v "cMD" | grep -v "\-\-" | head -n 60 | awk '{print $1 "        " $2/(0.001987*298)}' > pmf.dat
elif [ $igamd == 10 ]; then
if [ $reweighted == "yes" ]; then
grep -v "#" data-pmf-1D-dist-lig-host-$sys-$ligand.dat | grep -v "cMD" | grep -v "\-\-" | head -n 60 | awk '{print $3 "        " $4/(0.001987*298) }' > pmf.dat
elif [ $reweighted == "no" ]; then
grep -v "#" data-pmf-1D-dist-lig-host-$sys-$ligand.dat | grep -v "cMD" | grep -v "\-\-" | head -n 60 | awk '{print $9 "        " $10/(0.001987*298) }' > pmf.dat
fi # reweighted
elif [ $igamd == 11 ]; then
if [ $reweighted == "yes" ]; then
grep -v "#" data-pmf-1D-dist-lig-host-$sys-$ligand.dat | grep -v "LiGaMD_Dual" | grep -v "\-\-" | head -n 60 | awk '{print $1 "        " $2/(0.001987*298) }' > pmf.dat
elif [ $reweighted == "no" ]; then
grep -v "#" data-pmf-1D-dist-lig-host-$sys-$ligand.dat | grep -v "LiGaMD_Dual" | grep -v "\-\-" | head -n 60 | awk '{print $4 "        " $5/(0.001987*298) }' > pmf.dat
fi # reweighted
fi # igamd
echo "smol_solver pmf.dat $xmin $xmax $bc $dx $dt $nsteps | tee St_smol-$sys-$ligand-igamd$igamd-reweighted$reweighted-${trans}.dat"
/home/julie/Desktop/Kinetics/smol_solver-main/smol_solver pmf.dat $xmin $xmax $bc $dx $dt $nsteps | tee St_smol-$sys-$ligand-igamd$igamd-reweighted$reweighted-${trans}.dat
rm -v pmf.dat
done
done

