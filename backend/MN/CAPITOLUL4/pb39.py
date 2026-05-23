"""
PROBLEMA 39 - Diferentiere numerica prin diferente finite
CERINTA: Aproximați f'(x) și f''(x) pentru f(x) = sin(x) la x = π/4 prin diferențe finite centrate cu h = 0.1.
==========================================================
TEORIE (Curs - Capitol: Diferentiere Numerica):
  Nu avem formula analitica => aproximam derivatele cu valori in puncte vecine.

  DERIVATA INTAI - diferente finite CENTRATE (cea mai buna precizie):
      f'(x) ≈ [f(x+h) - f(x-h)] / (2h)
      Eroarea: O(h^2)  => dubland precizia, eroarea scade de 4 ori

  DERIVATA A DOUA - diferente finite centrate:
      f''(x) ≈ [f(x+h) - 2*f(x) + f(x-h)] / h^2
      Eroarea: O(h^2)

  Alte variante (mai putin precise):
      f'(x) ≈ [f(x+h) - f(x)] / h      (diferenta progresiva, eroare O(h))
      f'(x) ≈ [f(x) - f(x-h)] / h      (diferenta regresiva, eroare O(h))

Se cere: f(x) = sin(x) la x = π/4, h = 0.1
Valori exacte: f'(π/4) = cos(π/4) = √2/2 ≈ 0.70711
              f''(π/4) = -sin(π/4) = -√2/2 ≈ -0.70711
"""

import math

# -------------------------------------------------------
# PASUL 1: Definim functia si parametrii
# -------------------------------------------------------
def f(x):
    return math.sin(x)      # f(x) = sin(x)

x = math.pi / 4    # punctul de evaluare: π/4 ≈ 0.7854
h = 0.1            # pasul de diferentiere (mic => eroare mica)

print("=== PROBLEMA 39 - Diferentiere Numerica (Diferente Finite) ===")
print(f"Functia: f(x) = sin(x)")
print(f"Punct:   x = π/4 = {x:.6f}")
print(f"Pas:     h = {h}")
print()

# -------------------------------------------------------
# PASUL 2: Evaluam f in punctele necesare
# -------------------------------------------------------
f_plus  = f(x + h)    # f(x+h) = sin(π/4 + 0.1)
f_zero  = f(x)        # f(x)   = sin(π/4)
f_minus = f(x - h)    # f(x-h) = sin(π/4 - 0.1)

print(f"f(x-h) = f({x-h:.4f}) = {f_minus:.8f}")
print(f"f(x)   = f({x:.4f}) = {f_zero:.8f}")
print(f"f(x+h) = f({x+h:.4f}) = {f_plus:.8f}")
print()

# -------------------------------------------------------
# PASUL 3: Formula derivatei intai CENTRATE
# f'(x) ≈ [f(x+h) - f(x-h)] / (2*h)
# -------------------------------------------------------
d1_centrat = (f_plus - f_minus) / (2 * h)

# Pentru comparatie: diferenta progresiva (mai imprecisa)
d1_progresiv = (f_plus - f_zero) / h

# -------------------------------------------------------
# PASUL 4: Formula derivatei a doua CENTRATE
# f''(x) ≈ [f(x+h) - 2*f(x) + f(x-h)] / h^2
# -------------------------------------------------------
d2_centrat = (f_plus - 2 * f_zero + f_minus) / (h ** 2)

# -------------------------------------------------------
# PASUL 5: Valorile exacte (analitice)
# -------------------------------------------------------
d1_exact = math.cos(x)        # derivata sin(x) = cos(x)
d2_exact = -math.sin(x)       # derivata a 2-a a sin(x) = -sin(x)

# -------------------------------------------------------
# PASUL 6: Afisam rezultatele
# -------------------------------------------------------
print("--- Derivata intai f'(x) ---")
print(f"  Centrata:   [f(x+h)-f(x-h)]/(2h) = {d1_centrat:.8f}")
print(f"  Progresiva: [f(x+h)-f(x)]/h       = {d1_progresiv:.8f}")
print(f"  Exacta:     cos(π/4)              = {d1_exact:.8f}")
print(f"  Eroare centrata:   {abs(d1_centrat - d1_exact):.2e}  (O(h^2))")
print(f"  Eroare progresiva: {abs(d1_progresiv - d1_exact):.2e}  (O(h))")
print()

print("--- Derivata a doua f''(x) ---")
print(f"  Centrata:   [f(x+h)-2f(x)+f(x-h)]/h^2 = {d2_centrat:.8f}")
print(f"  Exacta:     -sin(π/4)                  = {d2_exact:.8f}")
print(f"  Eroare: {abs(d2_centrat - d2_exact):.2e}  (O(h^2))")