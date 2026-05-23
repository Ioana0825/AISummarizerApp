"""
PROBLEMA 13 - Metoda Bisectiei: f(x) = x*e^x - 2 = 0 pe [0, 1]
================================================================
Capitol din curs: "Metode numerice pentru ecuatii neliniare"
                  Sectiunea: Metoda Bisectiei
CERINTA: Găsiți rădăcina ecuației f(x) = xe^x − 2 = 0 pe intervalul [0, 1] cu ε = 10−6 prin metoda bisecției.

TEORIE:
  Daca f(a)*f(b) < 0, exista o radacina in [a, b] (Teorema lui Bolzano).
  La fiecare pas, intervalul se injumatateste: c = (a + b) / 2
  Numarul de iteratii: n >= log2((b - a) / epsilon)

  Algoritm:
    1. Calculeaza c = (a + b) / 2  (mijlocul intervalului)
    2. Daca f(a)*f(c) < 0, radacina e in [a, c] => b = c
       Altfel, radacina e in [c, b] => a = c
    3. Repeta pana cand (b - a)/2 < epsilon
"""

import numpy as np  # Biblioteca pentru calcule matematice (exp, log2 etc.)


def f(x):
    """
    Functia de rezolvat: f(x) = x * e^x - 2
    Cautam x astfel incat f(x) = 0
    """
    return x * np.exp(x) - 2  # np.exp(x) calculeaza e^x


# --- Parametrii problemei ---
a = 0.0    # Capatul stang al intervalului
b = 1.0    # Capatul drept al intervalului
eps = 1e-6  # Precizia dorita (epsilon = 10^-6)
iteratie = 0  # Contorul de iteratii

# --- Verificam Teorema Bolzano: f(a) si f(b) trebuie sa aiba semne OPUSE ---
# Daca f(a)*f(b) < 0 => semne diferite => exista radacina in [a, b]
print(f"f(a=0) = {f(a):.4f}")
print(f"f(b=1) = {f(b):.4f}")
print(f"f(a)*f(b) = {f(a)*f(b):.4f}  (negativ => radacina garantata in [0,1])")
print()

# --- Formula pentru numarul teoretic de iteratii ---
# Din: (b-a)/2^n <= eps => n >= log2((b-a)/eps)
n_teoretic = np.ceil(np.log2((b - a) / eps))  # np.ceil = rotunjire in sus
print(f"Numar teoretic de iteratii: n >= log2({b-a}/{eps}) = {n_teoretic:.0f}")
print()

# --- Tabel de iteratii ---
print(f"{'Iter':>4} | {'a':>10} | {'b':>10} | {'c=(a+b)/2':>10} | {'f(c)':>12}")
print("-" * 57)

# --- Bucla principala a bisectiei ---
while (b - a) / 2 > eps:     # Continuam cat timp jumatatea intervalului > eps
    c = (a + b) / 2           # Mijlocul intervalului [a, b]
    iteratie += 1

    print(f"{iteratie:>4} | {a:>10.6f} | {b:>10.6f} | {c:>10.6f} | {f(c):>12.2e}")

    if f(c) == 0:              # Caz ideal: am nimerit exact radacina
        break
    elif f(a) * f(c) < 0:     # Radacina e in [a, c] => mutam b la c
        b = c
    else:                      # Radacina e in [c, b] => mutam a la c
        a = c

# --- Rezultat final ---
print(f"\nRadacina gasita: x = {c:.8f}")
print(f"Numar iteratii:  {iteratie}")
print(f"Verificare:      f({c:.6f}) = {f(c):.2e}  (aproape de 0 ✓)")