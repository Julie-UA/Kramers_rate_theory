#!/usr/bin/env bash

rm boostfiles.dat
rm trajectories.dat

echo "/home/julie/Desktop/LiGaMD_Prod_tryp_ben/Prod_restraint_E_change_11-1/Reweigthing/gamd_stripped.log" >> boostfiles.dat #path to gamd.log file of simulation
echo "/home/julie/Desktop/LiGaMD_Prod_tryp_ben/Prod_restraint_E_change_11-1/NPT_prod.nc" >> trajectories.dat #path to trajectory file of simulation



/home/julie/Desktop/LiGaMD_Prod_tryp_ben/Prod_restraint_E_change_11-1/Test_github/No_Reweight/no_reweight.py \
	--parm ../../../complex.stripped.prmtop \
	--ligand 225 \
	--trajectories trajectories.dat \
	--boosts boostfiles.dat \
	
