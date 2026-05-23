"""
PROBLEMA 18 - Comparatie metode pentru f(x) = x*e^x - 2 = 0
=============================================================
Capitol din curs: "Metode numerice pentru ecuatii neliniare"
                  Sectiunea: Comparatie metode, Ordinul de convergenta

CERINTA: Comparați toate metodele de rezolvare a ecuației f(x) = xex − 2 = 0 și f(x) = cos(x) − x = 0.

SCOP:
  Comparam Bisectia, Secanta si Newton-Raphson pe aceeasi ecuatie
  si masuram: numarul de iteratii, eroarea finala si viteza de convergenta.

ORDINUL DE CONVERGENTA:
  Bisectie:      p = 1  (liniar)  => eroarea se injumatateste la fiecare pas
  Secanta:       p ≈ 1.618 (supraliniar, numarul de aur)
  Newton-Raphson:p = 2  (patratic) => eroarea se patrateaza la fiecare pas
"""

import numpy as np  # Biblioteca pentru calcule matematice


# =====================================================================
# Definim functia si derivata ei
# =====================================================================

def f(x):
    """f(x) = x*e^x - 2  (ecuatia de rezolvat)"""
    return x * np.exp(x) - 2

def df(x):
    """f'(x) = e^x*(1+x)  (derivata, necesara pentru Newton)"""
    return np.exp(x) * (1 + x)


# =====================================================================
# METODA 1: BISECTIA
# Injumatatim intervalul la fiecare pas
# =====================================================================

def metoda_bisectie(f, a, b, eps=1e-6):
    """
    Implementarea bisectiei.
    Returneaza: (radacina, numar_iteratii, istoric_erori)
    """
    erori = []   # Lista pentru a salva eroarea la fiecare iteratie
    n = 0        # Contorul de iteratii

    while (b - a) / 2 > eps:
        c = (a + b) / 2         # Mijlocul intervalului
        n += 1
        erori.append(abs(f(c))) # Salvam |f(c)| ca masura a erorii

        if f(a) * f(c) < 0:    # Radacina in [a, c]
            b = c
        else:                    # Radacina in [c, b]
            a = c

    return (a + b) / 2, n, erori


# =====================================================================
# METODA 2: SECANTA
# Aproximam derivata cu raportul diferentelor
# =====================================================================

def metoda_secanta(f, x0, x1, eps=1e-6, max_iter=50):
    """
    Implementarea metodei secantei.
    Formula: x2 = x1 - f(x1)*(x1-x0)/(f(x1)-f(x0))
    Returneaza: (radacina, numar_iteratii, istoric_erori)
    """
    erori = []

    for i in range(max_iter):
        # Formula secantei: inlocuim f'(x) cu diferenta finita
        x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
        erori.append(abs(f(x2)))

        if abs(x2 - x1) < eps:    # Criteriu de oprire
            return x2, i + 1, erori

        x0, x1 = x1, x2           # Actualizam cele doua puncte

    return x2, max_iter, erori


# =====================================================================
# METODA 3: NEWTON-RAPHSON
# Folosim derivata exacta f'(x)
# =====================================================================

def metoda_newton(f, df, x0, eps=1e-6, max_iter=50):
    """
    Implementarea Newton-Raphson.
    Formula: x_nou = x - f(x)/f'(x)
    Returneaza: (radacina, numar_iteratii, istoric_erori)
    """
    erori = []

    for i in range(max_iter):
        # Formula Newton: tangenta la curba => intersectie cu Ox
        x1 = x0 - f(x0) / df(x0)
        erori.append(abs(f(x1)))

        if abs(x1 - x0) < eps:    # Criteriu de oprire
            return x1, i + 1, erori

        x0 = x1                    # Actualizam x

    return x1, max_iter, erori


# =====================================================================
# RULAM TOATE METODELE SI COMPARAM
# =====================================================================

r_bis, n_bis, e_bis = metoda_bisectie(f, 0, 1)
r_sec, n_sec, e_sec = metoda_secanta(f, 0, 1)
r_new, n_new, e_new = metoda_newton(f, df, 1.0)

# --- Tabel comparativ ---
print("=" * 65)
print("COMPARATIE METODE pentru f(x) = x*e^x - 2 = 0, eps = 1e-6")
print("=" * 65)
print(f"\n{'Metoda':<20} | {'Radacina':>12} | {'Iteratii':>8} | {'|f(x*)| final':>14}")
print("-" * 62)
print(f"{'Bisectie':<20} | {r_bis:>12.8f} | {n_bis:>8} | {abs(f(r_bis)):>14.2e}")
print(f"{'Secanta':<20} | {r_sec:>12.8f} | {n_sec:>8} | {abs(f(r_sec)):>14.2e}")
print(f"{'Newton-Raphson':<20} | {r_new:>12.8f} | {n_new:>8} | {abs(f(r_new)):>14.2e}")

# --- Evolutia erorii (primele iteratii) ---
print(f"\n--- Evolutia erorii |f(x)| la primele iteratii ---")
print(f"{'Iter':>4} | {'Bisectie':>12} | {'Secanta':>12} | {'Newton':>12}")
print("-" * 48)
max_afisare = max(len(e_bis), len(e_sec), len(e_new))
for i in range(min(max_afisare, 8)):
    b_val = f"{e_bis[i]:.2e}" if i < len(e_bis) else "     -      "
    s_val = f"{e_sec[i]:.2e}" if i < len(e_sec) else "     -      "
    n_val = f"{e_new[i]:.2e}" if i < len(e_new) else "     -      "
    print(f"{i+1:>4} | {b_val:>12} | {s_val:>12} | {n_val:>12}")

# --- Concluzii ---
print(f"""
CONCLUZII:
  Bisectie ({n_bis} iteratii):
    + Mereu converge (daca f(a)*f(b) < 0)
    + Simplu de implementat
    - Cel mai lent (convergenta liniara)

  Secanta ({n_sec} iteratii):
    + Nu necesita derivata f'(x)
    + Mai rapid ca bisectia
    - Poate diverge in cazuri rare

  Newton-Raphson ({n_new} iteratii):
    + CEL MAI RAPID (convergenta patratica)
    - Necesita derivata f'(x) calculata analitic
    - Poate diverge daca x0 e ales prost
""")