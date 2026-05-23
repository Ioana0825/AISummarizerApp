"""
PROBLEMA 23 – Eliminarea Gauss cu pivotare partiala – sistem 4x4
CERINTA: Rezolvati sistemul Ax = b cu:
A = [[4,1,-1,1],[1,5,2,0],[-1,2,6,1],[1,0,1,4]], b = [12, 8, 19, 11]
=================================================================
TEORIE (Curs: Capitol "Sisteme de Ecuatii Liniare – Metode Directe"):
  Vezi Algorithm 5 din curs: "Eliminarea Gauss cu pivotare partiala"

IDEEA PRINCIPALA:
  In loc sa lucram cu A si b separat, le LIPIM intr-o singura matrice extinsa:
       M = [A | b]  (matricea A cu coloana b adaugata la dreapta)

  Astfel, orice operatie pe un rand din A se aplica automat si pe b!

PASII (conform Algorithm 5 din curs):
  1. Formeaza matricea extinsa M <- [A | b]
  2. Pentru fiecare coloana i (pivot):
       a) Pivotare partiala: gaseste randul p cu |M[p][i]| maxim si
          schimba randul i cu randul p
       b) Eliminare: pentru fiecare rand k > i:
            m = M[k][i] / M[i][i]           <- factorul de eliminare
            M[k][i:] -= m * M[i][i:]        <- actualizeaza tot randul k
  3. Retrosubstitutie:
       x[n] = M[n][n+1] / M[n][n]           <- ultima necunoscuta
       x[i] = (M[i][n+1] - sum(M[i][j]*x[j], j=i+1..n)) / M[i][i]
"""

import numpy as np

# -----------------------------------------------------------------------
# Functia din curs – Eliminare Gauss cu pivotare partiala
# Foloseste matricea EXTINSA M = [A | b]
# -----------------------------------------------------------------------
def gauss_pivotare(A, b):
    """Eliminarea Gauss cu pivotare partiala."""

    n = len(b)                  # numarul de ecuatii / necunoscute

    # PASUL 1: Construim matricea extinsa M = [A | b]
    # np.hstack lipeste A si b (reshape(-1,1) transforma b din vector row in coloana)
    # Rezultat: M are n linii si n+1 coloane, ultima coloana fiind b
    Ab = np.hstack([A.astype(float), b.reshape(-1, 1).astype(float)])
    # Exemplu pentru sistemul nostru 4x4:
    # Ab = [ 4  1 -1  1 | 12 ]
    #      [ 1  5  2  0 |  8 ]
    #      [-1  2  6  1 | 19 ]
    #      [ 1  0  1  4 | 11 ]

    # PASUL 2: Eliminare cu pivotare – parcurgem fiecare coloana i
    for i in range(n):

        # --- Pivotare partiala (linia 3-4 din Algorithm 5) ---
        # Gasim randul cu elementul cel mai mare (in modul) in coloana i,
        # incepand de la randul i in jos: cautam max |Ab[i:, i]|
        # np.argmax returneaza pozitia relativa => adaugam i pentru pozitia absoluta
        max_row = i + np.argmax(np.abs(Ab[i:, i]))

        # Schimbam randul i cu randul max_row in TOATA matricea extinsa Ab
        # Astfel pivotul (cel mai mare element) ajunge pe diagonala
        Ab[[i, max_row]] = Ab[[max_row, i]]

        # --- Eliminare (liniile 5-10 din Algorithm 5) ---
        # Pentru fiecare rand k de sub pivotul curent (k > i):
        for k in range(i + 1, n):

            # Calculam factorul de eliminare: m = M[k][i] / M[i][i]
            # Acesta este numarul cu care inmultim randul pivot inainte de scadere
            m = Ab[k, i] / Ab[i, i]

            # Actualizam INTREG randul k (de la coloana i pana la sfarsit, inclusiv b)
            # Ab[k, i:] -= m * Ab[i, i:]  echivalent cu:
            # Ab[k][j] = Ab[k][j] - m * Ab[i][j]  pentru j = i, i+1, ..., n
            # Dupa aceasta operatie, Ab[k][i] devine 0 (elementul de sub pivot)
            Ab[k, i:] -= m * Ab[i, i:]

    # PASUL 3: Retrosubstitutie (liniile 13-16 din Algorithm 5)
    # Acum Ab este superior triunghiulara. Rezolvam de JOS in SUS.
    x = np.zeros(n)             # initializam vectorul solutie cu zerouri

    for i in range(n - 1, -1, -1):     # parcurgem de la randul n-1 la randul 0
        # Formula: x[i] = (M[i][n] - sum_{j=i+1}^{n-1} M[i][j]*x[j]) / M[i][i]
        # Ab[i, -1]   = ultimul element din randul i = termenul liber transformat
        # Ab[i, i+1:n] = coeficientii din randul i, dupa diagonala
        # x[i+1:n]    = solutiile deja calculate (de la pasii anteriori)
        x[i] = (Ab[i, -1] - np.dot(Ab[i, i+1:n], x[i+1:n])) / Ab[i, i]

    return x

# -----------------------------------------------------------------------
# Datele problemei
# -----------------------------------------------------------------------
A = np.array([[ 4,  1, -1,  1],
              [ 1,  5,  2,  0],
              [-1,  2,  6,  1],
              [ 1,  0,  1,  4]], dtype=float)

b = np.array([12, 8, 19, 11], dtype=float)

# -----------------------------------------------------------------------
# Rezolvam si afisam rezultatele
# -----------------------------------------------------------------------
print("=== Metoda Gauss cu pivotare partiala ===")
print(f"Matricea A:\n{A}\n")
print(f"Vectorul b: {b}\n")

x = gauss_pivotare(A, b)               # apelam functia si obtinem solutia

print(f"Solutia: x = {x}")
print(f"Verificare Ax = {A @ x}")      # A @ x trebuie sa fie egal cu b
print(f"Eroare: ||Ax - b|| = {np.linalg.norm(A @ x - b):.2e}")
# O eroare de ordinul 1e-15 inseamna practic zero (eroare numerica de masina)