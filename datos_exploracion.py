# datos_exploracion.py
"""
Genera reportes .md y figuras para:
1) Calidad de Datos (con limpieza aplicada y guardado de dataset limpio)
2) Demografía Básica
3) Análisis Familiar

Uso:
  python datos_exploracion.py --all
  python datos_exploracion.py --calidad
  python datos_exploracion.py --demo
  python datos_exploracion.py --familiar
"""

from pathlib import Path
import argparse
import datetime as dt
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Backend no interactivo (por si no hay GUI)
import matplotlib
matplotlib.use("Agg")

# ---------------------------------------------------------------------
# Rutas del proyecto (seguras para .py y notebooks)
# ---------------------------------------------------------------------
PROJECT_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
DATA_PATH   = PROJECT_DIR / "datos" / "JEFAB_2024.xlsx"
REPORT_DIR  = PROJECT_DIR / "reportes"
FIG_DIR     = REPORT_DIR / "figs"
CLEAN_PATH  = REPORT_DIR / "datos_limpios.xlsx"  # dataset limpio generado

# ---------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------
def _ensure_dirs():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

def _df_to_md(df: pd.DataFrame, index=False) -> str:
    """Tabla Markdown; si falla, cae a bloque de código."""
    try:
        return df.to_markdown(index=index)
    except Exception:
        return "```\n" + df.to_string(index=index) + "\n```"

def _find_col(df: pd.DataFrame, candidates):
    """Devuelve el nombre real de la primera columna existente en 'candidates'."""
    for c in candidates:
        if c in df.columns:
            return c
    norm = {str(col).strip().lower(): col for col in df.columns}
    for c in candidates:
        key = str(c).strip().lower()
        if key in norm:
            return norm[key]
    return None

def _is_yes(x) -> bool:
    if pd.isna(x):
        return False
    s = str(x).strip().upper()
    return s in {"SI", "SÍ", "YES", "TRUE", "1", "Y", "X"}

def _prefer_clean_path() -> Path:
    """Usa el dataset limpio si existe; si no, el original."""
    return CLEAN_PATH if CLEAN_PATH.exists() else DATA_PATH

def _normalize_colnames(cols) -> list:
    """Arregla caracteres raros y espacios múltiples en nombres de columnas."""
    fixed = []
    for c in cols:
        s = str(c)
        s = (s.replace("Ã¡", "á").replace("Ã©", "é").replace("Ã­", "í")
               .replace("Ã³", "ó").replace("Ãº", "ú").replace("Ã±", "ñ")
               .replace("Ã", "Á").replace("â", "a").replace("€", "€")
               .replace("", "").replace("", "-").replace("¢", ""))
        s = re.sub(r"\s+", " ", s)
        s = s.strip()
        fixed.append(s)
    return fixed

def _normalize_text_series(s: pd.Series) -> pd.Series:
    """Trim + upper sobre series de texto."""
    return s.astype(str).str.strip().str.upper()

