# ============================================================
# PROBLEMA 2: Precizia float32 vs float64 pentru 1/3
# Teorie in curs: Capitol 1 – "Tipuri de reprezentare in virgula mobila"
#   float32 (simpla precizie): ~7 cifre semnificative
#   float64 (dubla precizie): ~15-16 cifre semnificative
# CERINTA: Comparați precizia calculului 1/3 în reprezentare simplă (float32) și dublă (float64).
# ============================================================

import numpy as np  # numpy ne da acces la float32 si float64

val32 = np.float32(1) / np.float32(3)   # calculam 1/3 in simpla precizie
val64 = np.float64(1) / np.float64(3)   # calculam 1/3 in dubla precizie
exact = 1/3                              # Python foloseste float64 implicit

print(f"float32 (1/3): {val32:.20f}")
print(f"float64 (1/3): {val64:.20f}")
print(f"exact   (1/3): {exact:.20f}")
print(f"Eroare float32: {abs(float(val32) - exact):.2e}")   # ~9.93e-9
print(f"Eroare float64: {abs(float(val64) - exact):.2e}")   # ~1.11e-17