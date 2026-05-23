"""
PROBLEMA 30 – Conditionare buna vs. slaba – impact practic
CERINTA: Sistemul slab condiționat: A = [[1,1],[1,1.0001]], b = [2, 2.0001]. Perturbăm b cu 0.1% și
observăm.
============================================================
TEORIE (Curs: Capitol "Conditionarea Sistemelor Liniare"):

NUMARUL DE CONDITIONARE al matricei A:
  cond(A) = ||A|| * ||A^{-1}||

El masoara CUM SE AMPLIFICA ERORILE din b in solutia x.

Daca perturbam b cu delta_b, solutia se schimba cu delta_x:
  ||delta_x|| / ||x||  <=  cond(A) * ||delta_b|| / ||b||

=> Daca cond(A) este MARE (matrice slab conditionata):
     - o mica eroare in b => eroare MARE in x
     - sistemul este SENSIBIL la perturbatii

=> Daca cond(A) este MIC (aproape de 1):
     - erori mici in b => erori mici in x
     - sistemul este STABIL

EXEMPLU CLASIC DE MATRICE SLAB CONDITIONATA:
  A = [[1, 1], [1, 1.0001]]
  Randurile sunt aproape identice => det(A) aproape zero => instabila!
"""

import numpy as np

# -----------------------------------------------------------------------
# Datele problemei
# -----------------------------------------------------------------------
A_slab = np.array([
    [1,      1     ],
    [1,      1.0001]
], dtype=float)

b_orig = np.array([2, 2.0001], dtype=float)   # vectorul original

print("=" * 60)
print("PROBLEMA 30 – Conditionarea unui sistem liniar")
print("=" * 60)

# -----------------------------------------------------------------------
# Calculam numarul de conditionare
# -----------------------------------------------------------------------
# np.linalg.cond calculeaza ||A|| * ||A^{-1}|| (norma 2 implicita)
cond = np.linalg.cond(A_slab)
print(f"\nMatricea A (slab conditionata):\n{A_slab}")
print(f"\nNumarul de conditionare: cond(A) = {cond:.2e}")
print("=> Un numar de conditionare MARE inseamna matrice SLAB conditionata!")

# -----------------------------------------------------------------------
# Solutia pentru b original
# -----------------------------------------------------------------------
x_orig = np.linalg.solve(A_slab, b_orig)
print(f"\nb original = {b_orig}")
print(f"Solutia x_orig = {x_orig}")

# -----------------------------------------------------------------------
# Perturbam b cu 0.1% si rezolvam din nou
# -----------------------------------------------------------------------
factor_perturb = 0.001                         # 0.1% perturbatie
delta_b = factor_perturb * b_orig              # perturbatia aplicata lui b
b_pert  = b_orig + delta_b                     # b perturbat

x_pert  = np.linalg.solve(A_slab, b_pert)     # solutia cu b perturbat

print(f"\n--- Perturbatie 0.1% in b ---")
print(f"b perturbat   = {b_pert}")
print(f"Solutia x_pert = {x_pert}")

# -----------------------------------------------------------------------
# Calculam erorile relative
# -----------------------------------------------------------------------
# Eroarea relativa in b: ||delta_b|| / ||b||
eroare_b = np.linalg.norm(delta_b) / np.linalg.norm(b_orig)

# Eroarea relativa in x: ||delta_x|| / ||x||
delta_x  = x_pert - x_orig
eroare_x = np.linalg.norm(delta_x) / np.linalg.norm(x_orig)

print(f"\n--- Analiza erorilor ---")
print(f"Eroare relativa in b: {eroare_b:.2e} ({eroare_b*100:.4f}%)")
print(f"Eroare relativa in x: {eroare_x:.2e} ({eroare_x*100:.4f}%)")
print(f"Factor de amplificare: {eroare_x/eroare_b:.2f}")
print(f"Numar de conditionare: {cond:.2e}")
print(f"=> Eroarea in x e de ~{eroare_x/eroare_b:.0f}x mai mare decat eroarea in b!")

# -----------------------------------------------------------------------
# Comparatie cu un sistem BINE conditionat
# -----------------------------------------------------------------------
A_bun = np.array([[4, 1], [1, 3]], dtype=float)
cond_bun = np.linalg.cond(A_bun)
b2 = np.array([5, 4], dtype=float)
x2_orig = np.linalg.solve(A_bun, b2)
delta_b2 = 0.001 * b2
x2_pert  = np.linalg.solve(A_bun, b2 + delta_b2)
eroare_x2 = np.linalg.norm(x2_pert - x2_orig) / np.linalg.norm(x2_orig)

print("\n" + "=" * 60)
print("COMPARATIE: Bine conditionat vs. Slab conditionat")
print("=" * 60)
print(f"  A_bun:  cond = {cond_bun:.2f}  => eroare relativa x: {eroare_x2:.2e}")
print(f"  A_slab: cond = {cond:.2e} => eroare relativa x: {eroare_x:.2e}")
print(f"\nCONCLUZIE: La aceeasi perturbatie de 0.1% in b,")
print(f"  sistemul slab conditionat produce o eroare de {eroare_x/eroare_x2:.0f}x mai mare!")