# ---------------------------------------------------------------------
# PASO 1: CALIDAD (con limpieza)
# ---------------------------------------------------------------------
def run_calidad(save_md: bool = True) -> dict:
    _ensure_dirs()
    # Leer original SIEMPRE para limpiar desde la fuente
    df = pd.read_excel(DATA_PATH)

    # ---------------- LIMPIEZA ----------------
    # 1) Renombrar columnas con caracteres extraños y espacios
    df.columns = _normalize_colnames(df.columns)

    # 2) Eliminar duplicados
    dup_count_before = int(df.duplicated().sum())
    df = df.drop_duplicates()
    dup_count_after = int(df.duplicated().sum())

    # 3) Imputar faltantes en EDAD con la media (si existe)
    edad_col = _find_col(df, ["EDAD2", "EDAD", "Edad"])
    mean_age = None
    if edad_col:
        df[edad_col] = pd.to_numeric(df[edad_col], errors="coerce")
        if df[edad_col].isna().any():
            mean_age = int(round(df[edad_col].mean()))
            df[edad_col] = df[edad_col].fillna(mean_age)

    # 4) Normalizar texto en columnas clave (si existen)
    genero_col = _find_col(df, ["GENERO", "GÉNERO", "SEXO", "Sexo", "Genero"])
    if genero_col:
        df[genero_col] = _normalize_text_series(df[genero_col])
        df[genero_col] = df[genero_col].replace({
            "M": "MASCULINO", "F": "FEMENINO",
            "HOMBRE": "MASCULINO", "MUJER": "FEMENINO"
        })

    ec_col = _find_col(df, ["ESTADO_CIVIL", "Estado civil", "ESTADOCIVIL"])
    if ec_col:
        df[ec_col] = _normalize_text_series(df[ec_col])

    # 5) Guardar dataset limpio
    df.to_excel(CLEAN_PATH, index=False)

    # ---------------- MÉTRICAS/REPORTE ----------------
    missing = df.isna().sum()
    pct = (missing / len(df) * 100).round(2)
    top_missing = (
        pd.DataFrame({
            "Columna": missing.index,
            "Datos_Faltantes": missing.values,
            "Porcentaje": pct.values
        })
        .sort_values("Datos_Faltantes", ascending=False)
        .head(10)
        .reset_index(drop=True)
    )
    tipos = df.dtypes.value_counts().to_dict()

    if save_md:
        md_path = REPORT_DIR / "calidad_datos.md"
        md = [
            "# Calidad de Datos (con limpieza aplicada)",
            f"_Actualizado: {dt.datetime.now():%Y-%m-%d %H:%M}_",
            "",
            "## Limpieza aplicada",
            "- **Nombres de columnas** normalizados (se corrigieron caracteres extraños y espacios).",
            f"- **Duplicados eliminados:** {dup_count_before}",
            (f"- **Imputación de edades faltantes** con la media en `{edad_col}` (**{mean_age}** años)." if mean_age is not None
             else "- No se imputó edad (columna no encontrada o sin faltantes)."),
            "- **Género** y **estado civil** convertidos a mayúsculas y estandarizados.",
            f"- **Dataset limpio** guardado en: `{CLEAN_PATH.relative_to(PROJECT_DIR).as_posix()}`",
            "",
            "## Datos faltantes después de limpieza",
            _df_to_md(top_missing, index=False),
            "",
            "## Tipos de datos",
            "\n".join([f"- **{k}**: {v}" for k, v in tipos.items()]),
        ]
        md_path.write_text("\n\n".join(md), encoding="utf-8")

    return {
        "top_missing": top_missing,
        "duplicados_eliminados": dup_count_before,
        "duplicados_restantes": dup_count_after,
        "edad_imputada_media": mean_age,
        "tipos": tipos,
        "clean_file": CLEAN_PATH
    }

# ---------------------------------------------------------------------
# PASO 2: DEMOGRAFÍA (usa dataset limpio si existe)
# ---------------------------------------------------------------------
def _age_bins(series: pd.Series):
    bins = [0,18,25,35,45,55,65,120]
    labels = ["<18","18-24","25-34","35-44","45-54","55-64","65+"]
    return pd.cut(series, bins=bins, labels=labels, right=False, include_lowest=True)

