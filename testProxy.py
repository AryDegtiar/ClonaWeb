import requests

# URL de la página web a descargar
url_pagina = "https://www.whatanicedaytobrowse.com/24QSBG/NFJT1XF/?source_id{affiliate_id}&sub1={transaction_id}"
#url_pagina = "https://www.google.com"

# Configuración del proxy
proxy_url = "http://170.64.222.86:8000"  # Reemplaza "your_proxy_ip" y "port" con la dirección IP y el puerto de tu proxy
proxy = {
    "http": proxy_url,
    "https": proxy_url
}

try:
    # Realizar la solicitud GET a la URL utilizando el proxy
    response = requests.get(url_pagina, proxies=proxy, timeout=15)  # Aumenta el tiempo de espera a 10 segundos

    
    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Establecer la codificación correcta para el contenido HTML
        response.encoding = response.apparent_encoding
        # Obtener el contenido HTML de la página
        html_pagina = response.text
        print("Página descargada correctamente.")
        print(html_pagina)
        # Aquí puedes continuar con el procesamiento de la página descargada
    else:
        # Si la solicitud no fue exitosa, imprimir el código de estado
        print(f"Error al descargar la página. Código de estado: {response.status_code}")
except requests.RequestException as e:
    # Capturar excepciones de solicitud y mostrar un mensaje de error
    print(f"Error de solicitud: {e}")
