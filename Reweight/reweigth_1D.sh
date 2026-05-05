#!/usr/bin/env bash

rm blindspotter-boostfiles.dat
rm blindspotter-trajectories.dat

echo "/home/julie/Desktop/LiGaMD_Prod_tryp_ben/Prod_restraint_E_change_11-1/Reweigthing_correct/gamd_stripped.log" >> blindspotter-boostfiles.dat
echo "/home/julie/Desktop/LiGaMD_Prod_tryp_ben/Prod_restraint_E_change_11-1/NPT_prod.nc" >> blindspotter-trajectories.dat



/home/julie/Desktop/LiGaMD_Prod_tryp_ben/Prod_restraint_E_change_11-1/Reweigthing_correct/reweigth.py \
	--parm ../../complex.stripped.prmtop \
	--ligand 225 \
	--centers ca_active_site.pdb \
	--trajectories blindspotter-trajectories.dat \
	--boosts blindspotter-boostfiles.dat \
	--fraction 1 \
	--output blindspotter-hotspot.pdb
	
