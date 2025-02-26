import requests
import os
import sys

# Configuración
GITHUB_REPO = "https://github.com/Delpinoo/Inventario"
VERSION_FILE = "version.txt"
EXE_FILE = "InventaryTech.exe"

def obtener_version_local():
    """Lee la versión actual del programa"""
    return "1.0.0"  # Reemplázalo con la versión actual de tu programa

def obtener_version_remota():
    """Consulta la versión más reciente en GitHub"""
    try:
        response = requests.get(GITHUB_REPO + VERSION_FILE, timeout=5)
        if response.status_code == 200:
            return response.text.strip()
    except requests.RequestException:
        return None
    return None

def descargar_actualizacion():
    """Descarga la nueva versión y la reemplaza"""
    nueva_version = obtener_version_remota()
    if not nueva_version:
        print("⚠ No se pudo verificar la actualización.")
        return

    if nueva_version > obtener_version_local():
        print(f"📢 Nueva versión disponible: {nueva_version}")
        opcion = input("¿Deseas actualizar? (S/N): ").strip().lower()
        if opcion == "s":
            url = GITHUB_REPO + EXE_FILE
            try:
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    with open(EXE_FILE, "wb") as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
                    print("✅ Actualización completada. Reiniciando...")
                    os.execv(sys.executable, [sys.executable] + sys.argv)
                else:
                    print("⚠ No se pudo descargar la actualización.")
            except requests.RequestException:
                print("⚠ Error al descargar la actualización.")
    else:
        print("🚀 Ya tienes la última versión.")

# Verificar actualizaciones al inicio
descargar_actualizacion()
