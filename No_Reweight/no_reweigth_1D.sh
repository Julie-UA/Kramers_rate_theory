#!/usr/bin/env bash


rm boostfiles.dat
rm trajectories.dat

echo "/home/julie/Desktop/LiGaMD_Prod_tryp_ben/Prod_restraint_E_change_11-1/No_Reweigthing/gamd_stripped.log" >> boostfiles.dat
echo "/home/julie/Desktop/LiGaMD_Prod_tryp_ben/Prod_restraint_E_change_11-1/NPT_prod.nc" >> trajectories.dat



/home/julie/Desktop/LiGaMD_Prod_tryp_ben/Prod_restraint_E_change_11-1/No_Reweigthing/no_reweigth.py \
	--centers ca_active_site.pdb \
	--parm ../../complex.stripped.prmtop \
	--ligand 225 \
	--trajectories trajectories.dat \
	--boosts boostfiles.dat \
	--fraction 1 \
	--output hotspot.pdb
	