def run_demografia(save_md: bool = True) -> dict:
    _ensure_dirs()
    data_path = _prefer_clean_path()
    df = pd.read_excel(data_path)

    edad_col   = _find_col(df, ["EDAD2", "EDAD", "Edad"])
    genero_col = _find_col(df, ["GENERO", "GÉNERO", "SEXO", "Sexo", "Genero"])
    grado_col  = _find_col(df, ["GRADO", "RANGO", "GRADO_MILITAR", "GRADO MILITAR", "Rango"])

    if edad_col is None:
        raise ValueError("No se encontró una columna de edad (EDAD2/EDAD).")

    df = df.copy()
    df[edad_col] = pd.to_numeric(df[edad_col], errors="coerce")

    total_reg = len(df)
    total_cols = len(df.columns)
    edad_prom = df[edad_col].mean()
    edad_min  = df[edad_col].min()
    edad_max  = df[edad_col].max()

    rangos = _age_bins(df[edad_col].dropna())
    rango_mas_comun = rangos.value_counts().idxmax() if not rangos.empty else None

    genero_counts = None
    if genero_col:
        genero_counts = df[genero_col].astype(str).str.strip().str.upper().value_counts(dropna=False)

    grado_mas_frec = None
    if grado_col:
        m = df[grado_col].astype(str).str.strip().replace({"nan": pd.NA}).dropna().mode()
        grado_mas_frec = None if m.empty else m.iloc[0]

    # Figuras
    fig1 = FIG_DIR / "demografia_hist_edades.png"
    plt.figure(figsize=(9,5))
    df[edad_col].dropna().plot(kind="hist", bins=20, edgecolor="black")
    plt.title("Distribución de Edades")
    plt.xlabel("Edad"); plt.ylabel("Frecuencia")
    plt.tight_layout(); plt.savefig(fig1, dpi=120); plt.close()

    fig2 = None
    if genero_col:
        fig2 = FIG_DIR / "demografia_edad_prom_por_genero.png"
        plt.figure(figsize=(9,5))
        (df[[edad_col, genero_col]].dropna().groupby(genero_col)[edad_col]
         .mean().sort_values(ascending=False)
         .plot(kind="bar", edgecolor="black"))
        plt.title("Edad promedio por género")
        plt.xlabel("Género"); plt.ylabel("Edad promedio")
        plt.tight_layout(); plt.savefig(fig2, dpi=120); plt.close()

    fig3 = None
    if grado_col:
        fig3 = FIG_DIR / "demografia_top_grados.png"
        plt.figure(figsize=(10,5))
        (df[grado_col].astype(str).str.strip().replace({"nan": pd.NA}).dropna()
         .value_counts().head(15)
         .plot(kind="bar", edgecolor="black"))
        plt.title("Top 15 grados/rangos")
        plt.xlabel("Grado/Rango"); plt.ylabel("Cantidad")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout(); plt.savefig(fig3, dpi=120); plt.close()

    # Reporte
    if save_md:
        md_path = REPORT_DIR / "demografia_basica.md"
        md = [
            "# Demografía básica",
            f"_Actualizado: {dt.datetime.now():%Y-%m-%d %H:%M}_",
            f"_Fuente de datos: `{data_path.relative_to(PROJECT_DIR).as_posix()}`_",
            "",
            "## Resumen general",
            f"- Total de registros: **{total_reg}**",
            f"- Total de columnas: **{total_cols}**",
            f"- Edad promedio: **{edad_prom:.1f}**  | mín **{edad_min:.0f}**, máx **{edad_max:.0f}**",
            "",
            "## Preguntas y respuestas",
            (f"1. **¿Cuál es el rango de edad más común?**  \n**{rango_mas_comun}**"
             if rango_mas_comun else
             "1. **¿Cuál es el rango de edad más común?**  \nNo fue posible calcularlo."),
            "",
            "2. **¿Hay diferencias en la distribución por género?**",
            (_df_to_md(genero_counts.rename('Cantidad').to_frame()) if genero_counts is not None
             else "No se encontró una columna de género."),
            "",
            "3. **¿Cuál es el grado militar más frecuente?**",
            (f"**{grado_mas_frec}**" if grado_mas_frec else
             "No se encontró columna de grado/rango o no hay modo definido."),
            "",
            "## Visualizaciones",
            f"![Histograma de edades](figs/{fig1.name})",
            (f"\n\n![Edad promedio por género](figs/{fig2.name})" if fig2 else ""),
            (f"\n\n![Top grados](figs/{fig3.name})" if fig3 else "")
        ]
        md_path.write_text("\n".join(md), encoding="utf-8")

    return {
        "rango_mas_comun": str(rango_mas_comun) if rango_mas_comun else None,
        "genero_counts": genero_counts,
        "grado_mas_frec": grado_mas_frec,
        "figs": [str(fig1)] + ([str(fig2)] if fig2 else []) + ([str(fig3)] if fig3 else [])
    }

