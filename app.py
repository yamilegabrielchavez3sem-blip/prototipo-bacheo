import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# 1. El título de la página
st.title("Prioridad de mantenimiento vial")
st.caption("⚠️ Datos ilustrativos: son inventados para el prototipo.")

# 2. Inventamos 30 tramos de calle
rng = np.random.default_rng(1)   # "dado" que siempre da los mismos números
n = 30
df = pd.DataFrame({
    "tramo": [f"T{i+1}" for i in range(n)],
    "lat": rng.uniform(19.45, 19.65, n),    # posición norte-sur
    "lon": rng.uniform(-99.20, -99.00, n),  # posición este-oeste
    "zona": rng.choice([1, 2, 3], n),       # tipo de suelo (1, 2 o 3)
    "esals": rng.uniform(0.2, 1.0, n),      # cuánto tráfico pesado pasa
})

# 3. Qué tan débil es cada suelo (la zona 3 es la más débil)
ksuelo = {1: 1.0, 2: 1.2, 3: 1.5}
df["ksuelo"] = df["zona"].map(ksuelo)

# 4. Las dos barritas que mueve el usuario
lluvia = st.slider("Lluvia pronosticada en 72 h (mm)", 0, 100, 30)
umbral = st.slider("Umbral de alerta", 0.50, 0.95, 0.80)

# 5. Calculamos la probabilidad (fórmula inventada, solo para la demo)
puntaje = df["ksuelo"] * df["esals"] * lluvia / 40
df["P72h"] = 1 - np.exp(-puntaje)
df["alerta"] = df["P72h"] > umbral

# 6. Dibujamos el mapa
fig = px.scatter_map(
    df, lat="lat", lon="lon",
    color="P72h", size="esals",
    hover_name="tramo", zoom=10,
    color_continuous_scale="RdYlGn_r", range_color=(0, 1),
)
fig.update_layout(map_style="open-street-map")
st.plotly_chart(fig, use_container_width=True)

# 7. La tabla de alertas
st.subheader("Tramos en alerta")
alertas = df[df["alerta"]].sort_values("P72h", ascending=False)
st.dataframe(alertas[["tramo", "zona", "P72h"]])
