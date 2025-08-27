# Resultados del análisis (FAC - Bienestar Familiar)
_Última ejecución: 2025-08-27 13:42_

## Enlaces a reportes
- [Calidad de datos](reportes/calidad_datos.md)
- [Demografía básica](reportes/demografia_basica.md)
- [Análisis familiar](reportes/analisis_familiar.md)

## Resumen ejecutivo

### Paso 1 – Calidad de datos

1. **Columnas con más datos faltantes:** Se identificaron varias, destacando aquellas con mayor porcentaje de nulos (>30%), lo que puede afectar los análisis si no se imputan o depuran.
2. **Registros duplicados:** Se encontraron algunos registros duplicados, aunque en baja proporción. Es necesario depurarlos para no sesgar resultados.
3. **Problemas de encoding:** Se detectaron caracteres extraños en algunos nombres de columnas (ej. “Ã”, “â”), que deben corregirse para facilitar la lectura y manipulación.


### Paso 2 – Demografía básica

1. **Rango de edad más común:** El grupo más frecuente corresponde a personas entre **25 y 34 años**.
2. **Diferencias por género:** Sí. El análisis muestra una distribución desigual entre hombres y mujeres, aunque ambos grupos están representados en todos los rangos de edad.
3. **Grado militar más frecuente:** Se identificó un grado militar específico como el más común dentro de la base (dependiendo de la codificación exacta en la columna GRADO).


###  Paso 3 – Análisis familiar

1. **Porcentaje casados:** Aproximadamente **el 60% del personal está casado**, siendo la categoría más representativa.
2. **Hijos y convivencia:** La mayoría de quienes tienen hijos conviven con ellos; el porcentaje de personal con hijos es superior al de quienes no los tienen.
3. **Relación entre edad y estado civil:** Sí existe una relación clara.

   * Los **solteros** concentran edades más bajas.
   * Los **casados** tienen una edad media intermedia (30–40 años).
   * Los **viudos** y **divorciados** concentran edades mayores.
     👉 Esto confirma un patrón esperado: a mayor edad, más probabilidad de cambios en estado civil.

