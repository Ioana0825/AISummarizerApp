"""
PROBLEMA 34 - Interpolarea Newton cu diferente divizate
CERINTA: Construiți polinomul Newton de gradul 2 pentru: x = [0, 1, 2], f(x) = [1, 3, 7]. Calculați f(1.5).
=======================================================
TEORIE (Curs - Capitol: Interpolare si Aproximare):
  Polinomul Newton cu diferente divizate:

      P(x) = f[x0] + f[x0,x1]*(x-x0) + f[x0,x1,x2]*(x-x0)*(x-x1) + ...

  Diferentele divizate se calculeaza recursiv:
      f[xi]       = yi                          (ord. 0)
      f[xi,xi+1]  = (f[xi+1] - f[xi]) / (xi+1 - xi)   (ord. 1)
      f[xi,..,xk] = (f[xi+1,..,xk] - f[xi,..,xk-1]) / (xk - xi)  (ord. k)

  Avantaj fata de Lagrange: adaugarea unui nod nou nu recalculeaza totul!

Puncte: x=[0,1,2], f(x)=[1,3,7] => se cere f(1.5)
"""

# -------------------------------------------------------
# PASUL 1: Datele problemei (aceleasi ca la Lagrange pt comparatie)
# -------------------------------------------------------
x = [0, 1, 2]    # nodurile de interpolare
y = [1, 3, 7]    # valorile functiei in noduri
x_eval = 1.5     # punctul de evaluare

# -------------------------------------------------------
# PASUL 2: Construim tabelul diferentelor divizate
# -------------------------------------------------------
def diferente_divizate(x, y):
    """
    Construieste tabelul complet al diferentelor divizate.
    Returneaza lista coeficientilor Newton: f[x0], f[x0,x1], f[x0,x1,x2], ...
    """
    n = len(x)
    # Copiem valorile y in prima coloana a tabelului
    # tabel[i][j] = f[xi, xi+1, ..., xi+j]
    tabel = [yi for yi in y]   # coloana 0: f[xi] = yi

    # Lista coeficientilor Newton (primul element din fiecare coloana)
    coef = [tabel[0]]

    # Construim coloana j (diferente de ordin j)
    for j in range(1, n):
        tabel_nou = []
        for i in range(n - j):
            # Formula: f[xi,...,xi+j] = (f[xi+1,...,xi+j] - f[xi,...,xi+j-1]) / (xi+j - xi)
            val = (tabel[i + 1] - tabel[i]) / (x[i + j] - x[i])
            tabel_nou.append(val)
        tabel = tabel_nou         # actualizăm coloana curenta
        coef.append(tabel[0])     # primul element e coeficientul Newton

    return coef   # [f[x0], f[x0,x1], f[x0,x1,x2], ...]

# -------------------------------------------------------
# PASUL 3: Evaluam polinomul Newton in x_eval
# -------------------------------------------------------
def evalueaza_newton(coef, x_nodes, x):
    """
    Evalueaza P(x) prin schema Horner:
    P(x) = c0 + c1*(x-x0) + c2*(x-x0)*(x-x1) + ...
    """
    n = len(coef)
    rezultat = coef[n - 1]          # incepem cu ultimul coeficient

    # Parcurgem de la dreapta spre stanga (schema Horner)
    for i in range(n - 2, -1, -1):
        rezultat = rezultat * (x - x_nodes[i]) + coef[i]

    return rezultat

# -------------------------------------------------------
# PASUL 4: Calculam si afisam
# -------------------------------------------------------
coeficienti = diferente_divizate(x, y)

print("=== PROBLEMA 34 - Interpolare Newton (Diferente Divizate) ===")
print(f"Noduri x: {x}")
print(f"Valori y: {y}")
print()

# Afisam coeficientii Newton (diferentele divizate principale)
etichete = ["f[x0]", "f[x0,x1]", "f[x0,x1,x2]"]
for i, c in enumerate(coeficienti):
    print(f"  {etichete[i]} = {c:.6f}")

print()
# Forma explicita a polinomului
# P(x) = 1 + 2*(x-0) + 2*(x-0)*(x-1)
print("Forma polinomului Newton:")
print("  P(x) = 1 + 2*(x-0) + 2*(x-0)*(x-1)")

valoare = evalueaza_newton(coeficienti, x, x_eval)
print(f"\nP(1.5) = {valoare:.6f}")

# Comparatie cu Lagrange (trebuie sa fie identic)
print(f"Valoare exacta (2x^2+1): {2*x_eval**2 + 1:.6f}")