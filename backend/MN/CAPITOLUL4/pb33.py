"""
PROBLEMA 33 - Interpolarea Lagrange (polinom de gradul 2)
CERINTA: Construiți polinomul Lagrange de gradul 2 pentru punctele: (0, 1), (1, 3), (2, 7). Calculați f(1.5).
=========================================================
TEORIE (Curs - Capitol: Interpolare si Aproximare):
  Dat fiind n+1 puncte (x0,y0), (x1,y1), ..., (xn,yn),
  polinomul Lagrange de grad n este:

      P(x) = sum_{i=0}^{n} y_i * L_i(x)

  unde baza Lagrange L_i(x) este:

      L_i(x) = prod_{j=0, j!=i}^{n} (x - x_j) / (x_i - x_j)

  Fiecare L_i(x) are proprietatea: L_i(x_i)=1 si L_i(x_j)=0 pt j!=i

Puncte date: (0,1), (1,3), (2,7) => polinom grad 2
Se cere: f(1.5)
"""

# -------------------------------------------------------
# PASUL 1: Definim datele problemei
# -------------------------------------------------------
# Nodurile de interpolare (valorile x cunoscute)
x_nodes = [0, 1, 2]

# Valorile functiei in noduri (valorile y cunoscute)
y_nodes = [1, 3, 7]

# Punctul in care vrem sa aproximam valoarea functiei
x_eval = 1.5

# -------------------------------------------------------
# PASUL 2: Functia de interpolare Lagrange
# -------------------------------------------------------
def lagrange(x_nodes, y_nodes, x):
    """
    Calculeaza P(x) prin formula Lagrange.
    Formula: P(x) = sum_i [ y_i * L_i(x) ]
    """
    n = len(x_nodes)   # numarul de noduri
    rezultat = 0.0     # initializam suma cu 0

    for i in range(n):
        # Calculam baza Lagrange L_i(x):
        # L_i(x) = prod_{j!=i} (x - x_j) / (x_i - x_j)
        Li = 1.0
        for j in range(n):
            if j != i:
                # Inmultim cu (x - x_j) / (x_i - x_j) pentru fiecare j diferit de i
                Li *= (x - x_nodes[j]) / (x_nodes[i] - x_nodes[j])

        # Adunam contributia nodului i: y_i * L_i(x)
        rezultat += y_nodes[i] * Li

    return rezultat

# -------------------------------------------------------
# PASUL 3: Calculam si afisam rezultatul
# -------------------------------------------------------
# Calculam polinomul Lagrange in x=1.5
valoare = lagrange(x_nodes, y_nodes, x_eval)

print("=== PROBLEMA 33 - Interpolare Lagrange ===")
print(f"Noduri x: {x_nodes}")
print(f"Valori y: {y_nodes}")
print(f"P(1.5) = {valoare:.6f}")

# -------------------------------------------------------
# PASUL 4: Verificare - polinomul Lagrange ESTE solutia exacta!
# -------------------------------------------------------
# Prin 3 puncte trece un singur polinom de grad <= 2.
# Gasim coeficientii rezolvand sistemul:
#   a*0^2 + b*0 + c = 1  => c = 1
#   a*1^2 + b*1 + c = 3  => a + b = 2
#   a*2^2 + b*2 + c = 7  => 4a + 2b = 6 => 2a + b = 3
# Scazand: a = 1, b = 1 => P(x) = x^2 + x + 1
# La x=1.5: P(1.5) = 2.25 + 1.5 + 1 = 4.75 ✓ (corespunde!)
valoare_exacta = x_eval**2 + x_eval + 1   # P(x) = x^2 + x + 1
print(f"Polinomul interpolant exact: P(x) = x^2 + x + 1")
print(f"P(1.5) = (1.5)^2 + 1.5 + 1 = {valoare_exacta:.6f}")
print(f"Eroarea (trebuie ~0): {abs(valoare - valoare_exacta):.2e}")