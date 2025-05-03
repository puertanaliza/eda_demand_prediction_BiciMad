import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pydeck as pdk

# Configuración
st.set_page_config(page_title="EDA Bicis Madrid", layout="wide")
st.title("📊 Análisis Exploratorio de Datos - Bicicletas Madrid")

# Cargo datos
@st.cache_data
def load_data():
    df = pd.read_csv('data_viajes.csv', parse_dates=['fecha', 'unlock_date'])
    # Convertir campos si no están
    if 'geolocation_lock' in df.columns:
        df[['lat', 'lon']] = df['geolocation_lock'].str.extract(r"\((.*), (.*)\)").astype(float)
    df['hour'] = df['unlock_date'].dt.hour
    df['hour'] = df['hour'].astype(int)
    return df

df = load_data()

# Derivo variables
df_daily = df.groupby('fecha').agg(
    trips_count=('idBike', 'count'),
    avg_trip_minutes=('trip_minutes', 'mean')
).reset_index()
df_daily['day_of_week'] = df_daily['fecha'].dt.day_name()

# Estación del año
def get_season(date):
    month = date.month
    if month in [12, 1, 2]: return 'Winter'
    elif month in [3, 4, 5]: return 'Spring'
    elif month in [6, 7, 8]: return 'Summer'
    else: return 'Autumn'

df_daily['season'] = df_daily['fecha'].apply(get_season)
df['season'] = df['fecha'].apply(get_season)

# ---------- Gráficos ----------
st.subheader("📈 Evolución diaria de viajes")
fig1, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(df_daily['fecha'], df_daily['trips_count'], color='steelblue')
ax1.set(title='Número de viajes diarios', xlabel='Fecha', ylabel='Viajes')
ax1.grid(True)
st.pyplot(fig1)

st.subheader("🕒 Duración media por día de la semana")
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.boxplot(x='day_of_week', y='avg_trip_minutes', data=df_daily,
            order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ax=ax2)
ax2.set(title='Duración media de viaje', xlabel='Día de la semana', ylabel='Minutos')
ax2.grid(True)
st.pyplot(fig2)

st.subheader("🛴 Distribución por tipo de flota y tipo de anclaje")
col1, col2 = st.columns(2)
with col1:
    fig3, ax3 = plt.subplots()
    sns.countplot(x='fleet', data=df, ax=ax3)
    ax3.set(title='Tipo de flota')
    ax3.grid(True)
    st.pyplot(fig3)
with col2:
    fig4, ax4 = plt.subplots()
    sns.countplot(x='locktype', data=df, ax=ax4)
    ax4.set(title='Tipo de bloqueo')
    ax4.grid(True)
    st.pyplot(fig4)

st.subheader("🌦️ Viajes medios por estación y día de la semana")
pivot1 = df_daily.pivot_table(index='season', columns='day_of_week', values='trips_count', aggfunc='mean')
pivot1 = pivot1.reindex(index=['Winter', 'Spring', 'Summer', 'Autumn'])
pivot1 = pivot1[['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']]
fig5, ax5 = plt.subplots(figsize=(10, 6))
sns.heatmap(pivot1, cmap='YlGnBu', ax=ax5)
ax5.set(title='Viajes diarios medios', xlabel='Día', ylabel='Estación')
st.pyplot(fig5)

st.subheader("⏰ Viajes medios por estación y hora")
df_hour = df.groupby(['hour', 'season']).agg(
    trips_count=('idBike', 'count')
).reset_index()
pivot2 = df_hour.pivot_table(index='season', columns='hour', values='trips_count', aggfunc='mean')
pivot2 = pivot2.reindex(index=['Winter', 'Spring', 'Summer', 'Autumn'])
fig6, ax6 = plt.subplots(figsize=(12, 5))
sns.heatmap(pivot2, cmap='YlGnBu', ax=ax6)
ax6.set(title='Viajes por hora del día', xlabel='Hora', ylabel='Estación')
st.pyplot(fig6)

# ---------- Mapa de calor ----------
sample_df = df.sample(10000, random_state=1)  # Muestra aleatoria de 10000 filas

# Extraigo latitud y longitud de la columna geolocation_unlock
sample_df['lat'] = sample_df['geolocation_unlock'].apply(lambda x: eval(x)['coordinates'][1] if isinstance(x, str) else None)
sample_df['lon'] = sample_df['geolocation_unlock'].apply(lambda x: eval(x)['coordinates'][0] if isinstance(x, str) else None)
sample_df = sample_df.groupby(['lat','lon']).agg(
    trips_count=('idBike', 'count')
).reset_index()
sample_df['lat'] = sample_df['lat'].astype(float)
sample_df['lon'] = sample_df['lon'].astype(float)
sample_df = sample_df.dropna(subset=['lat', 'lon', 'trips_count'])

sample_df = sample_df[(sample_df['lat'] != 0.0) & (sample_df['lon'] != 0.0)]

# Ahora, me aseguro de que las columnas lat y lon existan antes de continuar
if 'lat' in sample_df.columns and 'lon' in sample_df.columns:
    st.subheader("🗺️ Mapa de calor de demanda por ubicación de anclaje")

    # Visualización del mapa de calor usando pydeck
    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=40.4168,  # Coordenadas de Madrid
            longitude=-3.7038,
            zoom=12,
            pitch=20,
        ),
        layers=[
            pdk.Layer(
                "HeatmapLayer",
                data=sample_df[['lat', 'lon', 'trips_count']],  # Uso las columnas lat y lon extraídas
                get_position='[lon, lat]',  # Defino el formato de las coordenadas
                radius_pixels=60,
                get_weight="trips_count",
            )
        ],
    ))
else:
    st.warning("No se encontró la columna `geolocation_unlock` o no tiene formato adecuado para mostrar el mapa.")

# ---------- Fin ----------
st.markdown("---")
st.caption("Desarrollado por Diego | Datos reales de bicis en Madrid")
