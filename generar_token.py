import requests

# Endpoint oficial para generar tokens
url = "https://api.mercadolibre.com/oauth/token"

payload = {
    "grant_type": "authorization_code",
    "client_id": "3921311743973275",
    # Pegá acá el Client Secret que me mostraste en tu 4ta foto (el que empieza con zeDt...)
    "client_secret": "ACA_VA_TU_CLIENT_SECRET",
    # Pegá acá el código TG- que copiaste de la URL de Google en el Paso 1
    "code": "TG-69e04906e6cc2e00010ffab5-80886052&zx=1776306441590",
    "redirect_uri": "https://www.google.com"
}

headers = {
    "accept": "application/json",
    "content-type": "application/x-www-form-urlencoded"
}

print("Generando llave maestra...")
respuesta = requests.post(url, data=payload, headers=headers)

if respuesta.status_code == 200:
    datos = respuesta.json()
    print("\n✅ ¡ÉXITO! ESTE ES TU ACCESS TOKEN (Empieza con APP_USR):")
    print("-" * 50)
    print(datos.get("access_token"))
    print("-" * 50)
    print("Copiá este texto y pegalo en tu archivo app.py")
else:
    print(f"❌ Error {respuesta.status_code}: {respuesta.text}")
