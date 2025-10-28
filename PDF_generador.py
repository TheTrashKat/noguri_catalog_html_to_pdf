from playwright.sync_api import sync_playwright
from PIL import Image
import os
import sys
import subprocess
import time

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
imagenes = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    for i in range(0, 5):
        page.goto(f"http://127.0.0.1:8080/?id={i}", wait_until="networkidle") 

        page.evaluate("""
        () => Promise.all(Array.from(document.images).map(img => {
            if (img.complete && img.naturalWidth) return true;
            return new Promise(res => {
                img.addEventListener('load', () => res(true), {once:true});
                img.addEventListener('error', () => res(true), {once:true});
            });
        }))
    """)
        page.pdf(path="salida.pdf", format="A4", print_background=True, scale=1)
        time.sleep(1)
        page.screenshot(path=str(i)+".png", full_page=True)
        imagenes.append(str(i)+".png")
        
    
    browser.close()
    imgs_a_pdf(imagenes)