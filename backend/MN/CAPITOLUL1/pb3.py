# ============================================================
# PROBLEMA 3: Ordinea adunarii conteaza (b=10, t=4 cifre)
# Teorie in curs: Capitol 1 – "Erori de rotunjire si ordinea operatiilor"
#   In aritmetica cu precizie finita, adunarea numerelor mari cu mici
#   in ordine gresita duce la pierderea cifrelor mici.
# CERINTA: Într-un sistem cu b = 10 și t = 4 cifre semnificative, adunați: x1 = 0.2146, x2 = 3.175, x3 =
# 15.421, x4 = 176.86 în ordine crescătoare și descrescătoare.
# ============================================================

import math

# Functie care rotunjeste la t cifre semnificative (simuleaza t=4)
def rotunjeste(x, t=4):
    """Rotunjeste x la t cifre semnificative."""
    if x == 0:
        return 0
    d = math.floor(math.log10(abs(x)))  # gaseste ordinul de marime
    factor = 10 ** (t - 1 - d)          # factorul de scalare
    return round(x * factor) / factor   # rotunjeste si rescaleaza

numere = [0.2146, 3.175, 15.421, 176.86]  # cele 4 numere din problema

# Adunare in ordine DESCRESCATOARE (mare -> mic)
print("Ordine DESCRESCATOARE:")
suma_desc = 0.0
for x in sorted(numere, reverse=True):   # sortam descrescator
    suma_desc = rotunjeste(suma_desc + x) # adaugam si rotunjim la fiecare pas
    print(f"  + {x} -> {suma_desc}")
print(f"Suma descrescatoare (t=4): {suma_desc}")

# Adunare in ordine CRESCATOARE (mic -> mare)
print("\nOrdine CRESCATOARE:")
suma_cresc = 0.0
for x in sorted(numere):                  # sortam crescator
    suma_cresc = rotunjeste(suma_cresc + x)
    print(f"  + {x} -> {suma_cresc}")
print(f"Suma crescatoare   (t=4): {suma_cresc}")

print(f"\nValoarea exacta:        {sum(numere):.4f}")
print(f"Diferenta intre metode: {abs(suma_desc - suma_cresc):.4f}")