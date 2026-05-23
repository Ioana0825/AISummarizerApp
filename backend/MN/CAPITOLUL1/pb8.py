# ============================================================
# PROBLEMA 8: Catastrophic Cancellation - ecuatie x²-2px+1=0
# Teorie in curs: Capitol 1 – "Erori de catastrofa"
#   Ecuatia x²-2px+1=0 are coeficientii: a=1, b=-2p, c=1
#   Formula standard: x = (2p ± sqrt(4p²-4)) / 2
#   Cand p mare: sqrt(4p²-4) ≈ 2p => x2 = (2p - ~2p) / 2 => catastrofa!
#   Formula stabila: folosim relatia x1*x2 = 1 => x2 = 1/x1
# CERINTA:Rezolvați ecuația x2 − 2px + 1 = 0 pentru p = 10, 100, 1000, 10000, 100000 cu formula
# standard și formula stabilă.
# ===========================================================

import numpy as np

def solve_quadratic_standard(p):
    """Formula standard: x = (2p ± sqrt(4p²-4)) / 2"""
    discriminant = np.sqrt(4*p**2 - 4)        # sqrt(b²-4ac) = sqrt(4p²-4)
    x1 = (2*p + discriminant) / 2             # radacina mare: (2p + sqrt(...)) / 2
    x2 = (2*p - discriminant) / 2             # radacina mica: PROBLEMATICA pentru p mare!
    return x1, x2

def solve_quadratic_stable(p):
    """Formula stabila: folosim x1*x2 = 1"""
    discriminant = np.sqrt(4*p**2 - 4)        # acelasi discriminant ca mai sus
    x1 = (2*p + discriminant) / 2             # radacina mare (stabila in ambele formule)
    x2 = 1 / x1                               # x2 = 1/x1, relatie stabila numeric
    return x1, x2

# Afisam header tabel
print("Ecuatia: x^2 - 2px + 1 = 0")
print(f"{'p':<10} {'x2 (standard)':<20} {'x2 (stabil)':<20} {'Eroare rel.'}")
print("-" * 70)

for p in [10, 100, 1000, 10000, 100000]:
    x1_std,  x2_std  = solve_quadratic_standard(p)   # rezolvam cu formula standard
    x1_stab, x2_stab = solve_quadratic_stable(p)     # rezolvam cu formula stabila

    # x2_exact = 1/x1_stab (folosim formula stabila ca referinta corecta)
    x2_exact = 1 / x1_stab

    err_rel = abs(x2_std - x2_exact) / x2_exact      # eroarea relativa a formulei standard

    print(f"{p:<10} {x2_std:<20.10e} {x2_stab:<20.10e} {err_rel:.2e}")