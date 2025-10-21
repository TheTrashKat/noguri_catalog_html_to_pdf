from playwright.sync_api import sync_playwright
from PIL import Image
import os
import sys
import subprocess


def install(package):
    """Instala un paquete usando pip si no está instalado."""
    try:
        __import__(package)
        print(f"✅ {package} ya está instalado.")
    except ImportError:
        print(f"📦 Instalando {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# 1️⃣ Instalar dependencias principales
install("playwright")
install("Pillow")

# 2️⃣ Instalar navegadores de Playwright (solo la primera vez)
try:
    from playwright.sync_api import sync_playwright
    print("🌐 Instalando Chromium para Playwright...")
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    print("✅ Chromium instalado correctamente.")
except Exception as e:
    print("⚠️ No se pudo instalar Chromium automáticamente:", e)

print("\\n✅ Entorno listo. Puedes usar ahora:")
print("   from playwright.sync_api import sync_playwright")
print("   from PIL import Image")
print("\\n👉 Ejemplo para ejecutar tu script:")
print("   python tu_script.py")

def imgs_a_pdf(lista_imgs, salida_pdf="salida.pdf"):
    # Abrir todas las imágenes
    imagenes = [Image.open(img).convert("RGB") for img in lista_imgs]
    
    # Guardar todas en un solo PDF
    imagenes[0].save(
        salida_pdf, 
        save_all=True, 
        append_images=imagenes[1:]
    )
    print(f"✅ PDF generado correctamente: {salida_pdf}")

# Ejemplo de uso
imagenes = [
    "1.png",
    "1.png",
    "1.png"
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 2560, "height": 1440})
    page.goto("file:///D:/proyecto/GIT/noguri_catalog_html_to_pdf/index.html")
    page.pdf(path="salida.pdf", format="A4", print_background=True)
    page.screenshot(path="1.png", full_page=True)
    browser.close()
    imgs_a_pdf(imagenes)
    




