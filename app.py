# app.py
import streamlit as st
from pathlib import Path
import pandas as pd

import matplotlib
matplotlib.use("Agg")

from datos_exploracion import (
    run_calidad,
    run_demografia,
    run_familiar,
    DATA_PATH,
    REPORT_DIR,
)

st.set_page_config(page_title="FAC - Bienestar Familiar", layout="wide")
PROJECT_DIR = Path(__file__).resolve().parent

@st.cache_data(show_spinner=True)
def load_data(path: Path):
    try:
        return pd.read_excel(path)
    except Exception as err:
        return {"__error__": err}

st.title("Proyecto Colaborativo: Análisis de Datos FAC - Bienestar Familiar")
st.caption("Etapas: **Calidad de Datos**, **Demografía**, **Análisis Familiar**.")

data = load_data(DATA_PATH)
if isinstance(data, dict) and "__error__" in data:
    st.error("No se pudo cargar el archivo Excel.")
    st.code(str(DATA_PATH))
    st.exception(data["__error__"])
else:
    with st.expander("Ver muestra de datos"):
        st.dataframe(data.head(20), use_container_width=True)

tab1, tab2, tab3 = st.tabs(["1) Calidad de datos", "2) Demografía básica", "3) Análisis familiar"])

with tab1:
    st.subheader("Calidad de datos")
    try:
        res = run_calidad(save_md=True)
        st.markdown("### Preguntas")
        st.markdown("**1. ¿Qué columnas tienen más datos faltantes?**")
        st.dataframe(res["top_missing"], use_container_width=True)

        st.markdown("**2. ¿Hay registros duplicados?**")
        st.metric(label="Duplicados", value=res["duplicados"])

        st.markdown("**3. ¿Qué problemas de encoding se detectan?**")
        if res["encoding_cols"]:
            st.write(f"Columnas afectadas: {len(res['encoding_cols'])}")
            st.write(res["encoding_cols"])
        else:
            st.success("No se detectaron problemas típicos de encoding en nombres de columnas.")

        st.markdown("---")
        st.markdown(f"**Reporte .md:** `{(REPORT_DIR/'calidad_datos.md').as_posix()}`")
    except Exception as e:
        st.error("Falló el análisis de calidad de datos.")
        st.exception(e)

with tab2:
    st.subheader("Demografía básica")
    try:
        res = run_demografia(save_md=True)

        st.markdown("### Preguntas")
        st.markdown("**1. ¿Cuál es el rango de edad más común?**")
        st.metric("Rango de edad dominante", res.get("rango_mas_comun") or "N/D")

        st.markdown("**2. ¿Hay diferencias en la distribución por género?**")
        if res["genero_counts"] is not None:
            st.dataframe(res["genero_counts"].rename("Cantidad").to_frame(), use_container_width=True)
        else:
            st.info("No se encontró una columna de género.")

        st.markdown("**3. ¿Cuál es el grado militar más frecuente?**")
        st.metric("Grado/Rango más frecuente", res.get("grado_mas_frec") or "N/D")

        st.markdown("### Visualizaciones")
        for fig in res["figs"]:
            st.image(fig, use_column_width=True)

        st.markdown("---")
        st.markdown(f"**Reporte .md:** `{(REPORT_DIR/'demografia_basica.md').as_posix()}`")
    except Exception as e:
        st.error("Falló el análisis demográfico.")
        st.exception(e)

with tab3:
    st.subheader("Análisis familiar")
    try:
        res = run_familiar(save_md=True)

        st.markdown("### Preguntas")
        st.markdown("**1. ¿Qué porcentaje del personal está casado?**")
        st.metric("% Casados", f"{res['pct_casados']}%")

        st.markdown("**2. ¿Cuántos tienen hijos y cuántos viven con ellos?**")
        col1, col2 = st.columns(2)
        col1.metric("Con hijos", res.get("total_tiene_hijos", "N/D"))
        col2.metric("Viven con familia/hijos", res.get("total_conviven", "N/D"))

        st.markdown("**3. ¿Hay relación entre edad y estado civil?**")
        st.write("Revisa el boxplot y las medias por grupo para evidencias descriptivas de relación.")
        for fig in res["figs"]:
            st.image(fig, use_column_width=True)

        st.markdown("---")
        st.markdown(f"**Reporte .md:** `{(REPORT_DIR/'analisis_familiar.md').as_posix()}`")
    except Exception as e:
        st.error("Falló el análisis familiar.")
        st.exception(e)
#fin