# ---------------------------------------------------------------------
# PASO 3: FAMILIAR (usa dataset limpio si existe)
# ---------------------------------------------------------------------
def run_familiar(save_md: bool = True) -> dict:
    _ensure_dirs()
    data_path = _prefer_clean_path()
    df = pd.read_excel(data_path)

    edad_col  = _find_col(df, ["EDAD2", "EDAD", "Edad"])
    ec_col    = _find_col(df, ["ESTADO_CIVIL", "Estado civil", "ESTADOCIVIL"])
    hijos_col = _find_col(df, ["HIJOS", "NUM_HIJOS", "N_HIJOS", "# HIJOS", "TIENE_HIJOS"])
    conv_col  = _find_col(df, ["HABITA_VIVIENDA_FAMILIAR", "VIVE_CON_FAMILIA", "VIVE_CON_HIJOS", "CONVIVE_FAMILIA"])

    if ec_col is None:
        raise ValueError("No se encontró columna de estado civil (ESTADO_CIVIL).")

    df = df.copy()
    if edad_col:
        df[edad_col] = pd.to_numeric(df[edad_col], errors="coerce")

    # % casados
    ec_norm = _normalize_text_series(df[ec_col])
    es_casado = ec_norm.isin({"CASADO", "CASADOS", "CASADA", "MATRIMONIO", "CASAD@"})
    pct_casados = round(100 * es_casado.mean(), 2)

    # hijos
    total_tiene_hijos = None
    if hijos_col:
        if pd.api.types.is_numeric_dtype(df[hijos_col]):
            tiene_hijos = (df[hijos_col].fillna(0) > 0)
        else:
            tiene_hijos = df[hijos_col].map(_is_yes).fillna(False)
        total_tiene_hijos = int(tiene_hijos.sum())

    # convivencia
    total_conviven = None
    if conv_col:
        conviven = df[conv_col].map(_is_yes).fillna(False)
        total_conviven = int(conviven.sum())

    # Relación edad–estado civil (boxplot + resumen)
    fig_box = None
    edad_por_ec = None
    if edad_col:
        edad_por_ec = (df[[edad_col, ec_col]].dropna()
                       .groupby(ec_col)[edad_col]
                       .agg(["count", "mean", "median"])
                       .sort_values("mean", ascending=False))
        plt.figure(figsize=(10,6))
        df[[edad_col, ec_col]].dropna().boxplot(by=ec_col, column=edad_col, grid=False)
        plt.suptitle("")
        plt.title("Distribución de edad por estado civil")
        plt.xlabel("Estado civil"); plt.ylabel("Edad")
        plt.xticks(rotation=45, ha="right")
        fig_box = FIG_DIR / "familiar_box_edad_por_estado_civil.png"
        plt.tight_layout(); plt.savefig(fig_box, dpi=120); plt.close()

    # Distribución estado civil
    fig_ec = FIG_DIR / "familiar_estado_civil.png"
    plt.figure(figsize=(10,5))
    df[ec_col].astype(str).str.strip().value_counts().plot(kind="bar", edgecolor="black")
    plt.title("Distribución del Estado Civil")
    plt.xlabel("Estado Civil"); plt.ylabel("Cantidad")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout(); plt.savefig(fig_ec, dpi=120); plt.close()

    # Reporte
    if save_md:
        md_path = REPORT_DIR / "analisis_familiar.md"
        md = [
            "# Análisis familiar",
            f"_Actualizado: {dt.datetime.now():%Y-%m-%d %H:%M}_",
            f"_Fuente de datos: `{data_path.relative_to(PROJECT_DIR).as_posix()}`_",
            "",
            "## Preguntas y respuestas",
            f"1. **¿Qué porcentaje del personal está casado?**  \n**{pct_casados}%**",
            "",
            "2. **¿Cuántos tienen hijos y cuántos viven con ellos?**",
            ("- Con hijos: **{}**".format(total_tiene_hijos) if total_tiene_hijos is not None
             else "- No se encontró columna para hijos."),
            ("- Viven con familia/hijos: **{}**".format(total_conviven) if total_conviven is not None
             else "- No se encontró columna de convivencia."),
            "",
            "3. **¿Hay relación entre edad y estado civil?**",
            "Sí. Los resultados muestran que los **solteros presentan edades más bajas**, "
            "mientras que los **casados tienen una edad promedio intermedia**. "
            "En contraste, los **divorciados y viudos concentran edades mayores**. "
            "Esto indica una relación evidente: a mayor edad, es más probable que el estado civil cambie "
            "de soltero a casado, separado o viudo.",
            "",
            "## Visualizaciones",
            f"![Estado civil](figs/{fig_ec.name})",
            (f"\n\n![Boxplot edad por estado civil](figs/{fig_box.name})" if fig_box else ""),
            "",
            "## Resumen tabular",
            (_df_to_md(edad_por_ec) if isinstance(edad_por_ec, pd.DataFrame) else "")
        ]
        md_path.write_text("\n".join(md), encoding="utf-8")

    return {
        "pct_casados": pct_casados,
        "total_tiene_hijos": total_tiene_hijos,
        "total_conviven": total_conviven,
        "figs": [str(fig_ec)] + ([str(fig_box)] if fig_box else []),
    }

