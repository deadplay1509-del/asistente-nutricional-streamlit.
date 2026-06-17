import requests

# 1. La dirección web (URL) de la API pública de CoinGecko
url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

print("📡 Conectando con los servidores de la API...")

# 2. Hacemos la petición en vivo a internet (Método GET)
respuesta = requests.get(url)

# 3. Transformamos la respuesta en un formato JSON (que es como un diccionario de Python)
datos = respuesta.json()

# 4. Extraemos el precio exacto metiéndonos en las llaves del JSON
precio_bitcoin = datos["bitcoin"]["usd"]

# --- NUEVA PRUEBA ---
print("Objeto JSON completo recibido del servidor:")
print(datos)