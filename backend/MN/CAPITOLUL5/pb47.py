import numpy as np

# ============================================================
# PROBLEMA 47 – Punct fix: divergență (analiza ρ(G') > 1)
# Scop: arătăm că rescrierea g1=√(4-y²), g2=1-eˣ NU converge
# Curs: Cap. "Metoda Punctului Fix pentru sisteme – condiția de convergență"
# CERINTA: Arătați că rescrierea g1(x,y) = √(4−y2), g2(x,y) = 1−ex nu converge (Analiza ρ(G') > 1).
#
# Condiția de convergență: raza spectrală ρ(G') < 1
# unde G' = Jacobianul funcției de iterație g = [g1, g2]
# Dacă ρ(G') > 1 → metodă DIVERGENTĂ
# ============================================================

def g(v):
    """Funcția de iterație la punct fix:
    g1(x,y) = sqrt(4 - y²)
    g2(x,y) = 1 - e^x
    Derivată din F1=x²+y²-4=0 → x=√(4-y²)
                 F2=e^x+y-1=0 → y=1-e^x
    """
    x, y = v
    return np.array([np.sqrt(4 - y**2),
                     1 - np.exp(x)])

def jacobian_g(x, y):
    """Jacobianul analitic al lui g la (x, y):
    ∂g1/∂x = 0,           ∂g1/∂y = -y / √(4-y²)
    ∂g2/∂x = -e^x,        ∂g2/∂y = 0
    """
    dg1_dx = 0
    dg1_dy = -y / np.sqrt(4 - y**2)
    dg2_dx = -np.exp(x)
    dg2_dy = 0
    return np.array([[dg1_dx, dg1_dy],
                     [dg2_dx, dg2_dy]])

# --- Soluția adevărată a sistemului (pentru referință) ---
# x ≈ -1.8163, y ≈ 0.8374 (din problema 46)
x_sol, y_sol = -1.81626, 0.83737

print("Analiza convergenței metodei punctului fix:")
print(f"g1(x,y) = sqrt(4 - y²)")
print(f"g2(x,y) = 1 - e^x\n")

# --- Calculul Jacobianului G' la soluție ---
G = jacobian_g(x_sol, y_sol)
print("Jacobianul G' la soluție:")
print(G)

# --- Raza spectrală: maximul valorilor proprii în modul ---
vals = np.linalg.eigvals(G)
rho = max(abs(vals))   # raza spectrală ρ(G')

print(f"\nValorile proprii ale G': {vals}")
print(f"Raza spectrală ρ(G') = {rho:.4f}")

if rho < 1:
    print("→ ρ(G') < 1: metoda CONVERGE ✓")
else:
    print(f"→ ρ(G') = {rho:.4f} > 1: metoda DIVERGE ✗")

# --- Demonstrație practică: iterații care diverge ---
print("\n--- Simulare iterații (pornind din (1.0, 1.5)) ---")
print(f"{'Iter':>5}  {'x':>12}  {'y':>12}")
print("-" * 35)

v = np.array([1.0, 1.5])
print(f"{0:>5}  {v[0]:>12.6f}  {v[1]:>12.6f}")

for i in range(1, 8):
    try:
        v = g(v)    # aplicăm iterația
        print(f"{i:>5}  {v[0]:>12.6f}  {v[1]:>12.6f}")
        # Dacă valorile explodează, oprim
        if np.any(np.isnan(v)) or np.any(np.abs(v) > 1e10):
            print("       → DIVERGENȚĂ (nan sau valori foarte mari)")
            break
    except Exception as e:
        print(f"       → EROARE la iterația {i}: {e} (ieșire din domeniu)")
        break

print("\nConcluzie: rescrierea g1=√(4-y²), g2=1-eˣ este INSTABILĂ numerică.")
print("Se preferă metoda Newton-Raphson sau Broyden (problemele 21, 46).")