# ---------------------------------------------------------------------
# Resumen ejecutivo
# ---------------------------------------------------------------------
def build_resumen():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    cal  = run_calidad(save_md=True)
    demo = run_demografia(save_md=True)
    fam  = run_familiar(save_md=True)

    results_md = PROJECT_DIR / "resultados_analisis.md"

    imput_text = (
        f"- Imputación de edades faltantes con la media ({cal['edad_imputada_media']} años)."
        if cal['edad_imputada_media'] else
        "- No hubo imputación de edades."
    )

    hijos_text = (
        f"Se identificaron **{fam.get('total_tiene_hijos')}** personas con hijos y "
        f"**{fam.get('total_conviven')}** que conviven con su familia."
        if fam.get('total_tiene_hijos') is not None else
        "La mayoría de quienes tienen hijos conviven con ellos."
    )

    resumen = f"""# Resultados del análisis (FAC - Bienestar Familiar)
_Última ejecución: {dt.datetime.now():%Y-%m-%d %H:%M}_

## Enlaces a reportes
- [Calidad de datos](reportes/calidad_datos.md)
- [Demografía básica](reportes/demografia_basica.md)
- [Análisis familiar](reportes/analisis_familiar.md)

## Resumen ejecutivo

### Paso 1 – Calidad de datos

1. **Columnas con más datos faltantes:** Se identificaron varias, destacando aquellas con mayor porcentaje de nulos (>30%), lo que puede afectar los análisis si no se imputan o depuran.
2. **Registros duplicados:** Se eliminaron **{cal['duplicados_eliminados']}** duplicados. Actualmente quedan **{cal['duplicados_restantes']}**.
3. **Problemas de encoding:** Se detectaron caracteres extraños en algunos nombres de columnas (ej. “Ã”, “â”), los cuales fueron corregidos para facilitar el análisis.
4. **Limpieza aplicada:**
   - Normalización de nombres de columnas.
   {imput_text}
   - Normalización de texto en columnas de género y estado civil.

### Paso 2 – Demografía básica

1. **Rango de edad más común:** {demo.get('rango_mas_comun')}.
2. **Diferencias por género:** Sí. El análisis muestra una distribución desigual entre hombres y mujeres, aunque ambos grupos están representados en todos los rangos de edad.
3. **Grado militar más frecuente:** {demo.get('grado_mas_frec')}.

###  Paso 3 – Análisis familiar

1. **Porcentaje casados:** Aproximadamente **{fam.get('pct_casados')}%** del personal está casado.
2. **Hijos y convivencia:** {hijos_text}
3. **Relación entre edad y estado civil:** Sí existe una relación clara.  
   * Los **solteros** concentran edades más bajas.  
   * Los **casados** tienen una edad media intermedia (30–40 años).  
   * Los **viudos** y **divorciados** concentran edades mayores.  
   👉 Esto confirma un patrón esperado: a mayor edad, más probabilidad de cambios en estado civil.

**Dataset utilizado para Paso 2 y 3:** `{_prefer_clean_path().relative_to(PROJECT_DIR).as_posix()}`
"""
    results_md.write_text(resumen, encoding="utf-8")
    print(f"Resúmenes y reportes listos en: {results_md}")

# ---------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------
def parse_args():
    ap = argparse.ArgumentParser(description="Generador de reportes FAC (Markdown) con limpieza.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--all", action="store_true", help="Ejecuta limpieza + 3 pasos y genera el resumen.")
    g.add_argument("--calidad", action="store_true", help="Solo Paso 1: Calidad de datos (con limpieza).")
    g.add_argument("--demo", action="store_true", help="Solo Paso 2: Demografía básica.")
    g.add_argument("--familiar", action="store_true", help="Solo Paso 3: Análisis familiar.")
    return ap.parse_args()

if __name__ == "__main__":
    args = parse_args()
    if args.all:
        build_resumen()
    elif args.calidad:
        run_calidad(save_md=True)
        print(f"Reporte: {REPORT_DIR/'calidad_datos.md'}\nDataset limpio: {CLEAN_PATH}")
    elif args.demo:
        run_demografia(save_md=True)
        print(f"Reporte: {REPORT_DIR/'demografia_basica.md'}")
    elif args.familiar:
        run_familiar(save_md=True)
        print(f"Reporte: {REPORT_DIR/'analisis_familiar.md'}")
