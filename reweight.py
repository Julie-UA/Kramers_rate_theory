#!/usr/bin/env python

import argparse
import sys
import os
import random
import numpy as np

try:
    from scipy.optimize import least_squares
    _HAVE_SCIPY = True
except Exception:
    _HAVE_SCIPY = False

VERSION = "1.0"
CPPTRAJ = "cpptraj" #"/usr/local/amber24/bin/cpptraj" path to used to call cpptraj function

# _residuals function
# ###################

def _residuals(x: np.ndarray, centers: np.ndarray, radii: np.ndarray) -> np.ndarray:
    """Residuals f_i(x) = ||x - c_i|| - r_i."""
    diffs = x[None, :] - centers  # (N,3)
    dists = np.linalg.norm(diffs, axis=1)  # (N,)
    return dists - radii

# _jacobian function
# ##################

def _jacobian(x: np.ndarray, centers: np.ndarray) -> np.ndarray:
    """
    Jacobian J_ij = ∂f_i/∂x_j = (x_j - c_ij)/||x - c_i||.
    If x coincides with a center, regularize to avoid division by zero.
    """
    diffs = x[None, :] - centers  # (N,3)
    dists = np.linalg.norm(diffs, axis=1)
    eps = 1e-12
    dists = np.where(dists < eps, eps, dists)
    return diffs / dists[:, None]  # (N,3)

# __covariance_from_jacobian function
# ###################################

def _covariance_from_jacobian(x: np.ndarray, centers: np.ndarray, radii: np.ndarray) -> tuple[np.ndarray, float]:
    """Return covariance matrix (3x3) and residual variance s2."""
    r = _residuals(x, centers, radii)
    J = _jacobian(x, centers)
    JTJ = J.T @ J
    # Regularize if near-singular
    try:
        JTJ_inv = np.linalg.inv(JTJ)
    except np.linalg.LinAlgError:
        JTJ_inv = np.linalg.pinv(JTJ)
    N = centers.shape[0]
    dof = max(N - 3, 1)
    s2 = float((r @ r) / dof)
    cov = s2 * JTJ_inv
    return cov, s2

# _gauss_newton function
# ######################

def _gauss_newton(
    x0: np.ndarray,
    centers: np.ndarray,
    radii: np.ndarray,
    max_iter: int = 200,
    tol: float = 1e-10,
) -> tuple[np.ndarray, bool]:
    """
    Simple damped Gauss-Newton fallback optimizer.
    Returns (x, converged).
    """
    x = x0.astype(float).copy()
    lam = 1e-3  # small damping
    for _ in range(max_iter):
        r = _residuals(x, centers, radii)  # (N,)
        J = _jacobian(x, centers)         # (N,3)
        JTJ = J.T @ J
        g = J.T @ r
        try:
            step = -np.linalg.solve(JTJ + lam * np.eye(3), g)
        except np.linalg.LinAlgError:
            step = -np.linalg.pinv(JTJ + lam * np.eye(3)) @ g
        x_new = x + step
        if np.linalg.norm(step) < tol * (1.0 + np.linalg.norm(x)):
            return x_new, True
        # simple acceptance rule
        if np.sum(_residuals(x_new, centers, radii) ** 2) < np.sum(r ** 2):
            # good step; slightly decrease damping
            lam *= 0.7
            x = x_new
        else:
            # reject; increase damping
            lam *= 2.0
    return x, False

# bootstrap_uncertainty function
# ##############################

