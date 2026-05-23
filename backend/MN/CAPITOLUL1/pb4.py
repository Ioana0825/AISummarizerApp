# ============================================================
# PROBLEMA 4: Adunarea in virgula mobila (b=10, t=6 cifre)
# Teorie in curs: Capitol 1 – "Aritmetica in virgula mobila"
#   Pasii: aliniere exponenti -> adunare mantise -> normalizare -> rotunjire
#   y are exponenta mai mare, deci x trebuie "aliniat", pierzand cifre mici.
# CERINTA: Adunați x = 4.156832 și y = 246.548 în sistemul cu baza b = 10, t = 6 cifre.
# ============================================================

x = 4.156832   # numarul mai mic
y = 246.548    # numarul mai mare

# Reprezentam cu 6 cifre semnificative (simuleaza sistemul t=6)
x_6 = float(f"{x:.6g}")       # .6g = 6 cifre semnificative
y_6 = float(f"{y:.6g}")

suma = x_6 + y_6               # adunarea propriu-zisa
suma_6 = float(f"{suma:.6g}")  # rotunjim rezultatul la 6 cifre

print(f"x rotunjit la 6 cifre: {x_6}")
print(f"y rotunjit la 6 cifre: {y_6}")
print(f"Suma inainte de rotunjire: {suma}")
print(f"Suma rotunjita la 6 cifre: {suma_6}")
print(f"Valoarea exacta:           {x + y}")
print(f"Eroarea de rotunjire:      {abs(suma_6 - (x + y)):.2e}")