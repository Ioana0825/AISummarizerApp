"""
PROBLEMA 38 - Cuadratura Gauss-Legendre (2 puncte)
CERINTA: Aproximați ∫−11 ex dx prin cuadratura Gauss-Legendre cu 2 puncte de integrare.
==================================================
TEORIE (Curs - Capitol: Integrare Numerica - Cuadratura Gaussiana):
  Ideea: alegem OPTIM atat nodurile cat si coeficientii (nu echidistant!)
  pentru a maximiza precizia cu putine evaluari.

  Pentru 2 puncte pe intervalul [-1, 1]:
      ∫_{-1}^{1} f(t) dt ≈ w1*f(t1) + w2*f(t2)

  Nodurile si ponderile (tabulate, din teoria polinoamelor Legendre):
      t1 = -1/√3 ≈ -0.57735    w1 = 1
      t2 = +1/√3 ≈ +0.57735    w2 = 1

  Precizia: exacta pentru polinoame de grad <= 2*n-1 = 3

  TRANSFORMARE de interval [a,b] -> [-1,1]:
      x = (a+b)/2 + (b-a)/2 * t
      dx = (b-a)/2 * dt

  Deci:
      ∫_a^b f(x)dx = (b-a)/2 * ∫_{-1}^{1} f((a+b)/2 + (b-a)/2 * t) dt

Se cere: ∫_{-1}^{1} e^x dx   (intervalul e deja [-1,1])
Valoarea exacta: e^1 - e^{-1} = e - 1/e ≈ 2.35040
"""

import math

# -------------------------------------------------------
# PASUL 1: Definim functia
# -------------------------------------------------------
def f(x):
    return math.exp(x)   # f(x) = e^x

# -------------------------------------------------------
# PASUL 2: Nodurile si ponderile Gauss-Legendre (2 puncte, tabulate)
# -------------------------------------------------------
# Acestea sunt FIXE pentru 2 puncte - se memoreaza sau se cauta in tabel
t1 = -1.0 / math.sqrt(3)   # ≈ -0.57735  (primul nod)
t2 = +1.0 / math.sqrt(3)   # ≈ +0.57735  (al doilea nod)
w1 = 1.0                    # ponderea primului nod
w2 = 1.0                    # ponderea celui de-al doilea nod

print("=== PROBLEMA 38 - Cuadratura Gauss-Legendre (2 puncte) ===")
print(f"Noduri Gauss:   t1={t1:.6f}, t2={t2:.6f}")
print(f"Ponderi Gauss:  w1={w1:.4f}, w2={w2:.4f}")
print()

# -------------------------------------------------------
# PASUL 3: Aplicam cuadratura pe [-1, 1]
# Formula: ∫_{-1}^{1} f(t)dt ≈ w1*f(t1) + w2*f(t2)
# -------------------------------------------------------
# Integrala pe [-1,1] => nu avem nevoie de transformare de interval
a = -1
b = 1

# Evaluam f in nodurile Gauss (dupa transformarea de interval daca e nevoie)
# Transformare: x = (a+b)/2 + (b-a)/2 * t = 0 + 1*t = t (pe [-1,1] raman t)
x1 = (a + b) / 2 + (b - a) / 2 * t1   # = t1 (pe [-1,1])
x2 = (a + b) / 2 + (b - a) / 2 * t2   # = t2

print("Evaluarea functiei in nodurile Gauss:")
print(f"  f(t1={x1:.6f}) = e^{x1:.6f} = {f(x1):.6f}")
print(f"  f(t2={x2:.6f}) = e^{x2:.6f} = {f(x2):.6f}")
print()

# Aplicam formula Gauss-Legendre (cu factorul (b-a)/2 pt schimbare de interval)
factor = (b - a) / 2    # = 1 pentru [-1,1]
rezultat = factor * (w1 * f(x1) + w2 * f(x2))

# -------------------------------------------------------
# PASUL 4: Comparatie cu valoarea exacta
# -------------------------------------------------------
exacta = math.exp(1) - math.exp(-1)    # e - 1/e ≈ 2.35040
eroare = abs(rezultat - exacta)

print(f"Rezultat Gauss-Legendre: {rezultat:.8f}")
print(f"Valoarea exacta:         {exacta:.8f}")
print(f"Eroarea absoluta:        {eroare:.2e}")
print()
print("OBSERVATIE: Cu doar 2 evaluari ale functiei, eroarea e mai mica")
print("decat Trapezul cu 4 subintervale! Aceasta e puterea Gauss.")