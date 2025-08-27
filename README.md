
```markdown
#  Proyecto Colaborativo: Análisis de Datos FAC - Bienestar Familiar

##  Objetivo del Proyecto
Realizar un análisis básico de datos reales de una encuesta de bienestar familiar del personal de la Fuerza Aérea Colombiana (FAC), aplicando herramientas de **Python**, buenas prácticas de trabajo colaborativo en **Git/GitHub**, y un flujo de **limpieza + análisis** de datos.

El proyecto se desarrolla en tres etapas principales:
1. **Calidad de Datos (con limpieza incluida)** – Identificación y corrección de problemas en los datos.  
2. **Demografía Básica** – Exploración de variables de edad, género y grado militar.  
3. **Análisis Familiar** – Estudio del estado civil, convivencia y estructura familiar.

---

##  Proceso de Limpieza
Antes de los análisis, el proyecto aplica un **proceso de limpieza automática** al dataset:

- **Nombres de columnas**: se corrigen caracteres extraños (`Ã`, `â`, etc.) y espacios innecesarios.  
- **Duplicados**: se eliminan registros repetidos.  
- **Edades faltantes**: se imputan con la **media de edad**.  
- **Texto normalizado**: columnas de **género** y **estado civil** se convierten a mayúsculas y se estandarizan (ej. “M” → “MASCULINO”).  
- **Dataset limpio**: se guarda en `reportes/datos_limpios.xlsx`, el cual es utilizado en los pasos de **Demografía** y **Análisis Familiar**.  

Esto garantiza que los resultados se basen en información coherente y depurada.

---

## Organización del Equipo (Grupo 8)

- **Mariana Celis**  
  - Rol de *Estudiante A*: Líder de análisis demográfico.  
  - Rol de *Estudiante C*: Encargada de calidad y limpieza de datos.  

- **Vanessa Cortés**  
  - Rol de *Estudiante B*: Especialista en análisis familiar.  

---

##  Estructura del Repositorio
```

analisis-datos-fac-equipo-8/
│── README.md                → Descripción del proyecto
│── datos\_exploracion.py     → Código principal con limpieza y análisis
│── resultados\_analisis.md   → Resumen ejecutivo del análisis
│── requirements.txt         → Dependencias del proyecto
│
├── datos/
│   └── JEFAB\_2024.xlsx      → Base de datos original
│
├── reportes/
│   ├── datos\_limpios.xlsx   → Dataset limpio generado automáticamente
│   ├── calidad\_datos.md     → Reporte de calidad de datos (con limpieza)
│   ├── demografia\_basica.md → Reporte de análisis demográfico
│   ├── analisis\_familiar.md → Reporte de análisis familiar
│   └── figs/                → Imágenes generadas para visualizaciones

````

---

##  Ejecución del Proyecto

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
````

### 2. Ejecutar los análisis

* **Todo el flujo (limpieza + 3 pasos + resumen):**

```bash
python datos_exploracion.py --all
```

* **Solo calidad (con limpieza aplicada):**

```bash
python datos_exploracion.py --calidad
```

* **Solo demografía:**

```bash
python datos_exploracion.py --demo
```

* **Solo análisis familiar:**

```bash
python datos_exploracion.py --familiar
```

---

##  Resultados generados

* `reportes/datos_limpios.xlsx` → dataset limpio
* `reportes/calidad_datos.md` → calidad de datos con limpieza
* `reportes/demografia_basica.md` → análisis demográfico
* `reportes/analisis_familiar.md` → análisis familiar
* `resultados_analisis.md` → resumen ejecutivo

---

##  Créditos

Proyecto realizado por:

* **Mariana Celis** (Calidad de Datos y Demografía)
* **Vanessa Cortés** (Análisis Familiar)

**Grupo 8 – Proyecto Colaborativo: Análisis de Datos FAC - Bienestar Familiar**