def bootstrap_uncertainty(
    centers: np.ndarray,
    radii: np.ndarray,
    n_boot: int = 500,
    random_state: int | None = 0,
    use_scipy: bool | None = None,
) -> dict:
    """
    Optional: non-parametric bootstrap to assess uncertainty robustness.
    Resamples the N spheres with replacement and re-fits each time.

    Returns dict with keys:
        - 'mean' : (3,) bootstrap mean of solutions
        - 'std'  : (3,) bootstrap standard deviation per axis
        - 'samples' : (n_boot, 3) all bootstrap solutions
    """
    rng = np.random.default_rng(random_state)
    N = centers.shape[0]
    sols = []
    base = IntersectSpheres(centers, radii, use_scipy=use_scipy)["x"]
    for _ in range(n_boot):
        idx = rng.integers(0, N, size=N)
        cs = centers[idx]
        rs = radii[idx]
        res = IntersectSpheres(cs, rs, x0=base, use_scipy=use_scipy)
        sols.append(res["x"])
    sols = np.array(sols)
    return {"mean": sols.mean(axis=0), "std": sols.std(axis=0, ddof=1), "samples": sols}

# Parse commannd-line arguments
# #############################

def ParseCommandline():

	parser = argparse.ArgumentParser()

	parser.add_argument("-v",
					"--version",
					action="store_true", 
					help="returns the version of the script",
					required=False)
					
					
	parser.add_argument("-p",
						"--parm",
						type=str,			
						help="AMBER parameter file describing the trajectory files. ",
						required=True)
					
	parser.add_argument("-l",
						"--ligand",
						type=int,			
						help="ligand id (number) as it occurs in the parameter file",
						required=True)
					
	parser.add_argument("-b",
						"--boosts",
						type=str,			
						help="TEXT file that contains the full path of all boost files that should be processed",
						required=True)
					
	parser.add_argument("-t",
						"--trajectories",
						type=str,			
						help="TEXT file that contains the full path of all trajectory files that should be processed",
						required=True)

	

	args = parser.parse_args()
	
	# --version
	if args.version:
		print("Version %s" % (VERSION))
		sys.exit(0)
	

	# --ligand
	if args.ligand < 0:
		print("Ligand id should be larger or equal than 0 - quitting with error code 1")
		sys.exit(1)
	
	# --trajectories
	if not os.path.exists(args.trajectories):
		print("Can not find the trajectories file %s - quitting with error code 1" % (args.trajectories))
		sys.exit(1)
	if not os.path.isfile(args.trajectories):
		print("The trajectories file %s is errorneous - quitting with error code 1" % (args.trajectories))
		sys.exit(1)
	
	# --boosts
	if not os.path.exists(args.boosts):
		print("Can not find the boosts file %s - quitting with error code 1" % (args.boosts))
		sys.exit(1)
	if not os.path.isfile(args.boosts):
		print("The boosts file %s is errorneous - quitting with error code 1" % (args.boosts))
		sys.exit(1)
	
	# --parm
	if not os.path.exists(args.parm):
		print("Can not find the parm file %s - quitting with error code 1" % (args.parm))
		sys.exit(1)
	if not os.path.isfile(args.parm):
		print("The parm file %s is errorneous - quitting with error code 1" % (args.parm))
		sys.exit(1)
	
	# Return
	return args
	
# Read the trajectory files
# #########################

def ReadTrajectoryFiles(fname):

	TRAJECTORIES = []
	
	try:
		f = open(fname, "r")
	except OSError:
		print("Could not open the trajectories file %s - quitting with error code 1" % (fname))
		sys.exit(1)
		
	with f:
		for LINE in f.readlines():
			LINE = LINE.strip()
			if LINE == "" or LINE[0] == "#": continue
			if not os.path.exists(LINE):
				print("Can not find the trajectory file %s - quitting with error code 1" % (LINE))
				sys.exit(1)
			if not os.path.isfile(LINE):
				print("The trajectory file %s is errorneous - quitting with error code 1" % (LINE))
				sys.exit(1)
			TRAJECTORIES.append(LINE)
	
	return TRAJECTORIES
			
# Process the boost files
# #######################

