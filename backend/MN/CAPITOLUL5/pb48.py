import numpy as np

# ============================================================
# PROBLEMA 48 – Metoda QR pentru valorile proprii
# Scop: calculăm TOATE valorile proprii ale unei matrice simetrice
# Curs: Cap. "Metoda QR – algoritm iterativ pentru valori proprii"
# CERINTA: Descrieți metoda QR pentru calculul tuturor valorilor proprii ale unei matrice simetrice A.
#
# Algoritmul:
#   1. Pornim cu A0 = A
#   2. La fiecare pas: factorizăm Ak = Qk * Rk (QR descompunere)
#   3. Calculăm A_(k+1) = Rk * Qk  (ordine inversată!)
#   4. Matricea converge spre o matrice diagonală (valori proprii pe diag)
#
# Proprietate cheie: Ak și A0 au aceleași valori proprii (matrice similare)
# ============================================================

# Matricea simetrică de test (are valori proprii reale)
A = np.array([[4.0, 1.0, 0.5],
              [1.0, 3.0, 0.5],
              [0.5, 0.5, 2.0]])

print("Metoda QR pentru A =")
print(A)

# Valorile proprii exacte (pentru verificare)
vals_exacte = np.linalg.eigvalsh(A)   # eigvalsh = pentru matrice simetrice
print(f"\nValori proprii exacte (NumPy): {sorted(vals_exacte, reverse=True)}")

# --- Algoritmul QR iterativ ---
max_iter = 100
tol = 1e-8

Ak = A.copy()

print(f"\n{'Iter':>5}  {'Diag(Ak) (aprox. valori proprii)':>45}  {'Eroare max':>12}")
print("-" * 70)

for k in range(max_iter):
    # Pasul 1: factorizare QR a matricei curente Ak = Qk * Rk
    # Q = matrice ortogonală, R = matrice superior triunghiulară
    Q, R = np.linalg.qr(Ak)

    # Pasul 2: formăm noua matrice A_(k+1) = Rk * Qk (inversăm ordinea!)
    Ak = R @ Q

    # Elementele de pe diagonală converg spre valorile proprii
    diag = np.diag(Ak)

    # Calculăm eroarea față de valorile exacte (sortate descrescător)
    vals_sortate = sorted(diag, reverse=True)
    eroare = max(abs(np.array(vals_sortate) - np.array(sorted(vals_exacte, reverse=True))))

    if k < 5 or k % 10 == 0 or eroare < tol:
        print(f"{k+1:>5}  {vals_sortate}  {eroare:>12.2e}")

    # Criteriu de oprire: elementele sub-diagonale devin neglijabile
    # (matricea e aproape diagonală)
    sub_diag = np.sum(np.abs(Ak - np.diag(diag)))
    if sub_diag < tol:
        print(f"\nConvergență la iterația {k+1} (sub-diag = {sub_diag:.2e})")
        break

print(f"\nMatricea finală Ak (aproape diagonală):")
print(np.round(Ak, 6))

print(f"\n>>> Valorile proprii găsite (diagonala):   {sorted(np.diag(Ak), reverse=True)}")
print(f">>> Valorile proprii exacte (NumPy):       {sorted(vals_exacte, reverse=True)}")