from bs4 import BeautifulSoup
import os
import requests
from urllib.parse import urlparse, urljoin, unquote

def descargar_pagina(url):
    try:
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

def descargar_recursos(html, url_base):
    try:
        # Crear un objeto BeautifulSoup para analizar el HTML
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extraer todas las etiquetas <link> con el atributo 'href' (archivos CSS)
        for link_tag in soup.find_all('link', href=True):
            url_recurso = urljoin(url_base, link_tag['href'])  # Convertir la URL relativa a absoluta
            descargar_recurso(url_recurso)

        # Extraer todas las etiquetas <script> con el atributo 'src' (archivos JavaScript)
        for script_tag in soup.find_all('script', src=True):
            url_recurso = urljoin(url_base, script_tag['src'])  # Convertir la URL relativa a absoluta
            descargar_recurso(url_recurso)

        # Extraer todas las etiquetas <img> con el atributo 'src' (imágenes)
        for img_tag in soup.find_all('img', src=True):
            url_recurso = urljoin(url_base, img_tag['src'])  # Convertir la URL relativa a absoluta
            descargar_recurso(url_recurso)

        # Extraer todas las etiquetas <video> con el atributo 'src' (videos)
        for video_tag in soup.find_all('video', src=True):
            url_video = urljoin(url_base, video_tag['src'])  # Convertir la URL relativa a absoluta
            descargar_recurso(url_video)

            # Si hay múltiples fuentes de video, también las descargamos
            for source_tag in video_tag.find_all('source', src=True):
                url_recurso = urljoin(url_base, source_tag['src'])  # Convertir la URL relativa a absoluta
                descargar_recurso(url_recurso)

        print("Recursos descargados correctamente.")
    except Exception as e:
        print(f"Error al descargar los recursos: {e}")

def descargar_recurso(url_recurso):
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
        ruta_archivo = os.path.join(os.getcwd(), ruta_relativa)
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

# URL de la página web a descargar
url_pagina = "https://cozy-strudel-510fd4.netlify.app/"

# Llamar a la función para descargar la página
html_pagina = descargar_pagina(url_pagina)

# Verificar si se descargó correctamente y descargar los recursos asociados
if html_pagina:
    # Extraer la URL base de la página para construir URL absolutas
    url_base = urlparse(url_pagina).scheme + "://" + urlparse(url_pagina).netloc
    descargar_recursos(html_pagina, url_base)

    # Guardar el archivo HTML de la página directamente en el directorio actual
    with open("index.html", 'w', encoding='utf-8') as archivo_html:
        archivo_html.write(html_pagina)

else:
    print("No se pudo descargar la página.")
