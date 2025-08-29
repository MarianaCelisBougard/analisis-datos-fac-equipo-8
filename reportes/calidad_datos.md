# Calidad de Datos (con limpieza aplicada)

_Actualizado: 2025-08-29 10:39_



## Limpieza aplicada

- **Nombres de columnas** normalizados (se corrigieron caracteres extraños y espacios).

- **Duplicados eliminados:** 0

- **Imputación de edades faltantes** con la media en `EDAD2` (**37** años).

- **Género** y **estado civil** convertidos a mayúsculas y estandarizados.

- **Dataset limpio** guardado en: `reportes/datos_limpios.xlsx`



## Datos faltantes después de limpieza

```
                              Columna  Datos_Faltantes  Porcentaje
NUMERO_PERSONAS_APORTE_SOSTENIMIENTO2             3928       61.16
             NUMERO_HABITAN_VIVIENDA2             3808       59.29
                         NUMERO_HIJOS             3217       50.09
                       HIJOS_EN_HOGAR             3200       49.82
                     EDAD_RANGO_PADRE             1939       30.19
                           EDAD_PADRE             1939       30.19
                     EDAD_RANGO_MADRE              889       13.84
                           EDAD_MADRE              885       13.78
                           EDAD_RANGO               13        0.20
                               CUERPO                0        0.00
```



## Tipos de datos

- **int64**: 153
- **object**: 66
- **float64**: 12