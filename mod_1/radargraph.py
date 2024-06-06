import numpy as np
import matplotlib.pyplot as plt

# Definir el número de variables
num_vars = 6

# Crear un array 2D de forma (6,) con los valores para cada variable
valores = [7.5, 5.0, 9.0, 4.5, 8.0, 6.5]  # Valores de ejemplo; reemplaza con tus datos reales
valores += valores[:1]  # Repetir el primer valor para cerrar el círculo

# Calcular el ángulo para cada eje
angulos = [n / float(num_vars) * 2 * np.pi for n in range(num_vars)]
angulos += angulos[:1]

# Inicializar el gráfico de radar
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

# Dibujar un eje por variable + agregar etiquetas
plt.xticks(angulos[:-1], ['Comunicación', 'Familiaridad', 'Uso futuro', 'Orientación', 'Escalabilidad', 'Programación'])

# Agregar etiquetas en el eje y
ax.set_rlabel_position(30)
plt.yticks([2.5, 5.0, 7.5], ["2.5", "5", "7.5"], color="grey", size=7)
plt.ylim(0, max(valores))

# Graficar los datos y rellenar con color
ax.plot(angulos, valores)
ax.fill(angulos, valores, 'skyblue', alpha=0.4)

# Mostrar el gráfico
plt.show()
