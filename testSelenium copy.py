import os
import time
import base64
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin, urlparse

# Configurar el servicio de ChromeDriver
chrome_driver_path = r"E:\Nueva carpeta\ChromeDriver\chromedriver-win64\chromedriver.exe"
service = Service(chrome_driver_path)

# Configurar las opciones del navegador para usar un proxy
proxy_url = "http://20.37.207.8:8080"  # Reemplaza con la dirección IP y el puerto de tu proxy
chrome_options = Options()
chrome_options.add_argument(f'--proxy-server={proxy_url}')

# Configurar tiempo de espera implícito a 20 segundos
#tiempo_espera_implícito = 10
driver = webdriver.Chrome(service=service, options=chrome_options)
#driver.implicitly_wait(tiempo_espera_implícito)

# URL de la página web a descargar
affiliate_id = "80"
transaction_id = "2"
#url_pagina = f"https://www.whatanicedaytobrowse.com/24QSBG/NFJT1XF/?source_id={affiliate_id}"
url_pagina = f"https://www.webalive.com.au/"

# Navegar a la página web
driver.get(url_pagina)

# Esperar un momento para que la página se cargue completamente
time.sleep(5)  # Puedes ajustar el tiempo de espera según sea necesario

# Obtener el HTML de la página después de que se haya generado dinámicamente
html_pagina = driver.page_source

# Crear un directorio para guardar los archivos descargados
ruta_descarga = "./google_descargado"
if not os.path.exists(ruta_descarga):
    os.makedirs(ruta_descarga)

# Guardar el archivo HTML de la página en la ruta de destino especificada
nombre_archivo_html = "index.html"
ruta_archivo_html = os.path.join(ruta_descarga, nombre_archivo_html)
with open(ruta_archivo_html, 'w', encoding='utf-8') as archivo_html:
    archivo_html.write(html_pagina)
print(f"El archivo HTML ha sido guardado correctamente en: {ruta_archivo_html}")

# Obtener los recursos (img, css, js) de la página
soup = BeautifulSoup(html_pagina, 'html.parser')

# Descargar imágenes, CSS y JavaScript
for tag in soup.find_all(["img", "link", "script"]):
    if tag.name == "img":
        src = tag.get("src")
        if src:
            img_url = urljoin(url_pagina, src)
            img_nombre = os.path.basename(img_url)
            img_path = os.path.join(ruta_descarga, "img", img_nombre)
            with open(img_path, "wb") as f:
                f.write(requests.get(img_url).content)
            print(f"Imagen guardada: {img_path}")
    elif tag.name == "link":
        href = tag.get("href")
        if href and href.endswith(".css"):
            css_url = urljoin(url_pagina, href)
            css_nombre = os.path.basename(css_url)
            css_path = os.path.join(ruta_descarga, "css", css_nombre)
            with open(css_path, "wb") as f:
                f.write(requests.get(css_url).content)
            print(f"Archivo CSS guardado: {css_path}")
    elif tag.name == "script":
        src = tag.get("src")
        if src and src.endswith(".js"):
            js_url = urljoin(url_pagina, src)
            js_nombre = os.path.basename(js_url)
            js_path = os.path.join(ruta_descarga, "js", js_nombre)
            with open(js_path, "wb") as f:
                f.write(requests.get(js_url).content)
            print(f"Archivo JavaScript guardado: {js_path}")

# Cerrar el navegador
driver.quit()
