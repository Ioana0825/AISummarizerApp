import numpy as np

# ============================================================
# PROBLEMA 43 – Metoda Puterii
# Scop: găsim cea mai mare valoare proprie (în modul) a unei matrice
# Curs: Cap. "Valori proprii – Metoda Puterii" - paginile 185-189
# Idee: înmulțim repetat A*v și normalizăm → vectorul converge
#       spre vectorul propriu dominant, iar raportul dă valoarea proprie
# CERINTA: Găsiți cea mai mare valoare proprie (în modul) a matricei A = [[2,1],[1,2]] prin metoda puterii,
# start v0=(1,0).
# ============================================================

# --- Datele problemei ---
A = np.array([[2, 1],
              [1, 2]], dtype=float)

v = np.array([1, 0], dtype=float)  # vectorul de start v0

tol = 1e-8       # toleranța de convergență
max_iter = 100   # număr maxim de iterații

print("Metoda Puterii pentru A =")
print(A)
print(f"\nVector start v0 = {v}\n")
print(f"{'Iter':>5}  {'lambda (val proprie)':>22}  {'v (vector propriu)':>25}")
print("-" * 65)

lambda_vechi = 0.0

for i in range(max_iter):
    # Pasul 1: înmulțim matricea A cu vectorul curent
    # Aceasta "amplifică" direcția vectorului propriu dominant
    w = A @ v

    # Pasul 2: estimăm valoarea proprie ca norma vectorului rezultat
    # (sau mai precis, componenta maximă ca raport față de v)
    lambda_nou = np.max(np.abs(w))   # norma infinit a lui w

    # Pasul 3: normalizăm vectorul pentru a evita overflow
    v = w / lambda_nou

    print(f"{i+1:>5}  {lambda_nou:>22.10f}  {v}")

    # Criteriu de oprire: valoarea proprie s-a stabilizat
    if abs(lambda_nou - lambda_vechi) < tol:
        print(f"\nConvergență la iterația {i+1}")
        break
    lambda_vechi = lambda_nou

print(f"\n>>> Cea mai mare valoare proprie: λ ≈ {lambda_nou:.10f}")
print(f">>> Vectorul propriu asociat:    v ≈ {v}")

# --- Verificare cu NumPy ---
vals, vecs = np.linalg.eig(A)
print(f"\n[Verificare NumPy] Valorile proprii: {vals}")
print(f"[Verificare NumPy] λ_max = {max(vals):.10f}")