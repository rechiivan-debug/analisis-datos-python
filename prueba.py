import requests
import pandas as pd

# Varias ciudades con sus coordenadas
ciudades = [
    {'nombre': 'Monterrey', 'lat': 25.67, 'lon': -100.31},
    {'nombre': 'CDMX', 'lat': 19.43, 'lon': -99.13},
    {'nombre': 'Guadalajara', 'lat': 20.67, 'lon': -103.35},
    {'nombre': 'Tijuana', 'lat': 32.53, 'lon': -117.03},
]

resultados = []  # lista vacía para acumular

for ciudad in ciudades:
    url = (f"https://api.open-meteo.com/v1/forecast"
           f"?latitude={ciudad['lat']}"
           f"&longitude={ciudad['lon']}"
           f"&current_weather=true")

    respuesta = requests.get(url)
    clima = respuesta.json()['current_weather']
    clima['ciudad'] = ciudad['nombre']  # agregar nombre
    resultados.append(clima)

# Convertir lista a DataFrame
df = pd.DataFrame(resultados)
df = df[['ciudad', 'temperature', 'windspeed', 'time']]

print(df)
df.to_csv('clima_ciudades.csv', index=False)
print("✅ Guardado!")