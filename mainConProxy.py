from bs4 import BeautifulSoup
import os
import requests
from urllib.parse import urlparse, urljoin, unquote


def descargar_pagina(url, proxy=None):
    try:
        # Configurar el proxy si se proporciona
        if proxy:
            response = requests.get(url, proxies=proxy, timeout=15)
        else:
            response = requests.get(url)
        
        # Realizar la solicitud GET a la URL
        response = requests.get(url)
        
        # Verificar si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            # Establecer la codificación correcta para el contenido HTML
            response.encoding = response.apparent_encoding
            # Devolver el contenido HTML de la página
            return response.text
        else:
            # Si la solicitud no fue exitosa, imprimir el código de estado
            print(f"Error al descargar la página. Código de estado: {response.status_code}")
            return None
    except requests.RequestException as e:
        # Capturar excepciones de solicitud y mostrar un mensaje de error
        print(f"Error de solicitud: {e}")
        return None

def descargar_recursos(html, url_base, ruta_descarga):
    try:
        # Crear un objeto BeautifulSoup para analizar el HTML
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extraer todas las etiquetas <link> con el atributo 'href' (archivos CSS)
        for link_tag in soup.find_all('link', href=True):
            url_recurso = urljoin(url_base, link_tag['href'])  # Convertir la URL relativa a absoluta
            descargar_recurso(url_recurso, ruta_descarga)

        # Extraer todas las etiquetas <script> con el atributo 'src' (archivos JavaScript)
        for script_tag in soup.find_all('script', src=True):
            url_recurso = urljoin(url_base, script_tag['src'])  # Convertir la URL relativa a absoluta
            descargar_recurso(url_recurso, ruta_descarga)

        # Extraer todas las etiquetas <img> con el atributo 'src' (imágenes)
        for img_tag in soup.find_all('img', src=True):
            url_recurso = urljoin(url_base, img_tag['src'])  # Convertir la URL relativa a absoluta
            descargar_recurso(url_recurso, ruta_descarga)

        print("Recursos descargados correctamente.")
    except Exception as e:
        print(f"Error al descargar los recursos: {e}")



def descargar_recurso(url_recurso, ruta_descarga):
    try:
        # Realizar la solicitud GET para descargar el recurso
        response = requests.get(url_recurso)
        # Obtener la ruta relativa del recurso
        ruta_relativa = urlparse(url_recurso).path
        # Eliminar el primer carácter '/' de la ruta relativa si existe
        if ruta_relativa.startswith('/'):
            ruta_relativa = ruta_relativa[1:]
        # Convertir los caracteres especiales de la URL
        ruta_relativa = unquote(ruta_relativa)
        # Construir la ruta absoluta en el sistema de archivos local
        ruta_archivo = os.path.join(ruta_descarga, ruta_relativa)
        # Crear directorios si no existen
        ruta_directorio = os.path.dirname(ruta_archivo)
        if not os.path.exists(ruta_directorio):
            os.makedirs(ruta_directorio)
        # Guardar el recurso en un archivo local dentro del directorio correspondiente
        with open(ruta_archivo, 'wb') as archivo:
            archivo.write(response.content)
        print(f"Recurso descargado: {ruta_archivo}")
    except Exception as e:
        print(f"Error al descargar el recurso {url_recurso}: {e}")

# Solicitar al usuario la URL de la página web a descargar
url_pagina = input("Por favor, ingresa la URL de la pagina web que deseas descargar: ")
#url_pagina = "https://www.whatanicedaytobrowse.com/24QSBG/NFJT1XF/?source_id{affiliate_id}&sub1={transaction_id}"

# Solicitar al usuario la ruta donde desea descargar los archivos
ruta_descarga = input("Por favor, ingresa la ruta donde deseas descargar los archivos: ")
#ruta_descarga = "./pagina_descargada"

'''
#proxy_url = "http://170.64.222.86:8000"  # Configura tu proxy aquí
proxy_url = "103.131.232.11:8080"
proxy = {
    "http": proxy_url,
    "https": proxy_url
}'''

# Llamar a la función para descargar la página
#html_pagina = descargar_pagina(url_pagina, proxy)
html_pagina = descargar_pagina(url_pagina)
                               
# Verificar si se descargó correctamente y descargar los recursos asociados
if html_pagina:
    # Extraer la URL base de la página para construir URL absolutas
    url_base = urlparse(url_pagina).scheme + "://" + urlparse(url_pagina).netloc
    descargar_recursos(html_pagina, url_base, ruta_descarga)

    # Guardar el archivo HTML de la página en la ruta de destino especificada
    nombre_archivo_html = "index.html"
    ruta_archivo_html = os.path.join(ruta_descarga, nombre_archivo_html)
    with open(ruta_archivo_html, 'w', encoding='utf-8') as archivo_html:
        archivo_html.write(html_pagina)
    print(f"La página ha sido guardada correctamente en: {ruta_archivo_html}")
else:
    print("No se pudo descargar la página.")