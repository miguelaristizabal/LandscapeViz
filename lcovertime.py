import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
ClassMetrics = pd.read_csv("ClassMetrics.csv")

# Ensure the mapbiomas2legend dictionary is defined
mapbiomas2legend = {
    1: {"code": "1", "es": "Formación boscosa", "en": "Forest formation", "hex": "#1F8D49", "parent": None},
    3: {"code": "1.1", "es": "Bosque", "en": "Forest", "hex": "#1F8D49", "parent": 1},
    5: {"code": "1.2", "es": "Manglar", "en": "Mangrove", "hex": "#04381D", "parent": 1},
    6: {"code": "1.3", "es": "Bosque inundable", "en": "Flooded forest", "hex": "#026975", "parent": 1},
    49: {"code": "1.4", "es": "Vegetación leñosa sobre arena", "en": "Wooded sand vegetation", "hex": "#02D659", "parent": 1},

    10: {"code": "2", "es": "Formación natural no boscosa", "en": "Natural non-forest formation", "hex": "#D6BC74", "parent": None},
    11: {"code": "2.1", "es": "Formación natural no forestal inundable", "en": "Wetland", "hex": "#519799", "parent": 10},
    12: {"code": "2.2", "es": "Formación herbácea", "en": "Grasslands/herbaceous", "hex": "#D6BC74", "parent": 10},
    32: {"code": "2.3", "es": "Planicie de marea hipersalina", "en": "Hypersaline tidal flat", "hex": "#FC8114", "parent": 10},
    29: {"code": "2.4", "es": "Afloramiento rocoso", "en": "Rocky outcrop", "hex": "#FFAA5F", "parent": 10},
    50: {"code": "2.5", "es": "Vegetación herbácea sobre arena", "en": "Herbaceous sand vegetation", "hex": "#AD5100", "parent": 10},
    13: {"code": "2.6", "es": "Otra formación natural no forestal", "en": "Other non-forest formation", "hex": "#D89F5C", "parent": 10},

    14: {"code": "3", "es": "Área agropecuaria", "en": "Agricultural and livestock area", "hex": "#FFEFC3", "parent": None},
    9:  {"code": "3.1", "es": "Silvicultura", "en": "Forest plantation", "hex": "#7A5900", "parent": 14},
    35: {"code": "3.2", "es": "Palma aceitera", "en": "Palm oil", "hex": "#9065D0", "parent": 14},
    21: {"code": "3.3", "es": "Mosaico de agricultura y/o pasto", "en": "Mosaic of agriculture and pasture", "hex": "#FFEFC3", "parent": 14},

    22: {"code": "4", "es": "Área sin vegetación", "en": "Non-vegetated area", "hex": "#D4271E", "parent": None},
    23: {"code": "4.1", "es": "Playas, dunas y bancos de arena", "en": "Beach, dune and sand spot", "hex": "#FFA07A", "parent": 22},
    24: {"code": "4.2", "es": "Infraestructura urbana", "en": "Infrastructure", "hex": "#D4271E", "parent": 22},
    30: {"code": "4.3", "es": "Minería", "en": "Mining", "hex": "#9C0027", "parent": 22},
    68: {"code": "4.4", "es": "Otra área natural sin vegetación", "en": "Other natural, non-vegetated area", "hex": "#E97A7A", "parent": 22},
    25: {"code": "4.5", "es": "Otra área sin vegetación", "en": "Other non-vegetated area", "hex": "#DB4D4F", "parent": 22},

    26: {"code": "5", "es": "Cuerpo de agua", "en": "Water body", "hex": "#2532E4", "parent": None},
    33: {"code": "5.1", "es": "Río, lago u océano", "en": "River, lake or ocean", "hex": "#2532E4", "parent": 26},
    31: {"code": "5.2", "es": "Acuicultura", "en": "Aquaculture", "hex": "#091077", "parent": 26},
    34: {"code": "5.3", "es": "Glaciar y nival", "en": "Glacier", "hex": "#93DFE6", "parent": 26},

    27: {"code": "6", "es": "No observado", "en": "Not observed", "hex": "#FFFFFF", "parent": None}
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
