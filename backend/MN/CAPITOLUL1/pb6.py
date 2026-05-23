# ============================================================
# PROBLEMA 6: Erori de trunchiere - seria Taylor pentru e
# Teorie in curs: Capitol 1 – "Erori de trunchiere"
#   Seria Taylor: e = 1 + 1/1! + 1/2! + 1/3! + ... (infiniti termeni)
#   Daca oprim dupa N termeni, comitem o eroare de trunchiere.
#   Cu cat N e mai mare, cu atat eroarea scade.
# CERINTA: Aproximați e = 2.71828... adunând primii N termeni din seria Taylor: e = 1 + 1/1! + 1/2! + 1/3! +
# ...
# Calculați eroarea absolută pentru N = 1, 2, 3, 4, 5 termeni.
# ============================================================

import math

e_exact = math.e   # valoarea exacta a lui e = 2.71828...

print(f"{'N':>4} | {'Aproximare e':>15} | {'Eroare absoluta':>15}")
print("-" * 42)

for N in range(1, 6):   # N = numarul de termeni din suma
    # Calculam suma: 1/0! + 1/1! + ... + 1/(N-1)!
    suma = sum(1/math.factorial(k) for k in range(N))   # suma primilor N termeni
    eroare = abs(e_exact - suma)                         # eroarea de trunchiere

    print(f"{N:>4} | {suma:>15.10f} | {eroare:>15.2e}")

print()
print("Observatie: cu fiecare termen adaugat, eroarea scade de ~N ori.")