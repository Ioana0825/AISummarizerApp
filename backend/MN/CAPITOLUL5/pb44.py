import numpy as np

# ============================================================
# PROBLEMA 44 – Valori și vectori proprii (calcul analitic 2×2)
# Scop: calculăm λ din ecuația caracteristică det(A - λI) = 0
# Curs: Cap. "Valori proprii – Ecuația caracteristică" - paginile
# CERINTA: Calculați valorile și vectorii proprii ai matricei A = [[4,1],[1,3]] prin ecuația caracteristică.
#
# Pentru A = [[a,b],[c,d]]:
#   det(A - λI) = (a-λ)(d-λ) - b*c = 0
#   λ² - (a+d)λ + (ad - bc) = 0
#   => λ = [ trace ± sqrt(trace² - 4*det) ] / 2
# ============================================================

A = np.array([[4, 1],
              [1, 3]], dtype=float)

print("Matricea A =")
print(A)

# --- Calculul analitic al valorilor proprii ---
trace = A[0, 0] + A[1, 1]          # urma matricei: a + d
det   = A[0, 0]*A[1, 1] - A[0, 1]*A[1, 0]  # determinantul: ad - bc

print(f"\nTrace(A) = {trace}")
print(f"det(A)   = {det}")

discriminant = trace**2 - 4 * det
print(f"Discriminant = {discriminant}")

lambda1 = (trace + np.sqrt(discriminant)) / 2
lambda2 = (trace - np.sqrt(discriminant)) / 2

print(f"\nValorile proprii:")
print(f"  λ1 = (trace + √discriminant) / 2 = {lambda1}")
print(f"  λ2 = (trace - √discriminant) / 2 = {lambda2}")

# --- Calculul vectorilor proprii ---
# Pentru fiecare λ, rezolvăm (A - λI)v = 0
def vector_propriu(A, lam):
    """Găsim vectorul propriu pentru valoarea proprie lam.
    (A - lam*I)v = 0 => prima ecuatie: (a-lam)*v1 + b*v2 = 0
    Alegem v2 = 1, deci v1 = -b / (a - lam)
    """
    a, b = A[0, 0], A[0, 1]
    # Dacă (a - lam) ≠ 0, extragem v1 din prima ecuație
    if abs(a - lam) > 1e-10:
        v1 = -b / (a - lam)
        v = np.array([v1, 1.0])
    else:
        # Altfel extragem din a doua ecuație
        c, d = A[1, 0], A[1, 1]
        v2 = -c / (d - lam)
        v = np.array([1.0, v2])
    return v / np.linalg.norm(v)  # normalizăm la lungime 1

v1 = vector_propriu(A, lambda1)
v2 = vector_propriu(A, lambda2)

print(f"\nVectorii proprii (normalizați):")
print(f"  v1 (pentru λ1={lambda1:.4f}) = {v1}")
print(f"  v2 (pentru λ2={lambda2:.4f}) = {v2}")

# --- Verificare cu NumPy ---
vals, vecs = np.linalg.eig(A)
print(f"\n[Verificare NumPy] λ = {vals}")
print(f"[Verificare NumPy] Vectori proprii (coloane):\n{vecs}")

# --- Verificare Av = λv ---
print(f"\n[Verificare] A @ v1 = {A @ v1}")
print(f"             λ1*v1 = {lambda1 * v1}")