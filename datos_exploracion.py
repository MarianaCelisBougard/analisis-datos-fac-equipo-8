# demografia_basica.py
 import pandas as pd
 import matplotlib.pyplot as plt
 # Leer los datos
 df = pd.read_excel('datos/JEFAB_2024.xlsx')
 # Explorar estructura básica
 print("=== INFORMACIÓN GENERAL ===")
 print(f"Total de registros: {len(df)}")
 print(f"Total de columnas: {len(df.columns)}")
 # Análisis de edad
 print("\n=== ANÁLISIS DE EDAD ===")
 print(f"Edad promedio: {df['EDAD2'].mean():.1f} años")
 print(f"Edad mínima: {df['EDAD2'].min()} años")
 print(f"Edad máxima: {df['EDAD2'].max()} años")
 # Análisis de género
 print("\n=== ANÁLISIS DE GÉNERO ===")
 print(df['GENERO'].value_counts())
 # Gráfico de edades
 plt.figure(figsize=(10, 6))
 plt.hist(df['EDAD2'], bins=20, edgecolor='black')
 plt.title('Distribución de Edades del Personal FAC')
 plt.xlabel('Edad')
 plt.ylabel('Cantidad de Personal')
 plt.show()
