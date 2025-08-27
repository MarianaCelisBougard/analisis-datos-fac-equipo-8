# Calidad de Datos

_Actualizado: 2025-08-27 13:42_



## Preguntas y respuestas

1. **¿Qué columnas tienen más datos faltantes?**

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
                                EDAD2               13        0.20
                           EDAD_RANGO               13        0.20
```



2. **¿Hay registros duplicados?**  
**0** registros duplicados.



3. **¿Qué problemas de encoding se detectan?**

No se detectaron patrones típicos de mal encoding (por ejemplo `Ã`, `â`).



## Tipos de datos

- **int64**: 153
- **object**: 66
- **float64**: 12