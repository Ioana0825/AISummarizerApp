# ============================================================
# PROBLEMA 11: Precizie extinsa - 2^200 cu float64 vs Decimal
# Teorie in curs: Capitol 1 – "Overflow si precizie extinsa"
#   float64: ~15-16 cifre semnificative, chiar daca numarul e reprezentabil
#   Decimal: precizie arbitrara => calculeaza exact toate cele ~60 cifre
#   int Python: precizie nelimitata nativa (referinta exacta)
# CERINTA: Calculați 2^200 cu precizie standard (float64) și cu precizie arbitrară (Decimal). Comparați.
# ============================================================

from decimal import Decimal, getcontext

getcontext().prec = 70   # 70 cifre pentru Decimal (2^200 are ~60 cifre)

val_float   = 2.0 ** 200          # float64: aproximat (doar ~16 cifre exacte)
val_decimal = Decimal(2) ** 200   # Decimal: exact (70 cifre)
val_exact   = 2 ** 200            # int Python: exact (referinta)

print(f"float64:  2^200 = {val_float:.6e}")
print(f"Decimal:  2^200 = {val_decimal}")
print(f"Exact:    2^200 = {val_exact}")

# Comparam ca siruri de caractere sa vedem de unde difera cifrele
float_str = f"{val_float:.0f}"
dec_str   = str(int(val_decimal))
exact_str = str(val_exact)

print(f"\nFloat   (primele 20 cifre): {float_str[:20]}...")
print(f"Decimal (primele 20 cifre): {dec_str[:20]}...")
print(f"Exact   (primele 20 cifre): {exact_str[:20]}...")

# Gasim prima pozitie unde float difera de valoarea exacta
prima_diferenta = next(
    (i for i, (a, b) in enumerate(zip(float_str, exact_str)) if a != b),
    "nicio"
)
print(f"\nFloat vs exact: prima diferenta la pozitia {prima_diferenta}")
print("=> float are doar ~16 cifre corecte din cele 61 ale lui 2^200")