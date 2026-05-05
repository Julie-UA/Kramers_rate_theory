import numpy as np
import matplotlib.pyplot as plt


# --- Data ---

A = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47]) 
F = np.array([2.57657265943638000,
4.77601056995759000, 
1.01990829650040000,
0.60306180626536100,
2.38146722556044000,
2.85155912829422000,
3.96412143568853000,
4.31808139786050000,
3.15656833377465000,
2.36855564704873000,
2.11431083151458000,
3.45228049087530000,
2.67673403451235000,
3.85712810994969000,
3.02115731903778000,
2.73435639189784000,
4.17774694523032000,
4.40778768287439000,
5.98438418890857000,
5.52096156481769000,
5.81580547706404000,
5.74325228561993000,
5.16009914564317000,
6.53778872839607000,
6.37810350860958000,
6.31149042077872000,
6.65130299986368000,
7.31870072534935000,
6.44638082704808000,
6.92463049759779000,
6.28783497353398000,
6.60153847681136000,
7.26812243581252000,
6.90038092217593000,
7.16194630528833000,
7.12971584372227000,
7.59424135464182000,
7.79891053622839000,
7.21773697143994000,
8.38925130462148000,
8.80884861583438000,
8.01032197378546000,
8.95028467434511000,
9.96050148899393000,
10.42740507214590000,
11.24996733533170000,
6.29551343375875000]) 
STD = np.array([3.64382399941464000,
3.03159173379728000, 
0.66280980695054400,
1.05525631025775000,
0.75784939725771400,
1.00837089559195000,
1.04220543756566000,
1.22932426046535000,
1.58071856214279000,
1.26863110057111000,
1.73375034014288000,
1.37232829110023000,
1.37209925085822000,
1.26200221576250000,
1.46513317720600000,
2.88289734378121000,
2.26023268169406000,
2.24167054251522000,
2.48796188966151000,
2.04977768021499000,
1.97742281693614000,
1.42258641715507000,
1.30154807394241000,
2.04220726969093000,
1.23369130379451000,
1.91360228273037000,
2.22500686102952000,
2.19659719128166000,
1.09988080937767000,
1.76203209722896000,
2.07032769292018000,
1.91309647769683000,
1.86982311970706000,
1.99794385666782000,
1.69841046889157000,
2.11228795344910000,
1.53884199214592000,
1.87461045812443000,
2.09316594730118000,
2.14767367124081000,
2.17930549827988000,
3.05180531896456000,
1.70232778799284000,
1.52842029349182000,
1.60759804147967000,
1.26909449382399000,
8.90320048012364000])

# -----------------------------
# DERIVATIVES
# -----------------------------
F_prime  = np.gradient(F, A)
F_second = np.gradient(F_prime, A)
print(F_second)
dA = A[1] - A[0]

# -----------------------------
# ERROR PROPAGATION FOR F''(A)
# -----------------------------
STD_second = np.zeros(len(A))

a =  1 / dA**2
b = -2 / dA**2
c =  1 / dA**2


for i in range(1, len(F)-1):
    STD_second[i] = np.sqrt(
        (a**2) * STD[i+1]**2 +
        (b**2) * STD[i]**2 +
        (c**2) * STD[i-1]**2
    )

# --- 1) Bound (well) index: global minimum of F ---
i_b = int(np.argmin(F))  # bound state (minimum)
print('i_b =', i_b)

# --- 2) Barrier index: pick the tallest interior local maximum ---
#local_maxima = [i for i in range(1, len(F)-1) if F[i] > F[i-1] and F[i] > F[i+1]]
#if local_maxima:
#    i_br = int(local_maxima[np.argmax(F[local_maxima])])
#else:
    # Fallback: use interior point near the global max
#    i_br = int(np.argmax(F))
#    if i_br == 0: i_br = 1
#    if i_br == len(F)-1: i_br = len(F)-2
i_br = 7
print('i_br =', i_br)


# --- 3) Unbound index: nearest to the given F value (your choice) ---
#i_u = int(np.argmin(np.abs(F - 0.581894901)))
i_u = 10
print('i_u =', i_u)

# -----------------------------
# CURVATURES + ERRORS
# -----------------------------
k_b,  sk_b  = F_second[i_b],  STD_second[i_b]
k_br, sk_br = F_second[i_br], STD_second[i_br]
k_u,  sk_u  = F_second[i_u],  STD_second[i_u]

# -----------------------------
# FREQUENCIES + ERRORS
# -----------------------------
def freq_and_error(k, sk):
    """Returns (ω, σ_ω) using ω = sqrt(|k|)/2*np.pi."""
    omega = np.sqrt(abs(k)) / (2*np.pi)
    sigma = sk / (np.sqrt(abs(k))*4*np.pi)
    return omega, sigma

omega_b,  sigma_b  = freq_and_error(k_b,  sk_b)
omega_br, sigma_br = freq_and_error(k_br, sk_br)
omega_u,  sigma_u  = freq_and_error(k_u,  sk_u)

# -----------------------------
# OUTPUT
# -----------------------------
print("\n===== CURVATURES & ERRORS =====")
print(f"Bound (index={i_b}):    F'' = {k_b:.6f} ± {sk_b:.6f}")
print(f"Barrier (index={i_br}): F'' = {k_br:.6f} ± {sk_br:.6f}")
print(f"Unbound (index={i_u}):  F'' = {k_u:.6f} ± {sk_u:.6f}")

print("\n===== FREQUENCIES & ERRORS =====")
print(f"ω_b   = {omega_b:.6f}  ± {sigma_b:.6f}")
print(f"ω_br  = {omega_br:.6f} ± {sigma_br:.6f}")
print(f"ω_u   = {omega_u:.6f}  ± {sigma_u:.6f}")


# -----------------------------
# PLOTS
# -----------------------------
plt.figure(figsize=(9,4))
plt.plot(A, F, label='F(X)',linewidth=5)
plt.plot(A, F_second, label='F\"(X)',linewidth=5)
plt.axvline(A[i_b],  color='g', linestyle='--', label='Bound',linewidth=5)
plt.axvline(A[i_br], color='r', linestyle='--', label='Barrier',linewidth=5)
plt.axvline(A[i_u],  color='k', linestyle='--', label='Unbound',linewidth=5)
plt.legend(fontsize=30)
plt.tick_params(axis='both', labelsize=30)
plt.title("Reweighted Free Energy Profile",fontsize=30,weight='bold')
plt.xlabel("distance(COM ligand - COM active site) (Å)",fontsize=30,weight='bold')
plt.ylabel("PMF (kcal/mol)",fontsize=30,weight='bold')
plt.tight_layout()
plt.show()


