
---
# 🚴‍♂️ EDA y Modelado - Bicis Madrid

Este proyecto realiza un análisis exploratorio de datos (EDA) y una comparación de modelos de predicción del número de viajes en bicicleta en la ciudad de Madrid. Incluye una aplicación interactiva con Streamlit y un cuaderno en Jupyter donde se evalúan dos enfoques predictivos: **XGBoostRegressor** y **SARIMAX**.

---

## 📦 Contenido del repositorio

```
eda_demand_prediction_BiciMad/
├── app.py                  # Aplicación Streamlit para análisis exploratorio
├── eda_modelos.ipynb       # Jupyter Notebook: comparación entre XGBoost y SARIMAX
├── data/
│   └── data_viajes.csv     # Datos de uso de bicicletas en Madrid del año 2022
├── requirements.txt        # Librerías necesarias
└── README.md               # Este archivo
```

---

## 🧪 Tecnologías utilizadas

- Python 3.8+
- Streamlit
- Pandas / NumPy
- Seaborn / Matplotlib / PyDeck
- XGBoost
- statsmodels (SARIMAX)
- Scikit-learn

---

## 🚀 Cómo ejecutar el proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/eda_demand_prediction_BiciMad.git
cd eda_demand_prediction_BiciMad
```

### 2. Instalar las dependencias

```bash
pip install -r requirements.txt
```

> 💡 Recomendado: usar un entorno virtual con `venv` o `conda`.

### 3. Colocar los datos

Guarda el archivo `data_viajes.csv` dentro de la carpeta `data/`.

### 4. Ejecutar la aplicación de Streamlit

```bash
streamlit run app.py
```

### 5. Ejecutar el análisis de modelos

Abre el archivo `BiciMad.ipynb` en JupyterLab o VSCode y sigue los pasos para comparar:

- Predicción del número de viajes diarios
- Métricas de rendimiento (RMSE, MAE, etc.)
- Visualización de predicciones

---

## 📊 Contenido visualizado en `app.py`

- 📈 Evolución diaria de viajes
- 🕒 Duración media por día de la semana
- 🛴 Distribución por tipo de flota y tipo de anclaje
- 🌦️ Viajes medios por estación y día
- ⏰ Distribución horaria estacional
- 🗺️ Mapa de calor de ubicaciones (con PyDeck)

---

## 🤖 Comparación de modelos (`BiciMad.ipynb`)

Se entrenan y comparan dos enfoques de predicción del número de viajes diarios:

| Modelo             | Descripción                                          |
|--------------------|------------------------------------------------------|
| XGBoostRegressor   | Modelo supervisado de boosting para regresión        |
| SARIMAX            | Modelo estadístico                                   |

Se evalúan usando métricas como RMSE y se comparan las curvas de predicción frente a los datos reales.

---

## ⚠️ Notas

- Asegúrate de que las columnas en el CSV están bien nombradas: `unlock_date`, `trip_minutes`, `idBike`, `geolocation_unlock`, etc.

---

## ✍️ Autor

Desarrollado por **Diego Puerta Martín ** como parte de un proyecto de análisis de datos y predicción del uso de bicicletas en Madrid.

---

## 📜 Licencia
GNU GENERAL PUBLIC LICENSE
