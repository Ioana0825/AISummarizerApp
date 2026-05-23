# ============================================================
# PROBLEMA 7: Eroare absoluta vs. eroare relativa
# Teorie in curs: Capitol 1 – "Masurarea erorilor"
#   Eroare absoluta  = |x_real - x_calc|
#   Eroare relativa  = |x_real - x_calc| / |x_real|
#   Eroarea relativa e mai relevanta cand valorile sunt foarte diferite.
# CERINTA: Comparați erorile de aproximare în două situații: x_real = 13 → x_calc = 14 și y_real = 1386
# → y_calc = 1387.
# ============================================================

# Cazul 1: numere mici
x_real = 13;   x_calc = 14
err_abs_x = abs(x_real - x_calc)       # eroarea absoluta
err_rel_x = err_abs_x / abs(x_real)    # eroarea relativa

# Cazul 2: numere mari
y_real = 1386; y_calc = 1387
err_abs_y = abs(y_real - y_calc)
err_rel_y = err_abs_y / abs(y_real)

print(f"Cazul 1: x_real={x_real}, x_calc={x_calc}")
print(f"  Eroare absoluta: {err_abs_x}")
print(f"  Eroare relativa: {err_rel_x:.4%}")    # afisat ca procent

print(f"\nCazul 2: y_real={y_real}, y_calc={y_calc}")
print(f"  Eroare absoluta: {err_abs_y}")
print(f"  Eroare relativa: {err_rel_y:.4%}")

print()
print("Concluzie: eroarea absoluta e aceeasi (1) in ambele cazuri,")
print("dar eroarea relativa arata ca x (7.69%) e mult mai prost")
print("aproximat decat y (0.07%).")