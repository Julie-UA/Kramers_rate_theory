#!/bin/bash
#SBATCH --job-name=LiGaMD_11-1
#SBATCH --output=NPT_prod.%j.out
#SBATCH --error=NPT_prod.%j.err
#SBATCH --partition=batch_gpu.q
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:l40s:1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G

# module load apptainer

# Optional OpenMP threading env (mostly unused by pmemd.cuda)
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
export APPTAINERENV_OMP_NUM_THREADS=$OMP_NUM_THREADS

# Container and input file paths
SIF=${SIF:-/imec/other/isd3/containers/amber/amber24_cuda_mpi.sif}
BIND_DIR=${BIND_DIR:-/imec/other/isd3/luyck100/Trypsin_Benzamidine/}
PRMTOP=${PRMTOP:-/imec/other/isd3/luyck100/Trypsin_Benzamidine/LiGaMD/complex.solvated.prmtop}
RESTART=${RESTART:-/imec/other/isd3/luyck100/Trypsin_Benzamidine/LiGaMD/NPT_eq/NPT_eq.ncrst}

# Create NPT production input file
cat > NPT_prod.inp<<EOF
NPT_prod
&cntrl
        imin=0,
        nstlim=500744000,   ! 500.000.000 steps of 0.002 ps = 1 micros = 1000 ns
        dt=0.002,
        irest=1,
        ig=-1,
        ntx=5,
        ntc=2,
        ntf=2,
        cut=8.0,
        ntpr=50000,     ! 50.000 = 10.000 frames
        ntwx=50000,     ! 50.000 = 10.000 frames 
        ntwr=50000,     ! 50.000 = 10.000 frames
	ntwprt=3240,
        ntt=1,
        temp0=300.0,
        ntb=2,              
        ntp=1,              
        barostat=1,         
        pres0=1,
        tautp=1.0,
        taup=2.0,
	
	ntr=1,
	restraint_wt=0.2,
	restraintmask='(:35,118,187) & @CA'
        igamd=11,
        iE=1,
        iEP=1,
        iED=1,
        ntcmdprep=62000,   !default is 200,000 for a simulation with 2 fs timestep
        ntcmd=372000,      !default is 1,000,000 for a simulation with 2 fs timestep
        ntebprep=62000,    !default is 200,000 for a simulation with 2 fs timestep
        nteb=372000,       !default is 1,000,000 for a simulation with 2 fs timestep
        ntave=62000,       !4*number of atoms +-5000 atoms
        irest_gamd=0,
        sigma0P=1.3,        
        sigma0D=10.6,
        timask1=':LIG',
        scmask1=':LIG',
	icfe=1,
	ifsc=1,
	ntf=1,
        nlig=1,
        ibblig=0,
/
EOF

# Run pmemd.cuda inside container
apptainer exec --nv --bind "$BIND_DIR":"$BIND_DIR" --pwd "$PWD" "$SIF" \
        pmemd.cuda \
        -O \
        -i   NPT_prod.inp \
        -o   NPT_prod.out \
        -p   "$PRMTOP" \
        -c   "$RESTART" \
	-ref "$RESTART" \
        -r   NPT_prod.ncrst \
        -x   NPT_prod.nc \
        -inf NPT_prod.mdinfo

# Generate PDB from final coordinates using cpptraj
echo "Generating PDB from final coordinates"
apptainer exec --bind "$BIND_DIR":"$BIND_DIR" --pwd "$PWD" "$SIF" \
        cpptraj -p "$PRMTOP" -y NPT_prod.ncrst -x NPT_prod.pdb -xa PDB

echo "NPT production complete"

