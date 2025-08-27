#  Proyecto Colaborativo: Análisis de Datos FAC - Bienestar Familiar

##  Objetivo del Proyecto
Realizar un análisis básico de datos reales de una encuesta de bienestar familiar del personal de la Fuerza Aérea Colombiana (FAC), aplicando herramientas de *Python* y buenas prácticas de trabajo colaborativo en *Git/GitHub*.  

El análisis se desarrolló en tres etapas principales:
1. *Calidad de Datos* – Identificación de faltantes, duplicados y problemas de codificación.  
2. *Demografía Básica* – Exploración de variables de edad, género y grado militar.  
3. *Análisis Familiar* – Estudio del estado civil, convivencia y estructura familiar.

---

## 👥 Organización del Equipo (Grupo 8)

- *Mariana Celis*  
  - Rol de Estudiante A: Especialista en datos familiares.  
  - Rol de Estudiante C: Experta en calidad de datos.  

- *Vanessa Cortés*  
  - Rol de Estudiante B: Líder de análisis demográfico. 

---

##  Estructura del Repositorio


analisis-datos-fac-equipo-8/
│── README.md                → Descripción del proyecto
│── datos\_exploracion.py     → Código principal con funciones de análisis y generación de reportes
│── resultados\_analisis.md   → Resumen ejecutivo del análisis
│── requirements.txt         → Dependencias del proyecto
│
├── datos/
│   └── JEFAB\_2024.xlsx      → Base de datos original
│
├── reportes/
│   ├── calidad\_datos.md     → Reporte de calidad de datos
│   ├── demografia\_basica.md → Reporte de análisis demográfico
│   ├── analisis\_familiar.md → Reporte de análisis familiar
│   └── figs/                → Imágenes generadas para visualizaciones

`

---

##  Ejecución del Proyecto

### 1. Requisitos
Instalar dependencias en un entorno de Python 3:
bash
pip install -r requirements.txt
`

### 2. Generar reportes y resumen

* *Ejecutar todos los pasos (calidad, demografía y familiar):*

bash
python datos_exploracion.py --all


* *Ejecutar solo un paso específico:*

bash
python datos_exploracion.py --calidad
python datos_exploracion.py --demo
python datos_exploracion.py --familiar


### 3. Resultados generados

* reportes/calidad_datos.md
* reportes/demografia_basica.md
* reportes/analisis_familiar.md
* resultados_analisis.md (resumen ejecutivo)

---

## Créditos

Proyecto realizado por:

* *Mariana Celis* (Análisis Familiar y Calidad de Datos)
* *Vanessa Cortés* (Análisis Demografico)

*Grupo 8 – Proyecto Colaborativo: Análisis de Datos FAC - Bienestar Familiar*

```
