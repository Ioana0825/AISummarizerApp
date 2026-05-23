# ============================================================
# PROBLEMA 12: Reprezentarea lui 0.1 in baza 2 (IEEE 754)
# Teorie in curs: Capitol 1 – "Reprezentarea IEEE 754" si "Erori de baza"
#   0.1 in baza 10 nu are reprezentare EXACTA in baza 2:
#   0.1 = 0.0001100110011... (binar, se repeta la infinit)
#   IEEE 754 double stocheaza cea mai apropiata valoare reprezentabila,
#   introducand o eroare mica dar inevitabila.
# CERINTA: Reprezentați numărul 0.1 în baza 2 (IEEE 754 double) și determinați eroarea față de valoarea
# exactă.
# ============================================================

import struct                    # pentru a inspecta bitii din memorie
from decimal import Decimal, getcontext
getcontext().prec = 30

x = 0.1   # valoarea stocata efectiv in calculator

# 1. Afisam valoarea stocata cu multe zecimale
print(f"Valoarea stocata de calculator:")
print(f"  0.1 = {x:.55f}")   # vedem ca nu e exact 0.1

# 2. Convertim manual 0.1 in baza 2 (algoritmul inmultirii cu 2)
print("\nConversia 0.1 din baza 10 in baza 2:")
val  = 0.1
biti = []
for i in range(20):      # calculam primii 20 biti dupa virgula binara
    val *= 2             # inmultim cu 2
    bit = int(val)       # partea intreaga (0 sau 1) = urmatorul bit
    biti.append(bit)
    val -= bit           # retinem numai fractia, continuam
print(f"  0.1 (baza 2) = 0.{''.join(map(str, biti))}...")
print(f"  (sirul 0011 se repeta la infinit -> nu are reprezentare exacta!)")

# 3. Inspectam bitii IEEE 754 stocati in memorie
octeti       = struct.pack('d', x)                         # impachetam double (8 bytes)
sir_biti     = ''.join(f'{b:08b}' for b in octeti)         # convertim la sir de biti
sir_biti_be  = sir_biti[::-1]                              # little-endian -> big-endian

print(f"\nStructura IEEE 754 double (64 biti):")
print(f"  Semn (1 bit):      {sir_biti_be[0]}          (0=pozitiv)")
print(f"  Exponent (11 biti):{sir_biti_be[1:12]}  = {int(sir_biti_be[1:12],2)-1023} (dupa scaderea bias-ului 1023)")
print(f"  Mantisa (52 biti): {sir_biti_be[12:]}")

# 4. Calculam eroarea de reprezentare
eroare = Decimal(0.1) - Decimal(1) / Decimal(10)   # eroarea exacta (cu Decimal)
print(f"\nEroarea de reprezentare IEEE 754:")
print(f"  = {eroare:.3e}")
print(f"  Adica ~5.55e-18, de ~18 ori mai mica decat cel mai mic float64 relativ (eps~2.2e-16)")