def ProcessBoostFiles(boostFileName, outFile):

	BOOSTFILES = []	
	
	try:
		f = open(boostFileName, "r")
	except OSError:
		print("Could not open the boosts file %s - quitting with error code 1" % (boostFileName))
		sys.exit(1)
		
	with f:
		for LINE in f.readlines():
			LINE = LINE.strip()
			if LINE == "" or LINE[0] == "#": continue
			if not os.path.exists(LINE):
				print("Can not find the boosts file %s - quitting with error code 1" % (LINE))
				sys.exit(1)
			if not os.path.isfile(LINE):
				print("The boosts file %s is errorneous - quitting with error code 1" % (LINE))
				sys.exit(1)
			BOOSTFILES.append(LINE)
	
	COUNTER = 1
	fo = open("%s" % (outFile), "w")
	for FN in BOOSTFILES:
		try:
			f = open(FN, "r")
		except OSError:
			print("Could not open the boosts file %s - quitting with error code 1" % (FN))
			sys.exit(1)
		with f:
			for LINE in f.readlines():
				LINE = LINE.strip()
				if LINE == "" or (len(LINE) > 0 and LINE[0] == "#"): continue
				FIELDS = LINE.split()
				if len(FIELDS) < 7:
					print("Warning: Line does not have enough fields (need at least 7), skipping: %s" % LINE)
					continue
				try:
					v = float(FIELDS[6])
					fo.write("%.5f %d %.5f\n" % (v / (0.001987 * 300.0), COUNTER, v))
					COUNTER += 1
				except ValueError:
					print("Warning: Could not parse float from field 6, skipping: %s" % LINE)
					continue
	fo.close()


# Calculate distances with cpptraj
# ################################

def CalculateDistances(trajectoryFiles, distancesOutFile, parmFile, ligandid): #resids

	f = open("cpptraj.inp", "w")
	f.write("parm %s\n" % (parmFile))
	for TF in trajectoryFiles: f.write("trajin %s 15 last 1\n" % (TF))  # modified to only included frames of LiGaMD_prod
	#for RESID in resids: f.write("distance %d :%d :%d@CA out %s\n" % (RESID, ligandid, RESID, distancesOutFile))
	f.write("distance COM_LIG_active :%d :171-174,177,191-198,204-206@CA out %s\n" % (ligandid, distancesOutFile))
	f.write("run\n")
	f.close()
	CMD = "%s -i cpptraj.inp" % (CPPTRAJ)
	
	return os.system(CMD)


# Main
# ####

if __name__ == "__main__":

	RADII = []

	# Parse command-line
	# ##################
	
	args = ParseCommandline()
	
	
	# Read the trajectory files
	# #########################
	
	trajectoryFiles = ReadTrajectoryFiles(args.trajectories)
	

	# Calculate the distances
	# #######################
	
	CalculateDistances(trajectoryFiles, "distances.txt", args.parm, args.ligand) 
	
	
	# Process the boost files
	# #######################
	
	ProcessBoostFiles(args.boosts, "processed.gamd.txt")
	
	
	# Loop over all centers to calculate PMFs
	# #######################################
	
	col_index = 1    # example: second column

	# Extract column → tmp.txt
	with open("distances.txt", "r") as fi, open("tmp.txt", "w") as fo:
		for line in fi:
		    line = line.strip()
		    if not line or line.startswith("#"):
		        continue
		    fields = line.split()
		    if len(fields) > col_index:
		        fo.write(fields[col_index] + "\n")

	# Compute min/max
	values = []

	with open("tmp.txt", "r") as fi:
		for line in fi:
		    try:
		        values.append(float(line.strip()))
		    except ValueError:
		        pass

	if not values:
		raise ValueError("Error: No valid numeric values found in tmp.txt")

	MIN = min(values)
	MAX = max(values)


	# Run the 1D reweighting script
	# #############################

	script_path = os.path.join(os.path.dirname(__file__), "PyReweighting-1D.py")
	CMD = "%s %s -input tmp.txt -T 300 -cutoff 75 -Xdim %d %d -disc 1 -Emax 20 -job amdweight_CE -weight processed.gamd.txt" % (sys.executable, script_path, MIN, MAX)
	print (CMD)
	os.system(CMD)
	
		
	
