# Resultados del análisis (FAC - Bienestar Familiar)
_Última ejecución: 2025-08-29 10:39_

## Enlaces a reportes
- [Calidad de datos](reportes/calidad_datos.md)
- [Demografía básica](reportes/demografia_basica.md)
- [Análisis familiar](reportes/analisis_familiar.md)

## Resumen ejecutivo

### Paso 1 – Calidad de datos

1. **Columnas con más datos faltantes:** Se identificaron varias, destacando aquellas con mayor porcentaje de nulos (>30%), lo que puede afectar los análisis si no se imputan o depuran.
2. **Registros duplicados:** Se eliminaron **0** duplicados. Actualmente quedan **0**.
3. **Problemas de encoding:** Se detectaron caracteres extraños en algunos nombres de columnas (ej. “Ã”, “â”), los cuales fueron corregidos para facilitar el análisis.
4. **Limpieza aplicada:**
   - Normalización de nombres de columnas.
   - Imputación de edades faltantes con la media (37 años).
   - Normalización de texto en columnas de género y estado civil.

### Paso 2 – Demografía básica

1. **Rango de edad más común:** 25-34.
2. **Diferencias por género:** Sí. El análisis muestra una distribución desigual entre hombres y mujeres, aunque ambos grupos están representados en todos los rangos de edad.
3. **Grado militar más frecuente:** NO RESPONDE.

###  Paso 3 – Análisis familiar

1. **Porcentaje casados:** Aproximadamente **60.55%** del personal está casado.
2. **Hijos y convivencia:** Se identificaron **3669** personas con hijos y **1185** que conviven con su familia.
3. **Relación entre edad y estado civil:** Sí existe una relación clara.  
   * Los **solteros** concentran edades más bajas.  
   * Los **casados** tienen una edad media intermedia (30–40 años).  
   * Los **viudos** y **divorciados** concentran edades mayores.  
   👉 Esto confirma un patrón esperado: a mayor edad, más probabilidad de cambios en estado civil.

**Dataset utilizado para Paso 2 y 3:** `reportes/datos_limpios.xlsx`
