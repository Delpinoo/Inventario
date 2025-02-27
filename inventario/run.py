import os
import subprocess
import requests
import sys
import zipfile
import time
import threading
import webview
import ctypes

# Configuración
ruta_instalacion = os.path.dirname(os.path.abspath(__file__))  # Ruta del directorio donde está el script
db_path = os.path.join(ruta_instalacion, "db.sqlite3")

GITHUB_REPO = "https://raw.githubusercontent.com/Delpinoo/Inventario/main/"  # URL base de GitHub
VERSION_FILE = "inventario/version.txt"  # Archivo de versión en GitHub
ZIP_FILE = "update.zip"  # Archivo ZIP con la actualización
EXTRACT_PATH = ruta_instalacion  # Ahora usa la ruta de instalación dinámica
TEMPLATES_DIR = os.path.join(ruta_instalacion, "app", "templates")
STATIC_DIR = os.path.join(ruta_instalacion, "app", "static")


def print_utf8(text):
    sys.stdout.buffer.write((text + "\n").encode("utf-8"))
    sys.stdout.flush()

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


def descargar_y_extraer_actualizacion():
    """Descarga y extrae la nueva versión si es necesario"""
    nueva_version = obtener_version_remota()
    if not nueva_version:
        print_utf8("⚠ No se pudo verificar la actualización.")
        return

    if nueva_version > obtener_version_local():
        print_utf8(f"📢 Nueva versión disponible: {nueva_version}")
        opcion = input("¿Deseas actualizar? (S/N): ").strip().lower()
        if opcion == "s":
            url = GITHUB_REPO + ZIP_FILE
            try:
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    zip_path = os.path.join(EXTRACT_PATH, ZIP_FILE)
                    with open(zip_path, "wb") as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
                    print_utf8("✅ Descarga completada. Extrayendo...")
                    with zipfile.ZipFile(zip_path, "r") as zip_ref:
                        zip_ref.extractall(EXTRACT_PATH)
                    os.remove(zip_path)
                    print_utf8("✅ Actualización completada. Reiniciando...")
                    os.execv(sys.executable, [sys.executable] + sys.argv)
                else:
                    print_utf8("⚠ No se pudo descargar la actualización.")
            except requests.RequestException:
                print_utf8("⚠ Error al descargar la actualización.")
    else:
        print_utf8("🚀 Ya tienes la última versión.")


# Verificar actualizaciones al inicio
descargar_y_extraer_actualizacion()


# Iniciar el servidor de Django en un hilo separado
def run_django():
    os.environ["DJANGO_SETTINGS_MODULE"] = "inventario.settings"
    python_exe = os.path.join(ruta_instalacion, "python_embedded", "python.exe")
    print_utf8(f"🐍 Usando Python en: {python_exe}")

    try:
        print_utf8("🛠 Ejecutando Django...")
        creation_flags = 0
        if sys.platform == "win32":  # Solo en Windows oculta la consola
            creation_flags = subprocess.CREATE_NO_WINDOW


        django_project_path = os.path.join(ruta_instalacion, "inventario")
        
        process = subprocess.Popen(
            [python_exe, "-m", "django", "runserver", "127.0.0.1:8000", "--noreload"],
            cwd=django_project_path,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            creationflags=creation_flags  # 🔹 Esta línea evita que se abra la consola
        )

        # Imprimir logs del servidor
        for line in process.stdout:
            print_utf8(line)

        process.wait()

    except Exception as e:
        print_utf8(f"\n❌ Error al ejecutar Django:\n{e}")


# Lanzar Django en un hilo
django_thread = threading.Thread(target=run_django, daemon=True)
django_thread.start()

# Cambiar el icono de la ventana en Windows
if sys.platform == "win32":
    myappid = "inventarytech.app"  # Identificador único de la app
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # Cambiar el ícono de la ventana
    import win32gui
    import win32con

    def set_window_icon():
        hwnd = win32gui.GetForegroundWindow()
        icon_path = os.path.abspath("icon_app.ico")
        if os.path.exists(icon_path):
            hicon = win32gui.LoadImage(0, icon_path, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE)
            win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_SMALL, hicon)
            win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, hicon)

# Esperar unos segundos para asegurarse de que el servidor de Django arranque antes de abrir la ventana
time.sleep(5)

# Abre la ventana de la aplicación con PyWebView
print_utf8("🖥 Abriendo la ventana de InventaryTech...")
webview.create_window("InventaryTech", "http://127.0.0.1:8000", width=1000, height=700)
webview.start(set_window_icon)
