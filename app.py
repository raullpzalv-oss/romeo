import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Plataforma Incidencias Ferroviarias", layout="wide")

st.title("Nueva Incidencia - MVP")

# Lista para almacenar incidencias (en memoria)
if "incidencias" not in st.session_state:
    st.session_state["incidencias"] = []

# -------------------------
# Formulario de incidencia
# -------------------------
with st.form("incidencia_form"):
    tipo = st.selectbox("Tipo de incidencia", [
        "Avería Infraestructura",
        "Avería Tren",
        "Meteorología adversa",
        "Orden público/Fuerza mayor",
        "Trabajos programados",
        "Operaciones"
    ])
    
    # Afectación territorial
    afectaciones = []
    num_afect = st.number_input("Número de líneas/Trayectos afectados", min_value=1, max_value=5, value=1)
    for i in range(int(num_afect)):
        st.markdown(f"**Afectación {i+1}**")
        linea = st.text_input(f"Línea {i+1}", value="R1", key=f"linea_{i}")
        trayecto = st.text_input(f"Trayecto {i+1}", value="Maçanet-Massanes - Arenys de Mar", key=f"trayecto_{i}")
        afectaciones.append({"line": linea, "route": trayecto})
    
    repercusion = st.selectbox("Repercusión", [
        "Afectación tren puntual",
        "Demoras leves en la línea",
        "Demoras graves en la línea",
        "Interrupción parcial del Servicio en la línea",
        "Interrupción total del Servicio en la línea"
    ])
    
    acciones = st.multiselect("Acciones", [
        "Comunicación con los usuarios",
        "Supresión parcial de servicios",
        "Trenes directos (Rodalies) con parada en todas las estaciones",
        "Trenes directos (Regionales) con parada en todas las estaciones",
        "PAT Bus",
        "PAT Otros transportes",
        "PAT Renfe Servicios Comerciales"
    ])
    
    resolucion = st.multiselect("Acciones para la resolución", [
        "Técnicos de Adif están trabajando para su resolución",
        "Por orden de Mossos/Bombers/Autoridad gobernativa"
    ])
    
    previsión = st.text_input("Previsión de solución", value="x minutos")
    
    descripcion = st.text_area("Descripción breve")
    
    submitted = st.form_submit_button("Crear incidencia")

# -------------------------
# Guardar y mostrar incidencia
# -------------------------
if submitted:
    incidencia = {
        "incidentId": f"INC-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "reportedAt": datetime.now().isoformat(),
        "type": tipo,
        "affectedTerritory": afectaciones,
        "repercussion": repercusion,
        "actionsTaken": acciones,
        "resolutionActions": resolucion,
        "expectedResolution": previsión,
        "description": descripcion
    }
    
    st.session_state["incidencias"].append(incidencia)
    
    st.success("✅ Incidencia creada!")
    st.json(incidencia)

# -------------------------
# Dashboard de incidencias
# -------------------------
st.header("Dashboard de Incidencias")
if st.session_state["incidencias"]:
    df = pd.DataFrame([{
        "ID": i["incidentId"],
        "Tipo": i["type"],
        "Repercusión": i["repercussion"],
        "Descripción": i["description"],
        "Fecha": i["reportedAt"]
    } for i in st.session_state["incidencias"]])
    
    st.table(df)
else:
    st.info("No hay incidencias creadas todavía.")
