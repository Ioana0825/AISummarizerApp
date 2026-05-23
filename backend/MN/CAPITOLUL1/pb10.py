# ============================================================
# PROBLEMA 10: Stabilitate numerica - (1/3)*3 == 1 ?
# Teorie in curs: Capitol 1 – "Aritmetica cu precizie arbitrara"
#   float64: ~15-16 cifre -> (1/3)*3 poate sau nu poate fi exact 1
#   Decimal: precizie configurabila -> arata mai clar eroarea acumulata
# CERINTA: Calculați x = 1/3 și verificați dacă (1/3)·3 == 1 în aritmetică float și Decimal (50 cifre).
# ============================================================

from decimal import Decimal, getcontext

getcontext().prec = 50   # setam 50 cifre de precizie pentru Decimal

# --- Calculul cu float standard Python (float64) ---
treime_float   = 1 / 3               # 1/3 in float64 (aproximat binar)
rezultat_float = treime_float * 3    # inmultim cu 3

print(f"float:   1/3        = {treime_float:.20f}")
print(f"float:   (1/3)*3    = {rezultat_float:.20f}")
print(f"float:   (1/3)*3 == 1? {rezultat_float == 1}")   # True (compensare fericita)

# --- Calculul cu Decimal (50 cifre) ---
treime_decimal   = Decimal(1) / Decimal(3)   # 1/3 cu 50 cifre
rezultat_decimal = treime_decimal * 3        # inmultim cu 3

print(f"\nDecimal: 1/3        = {treime_decimal}")
print(f"Decimal: (1/3)*3    = {rezultat_decimal}")
print(f"Decimal: (1/3)*3 == 1? {rezultat_decimal == 1}")  # False (eroarea e vizibila)

print()
print("Observatie: float 'compenseaza' eroarea accidental,")
print("dar Decimal cu 50 cifre arata ca (1/3)*3 nu e exact 1.")