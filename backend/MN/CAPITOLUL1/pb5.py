# ============================================================
# PROBLEMA 5: Amplificarea erorilor - integrala recursiva
# Teorie in curs: Capitol 1 – "Propagarea si amplificarea erorilor"
#   Recurenta In = 1/n - (9/2)*I(n-1) este INSTABILA numeric:
#   o mica eroare in I0 se amplifica cu factorul (9/2) la fiecare pas.
# CERINTA: Evaluați numeric In = ∫01 xn/(x2+9) dx pentru n=7 folosind recurența In = 1/n − (9/2)·In−1.
# Valorile I0 = (1/2)·ln(10) ≈ 0.1003353477 (exactă) și I0 ≈ 0.10034 (aproximată).
# ============================================================

# Valoarea exacta si cea aproximata a lui I0 (date in enunt)
I0_exact = 0.1003353477   # valoarea exacta: I0 = integral_0^1 1/(x²+9) dx
I0_aprox = 0.10034        # valoarea aproximata (mai putine cifre)

print(f"I0 exact:    {I0_exact:.10f}")
print(f"I0 aproximat:{I0_aprox:.10f}")
print(f"Eroare I0:   {abs(I0_exact - I0_aprox):.2e}")
print()

# Aplicam recurenta In = 1/n - (9/2)*I(n-1) pentru n = 1 pana la 7
In_exact = I0_exact   # pornim cu valoarea exacta
In_aprox = I0_aprox   # pornim cu valoarea aproximata

for n in range(1, 8):  # n de la 1 la 7
    In_exact = 1/n - (9/2) * In_exact   # formula de recurenta (exact)
    In_aprox = 1/n - (9/2) * In_aprox   # aceeasi formula (cu eroare initiala)
    print(f"I{n} (pornind exact):    {In_exact:.10f}")
    print(f"I{n} (pornind aproximat):{In_aprox:.10f}")

eroare = abs(In_exact - In_aprox)   # eroarea s-a amplificat la fiecare pas!
print(f"Eroarea amplificata:   {eroare:.6f}  <- era doar {abs(I0_exact - I0_aprox):.2e} la inceput!")