# ============================================================
# PROBLEMA 9: Numarul de conditionare - matrice bine vs. slab conditionata
# Teorie in curs: Capitol 1 / Capitol 3 – "Numarul de conditionare"
#   cond(A) = ||A|| * ||A^(-1)||
#   Sistem bine conditionat: cond mic  -> eroare mica in b => eroare mica in x
#   Sistem slab conditionat: cond mare -> eroare mica in b => eroare MARE in x
# CERINTA: Comparați sensibilitatea soluției la perturbații de 0.1% în b pentru două sisteme 2×2:
# A_bun = [[4,1],[1,3]], A_slab = [[1,1],[1,1.0001]]
# ============================================================

import numpy as np

# Matrice bine conditionata
A_bun  = np.array([[4.0, 1.0],
                   [1.0, 3.0]])

# Matrice slab conditionata (randurile sunt aproape proportionale => aproape singulara)
A_slab = np.array([[1.0, 1.0],
                   [1.0, 1.0001]])

b      = np.array([1.0, 2.0])      # vectorul b original
b_pert = b * (1 + 0.001)           # perturbam b cu 0.1%

for eticheta, A in [("BINE conditionata", A_bun), ("SLAB conditionata", A_slab)]:
    cond   = np.linalg.cond(A)            # calculam numarul de conditionare
    x      = np.linalg.solve(A, b)        # solutia pentru b original
    x_pert = np.linalg.solve(A, b_pert)   # solutia pentru b perturbat

    err_rel_b = np.linalg.norm(b_pert - b) / np.linalg.norm(b)    # eroarea relativa in b
    err_rel_x = np.linalg.norm(x_pert - x) / np.linalg.norm(x)    # eroarea relativa in x

    print(f"\nMatrice {eticheta}:")
    print(f"  cond(A)           = {cond:.2f}")
    print(f"  Eroare relativa b = {err_rel_b:.4%}")
    print(f"  Eroare relativa x = {err_rel_x:.4%}")
    print(f"  Amplificare       = {err_rel_x/err_rel_b:.1f}x")

print()
print("Concluzie: matricea slab conditionata amplifica mult eroarea din b.")