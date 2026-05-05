import numpy as np
import matplotlib.pyplot as plt


# --- Data ---
A = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47]) 
F = np.array([3.51738596760535000,
2.92283625615910000, 
1.19953003182552000,
0.33183995457544200,
0.91392073573907000,
1.47232265389448000,
1.46698608895166000,
1.04277278340196000,
0.55876294752506900,
0.51111797369919800,
0.81305459982825500,
1.31487649300971000,
1.32122935822833000,
1.36512979228292000,
1.49341177741354000,
1.47724129195418000,
1.47109570804134000,
1.44847126246339000,
1.43362192193152000,
1.46880000543306000,
1.39686494974262000,
1.33295355618437000,
1.43620703242216000,
1.47226056038478000,
1.46594366658746000,
1.43165052618388000,
1.47671720210977000,
1.43055085520344000,
1.49798253104811000,
1.48415661110778000,
1.40798972738230000,
1.46521391074610000,
1.52831190843874000,
1.48675097266386000,
1.56521127390662000,
1.66700989372656000,
1.72117402953320000,
1.80068722131661000,
1.96779927764132000,
2.11629341918667000,
2.30131821284830000,
2.30780200768332000,
2.49146388877946000,
3.00784152448640000,
3.24664950344206000,
3.31208867226717000,
3.99837415923404000])
STD = np.array([0.0723201560291838000,
1.4629741356716700000, 
0.5684307189976990000,
0.5229256371354110000,
0.8294771773678150000,
0.9010498913805110000,
0.4976712110408770000,
0.2997343347538160000,
0.4737018404892670000,
0.6186622528107160000,
0.6231197090751800000,
0.4193415255761660000,
0.4713952675279370000,
0.5413560792813100000,
0.4690065874760350000,
0.4199162168221460000,
0.3648177556787730000,
0.2608814485119080000,
0.2423827399453780000,
0.3103923064905630000,
0.3145387003821820000,
0.2733791541664400000,
0.2421346894649260000,
0.2936813395452220000,
0.2502509670892340000,
0.2917474779784590000,
0.3305619528227210000,
0.2948967566738720000,
0.2710260833085930000,
0.2761050047931890000,
0.2807066802639070000,
0.3144427958305710000,
0.3456809539558210000,
0.2898826078499850000,
0.2826825538047290000,
0.3250120509519090000,
0.3343318152395080000,
0.3360998031357830000,
0.4154431183143920000,
0.3061934681546620000,
0.4305246369358420000,
0.2410944992529740000,
0.3413684540186210000,
0.4640612422573650000,
0.4568259074583890000,
0.0299012146646165000,
0.4161235786713920000])

# --- Derivatives (handles non-uniform spacing automatically) ---
F_prime  = np.gradient(F, A)
F_second = np.gradient(F_prime, A)

dA = A[1] - A[0]

print(F_second)

# Plot
plt.figure(figsize=(8,4))
plt.plot(A, F, label='F(A)')
plt.plot(A, F_second, label='F"(A)')
plt.xlabel("A")
plt.ylabel("Value")
plt.legend()
plt.title("Free Energy and Its Second Derivative")
plt.show()


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
i_br = 5
print('i_br =', i_br)


# --- 3) Unbound index: nearest to the given F value (your choice) ---
#i_u = int(np.argmin(np.abs(F - 0.581894901)))
i_u=9
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
    """Returns (ω, σ_ω) using ω = sqrt(|k|)/ 2*np.pi."""
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
print(f"Bound (i={i_b}):    F'' = {k_b:.6f} ± {sk_b:.6f}")
print(f"Barrier (i={i_br}): F'' = {k_br:.6f} ± {sk_br:.6f}")
print(f"Unbound (i={i_u}):  F'' = {k_u:.6f} ± {sk_u:.6f}")

print("\n===== FREQUENCIES & ERRORS =====")
print(f"ω_b   = {omega_b:.6f}  ± {sigma_b:.6f}")
print(f"ω_br  = {omega_br:.6f} ± {sigma_br:.6f}")
print(f"ω_u   = {omega_u:.6f}  ± {sigma_u:.6f}")


# -----------------------------
# PLOTS
# -----------------------------
plt.figure(figsize=(9,4))
plt.plot(A, F, label='F(A)')
plt.plot(A, F_second, label='F\"(A)')
plt.axvline(A[i_b],  color='g', linestyle='--', label='Bound')
plt.axvline(A[i_br], color='r', linestyle='--', label='Barrier')
plt.axvline(A[i_u],  color='k', linestyle='--', label='Unbound')
plt.legend()
plt.title("Free Energy and Curvature")
plt.xlabel("A")
plt.ylabel("Value")
plt.tight_layout()
plt.show()


