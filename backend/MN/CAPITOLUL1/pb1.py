# ============================================================
# PROBLEMA 1: 0.1 + 0.2 != 0.3 in virgula mobila
# Teorie in curs: Capitol 1 – "Reprezentarea in virgula mobila"
#   Motivul: 0.1 si 0.2 nu au reprezentare EXACTA in baza 2 (binar),
#   deci se acumuleaza o mica eroare de rotunjire.
# CERINTA:Demonstrați că operația 0.1 + 0.2 în calculator nu produce exact 0.3, datorită reprezentării
# binare finite.
# ============================================================

a = 0.1          # 0.1 nu e exact in binar -> se stocheaza aproximat
b = 0.2          # la fel si 0.2
suma = a + b     # suma lor nu e exact 0.3

print(f"0.1 = {a:.20f}")         # afisam 20 zecimale ca sa vedem eroarea ascunsa
print(f"0.2 = {b:.20f}")
print(f"0.1 + 0.2 = {suma:.20f}")
print(f"0.3       = {0.3:.20f}")
print(f"Sunt egale? {suma == 0.3}")                         # False!
print(f"Diferenta (eroarea): {abs(suma - 0.3):.2e}")        # ~5.55e-17