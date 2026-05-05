import numpy as np
import matplotlib.pyplot as plt

# Load data (skip header line)
data_no = np.loadtxt("St_smol-Tryp-BEN-igamd11-reweightedno-unbinding.dat", skiprows=1)
data_yes = np.loadtxt("St_smol-Tryp-BEN-igamd11-reweightedyes-unbinding.dat", skiprows=1)

# Extract columns
t_no = data_no[:, 0]
lnS_no = data_no[:, 1]

t_yes = data_yes[:, 0]
lnS_yes = data_yes[:, 1]

# Convert ln(S) -> S
S_no = np.exp(lnS_no)
S_yes = np.exp(lnS_yes)

# Create plot
plt.figure()

plt.plot(t_no, S_no,'--', linewidth=2, label="No binding")
plt.plot(t_yes, S_yes, '-', linewidth=2, label="Yes binding")

# Thicker ticks
plt.xticks(fontweight='bold')
plt.yticks(fontweight='bold')

# Axis labels (bold)
plt.xlabel("t (s)", fontweight='bold')
plt.ylabel("S(t)", fontweight='bold')

# Legend
#plt.legend()

plt.tight_layout()
plt.savefig("St_unbinding.png", dpi=600)  # higher resolution
plt.show()
