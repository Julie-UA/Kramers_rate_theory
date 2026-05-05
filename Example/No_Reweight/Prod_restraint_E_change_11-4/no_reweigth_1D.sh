#!/usr/bin/env bash

# Identify hotspot
rm blindspotter-boostfiles.dat
rm blindspotter-trajectories.dat

echo "/home/julie/Desktop/LiGaMD_Prod_tryp_ben/Prod_restraint_E_change_11-4/No_Reweigthing_correct/gamd_stripped.log" >> blindspotter-boostfiles.dat
echo "/home/julie/Desktop/LiGaMD_Prod_tryp_ben/Prod_restraint_E_change_11-4/NPT_prod.nc" >> blindspotter-trajectories.dat



/home/julie/Desktop/LiGaMD_Prod_tryp_ben/Prod_restraint_E_change_11-4/No_Reweigthing_correct/no_reweigth.py \
	--centers ca_active_site.pdb \
	--parm ../../complex.stripped.prmtop \
	--ligand 225 \
	--trajectories blindspotter-trajectories.dat \
	--boosts blindspotter-boostfiles.dat \
	--fraction 1 \
	--output blindspotter-hotspot.pdb
	


