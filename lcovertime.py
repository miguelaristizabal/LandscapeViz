import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure the mapbiomas2legend dictionary is defined
mapbiomas2legend = {
    1: {"code": "1", "es": "Formación boscosa", "en": "Forest formation", "hex": "#1F8D49", "parent": None},
    3: {"code": "1.1", "es": "Bosque", "en": "Forest", "hex": "#1F8D49", "parent": 1},
    # Add the remaining entries...
}

# Define the plot function
def plot_stacked_pland(ClassMetrics, localidad, buffer_radius, mapbiomas2legend):
    filtered_df = ClassMetrics[
        (ClassMetrics["Localidad"] == localidad) & 
        (ClassMetrics["BufferRadius"] == buffer_radius)
    ]
    pivot_df = filtered_df.pivot(index="Year", columns="LC", values="PLAND_Rescaled").fillna(0)
    if mapbiomas2legend:
        pivot_df = pivot_df[sorted(pivot_df.columns, key=lambda x: list(mapbiomas2legend.keys()).index(x))]
    class_labels = [mapbiomas2legend[cls]["es"] for cls in pivot_df.columns]
    plt.figure(figsize=(14, 8))
    plt.stackplot(
        pivot_df.index,
        pivot_df.T.values,
        labels=class_labels,
        colors=[mapbiomas2legend[cls]["hex"] for cls in pivot_df.columns],
        alpha=0.8
    )
    plt.title(f"Dinámica de Coberturas de Suelo ({localidad}, {buffer_radius}m)", fontsize=16, weight="bold")
    plt.xlabel("Año", fontsize=14)
    plt.ylabel("Porcentaje (%)", fontsize=14)
    plt.legend(loc="upper left", title="Clases de Cobertura", fontsize=12, title_fontsize=14, bbox_to_anchor=(1, 1))
    sns.despine()
    plt.grid(visible=True, linestyle="--", alpha=0.6)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    st.pyplot(plt)

# Streamlit App UI
st.title("Dinámica de Coberturas de Suelo")

# File uploader
uploaded_file = st.file_uploader("Cargue el archivo ClassMetrics CSV", type="csv")

if uploaded_file is not None:
    ClassMetrics = pd.read_csv(uploaded_file)
    
    # Sidebar Filters
    localidades = ClassMetrics["Localidad"].unique()
    localidad = st.sidebar.selectbox("Seleccione la Localidad", localidades)

    buffer_radii = ClassMetrics["BufferRadius"].unique()
    buffer_radius = st.sidebar.selectbox("Seleccione el Radio de Búfer (m)", buffer_radii)

    # Main Visualization
    st.subheader(f"Dinámica de Coberturas de Suelo para {localidad} ({buffer_radius}m)")
    plot_stacked_pland(ClassMetrics, localidad, buffer_radius, mapbiomas2legend)
