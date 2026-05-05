import os
import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5), dpi=300)

# Accessible style variations
line_styles = ['-' ] * 10
line_widths = [1.5] * 10

# Color-blind-safe palette (secondary cue)
colors = plt.get_cmap("tab10").colors

for i in range(1, 11):
    folder = f"Prod_restraint_E_change_11-{i}/Reweigthing"
    file_path = os.path.join(folder, "pmf-c2-tmp.txt.xvg")

    if not os.path.isfile(file_path):
        print(f"Warning: {file_path} not found, skipping.")
        continue

    with open(file_path) as f:
        lines = [
            line for line in f
            if not line.lstrip().startswith(('#', '@'))
        ]

    data = np.loadtxt(lines)
    x = data[:, 0]
    y = data[:, 1]

    idx = i - 1

    plt.plot(
        x, y,
        linestyle=line_styles[idx],
        color=colors[idx % len(colors)],
        linewidth=line_widths[idx],
        label=f"Run {i}"
    )

# Axis labels
plt.xlabel("Distance Ligand COM – Active site COM (Å)", fontweight='bold')
plt.ylabel("PMF (kcal/mol)", fontweight='bold')

plt.xticks(fontweight='bold')
plt.yticks(fontweight='bold')

plt.legend(
    fontsize=12,
    frameon=False,
    ncol=2
)

plt.tight_layout()
plt.savefig("reweighted_pmfs_plot.png", dpi=600)
plt.show()

