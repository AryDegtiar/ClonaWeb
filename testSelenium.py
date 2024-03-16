import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import requests

# Configurar el servicio de ChromeDriver
chrome_driver_path = r"E:\Nueva carpeta\ChromeDriver\chromedriver-win64\chromedriver.exe"
service = Service(chrome_driver_path)

# Iniciar el navegador Chrome
driver = webdriver.Chrome(service=service)

# URL de la página web a descargar
url_pagina = "https://www.bbva.com.ar/"

# Navegar a la página de Google
driver.get(url_pagina)

# Esperar unos segundos para que la página se cargue completamente
time.sleep(5)

# Obtener el HTML de la página después de que se haya generado dinámicamente
html_pagina = driver.page_source

# Crear un directorio para guardar los archivos descargados
ruta_descarga = "./google_descargado"
if not os.path.exists(ruta_descarga):
    os.makedirs(ruta_descarga)

# Parsear el HTML con BeautifulSoup
soup = BeautifulSoup(html_pagina, 'html.parser')

# Crear subdirectorios para imágenes, CSS y JavaScript
subdirectorios = ['img', 'css', 'js']
for subdir in subdirectorios:
    subdir_path = os.path.join(ruta_descarga, subdir)
    if not os.path.exists(subdir_path):
        os.makedirs(subdir_path)

# Descargar imágenes, CSS y JavaScript
for tag in soup.find_all(['img', 'link', 'script']):
    if tag.name == 'img' and tag.get('src'):
        src = tag['src']
        img_url = urljoin(url_pagina, src)
        img_name = os.path.basename(urlparse(img_url).path)
        img_path = os.path.join(ruta_descarga, 'img', img_name)
        try:
            response = requests.get(img_url)
            response.raise_for_status()  # Verificar si hay errores al descargar la imagen
            with open(img_path, 'wb') as f:
                f.write(response.content)
            # Actualizar la referencia en el HTML
            tag['src'] = os.path.join('img', img_name)
        except Exception as e:
            print(f"Error al descargar imagen {img_url}: {e}")
    elif tag.name == 'link' and tag.get('href') and tag['href'].endswith('.css'):
        href = tag['href']
        css_url = urljoin(url_pagina, href)
        css_name = os.path.basename(urlparse(css_url).path)
        css_path = os.path.join(ruta_descarga, 'css', css_name)
        try:
            response = requests.get(css_url)
            response.raise_for_status()  # Verificar si hay errores al descargar el archivo CSS
            with open(css_path, 'wb') as f:
                f.write(response.content)
            # Actualizar la referencia en el HTML
            tag['href'] = os.path.join('css', css_name)
        except Exception as e:
            print(f"Error al descargar CSS {css_url}: {e}")
    elif tag.name == 'script' and tag.get('src') and tag['src'].endswith('.js'):
        src = tag['src']
        js_url = urljoin(url_pagina, src)
        js_name = os.path.basename(urlparse(js_url).path)
        js_path = os.path.join(ruta_descarga, 'js', js_name)
        try:
            response = requests.get(js_url)
            response.raise_for_status()  # Verificar si hay errores al descargar el archivo JavaScript
            with open(js_path, 'wb') as f:
                f.write(response.content)
            # Actualizar la referencia en el HTML
            tag['src'] = os.path.join('js', js_name)
        except Exception as e:
            print(f"Error al descargar JavaScript {js_url}: {e}")

# Guardar el archivo HTML modificado
nombre_archivo_html = "index.html"
ruta_archivo_html = os.path.join(ruta_descarga, nombre_archivo_html)
with open(ruta_archivo_html, 'w', encoding='utf-8') as archivo_html:
    archivo_html.write(str(soup))

# Cerrar el navegador
driver.quit()

print(f"El archivo HTML ha sido guardado correctamente en: {ruta_archivo_html}")
