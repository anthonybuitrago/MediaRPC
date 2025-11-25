import json
import os
import sys

# --- RUTAS DEL SISTEMA ---
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PATH_CONFIG = os.path.join(BASE_DIR, "config.json")
PATH_LOG = os.path.join(BASE_DIR, "stremio_log.txt")
PATH_ICON = os.path.join(BASE_DIR, "assets", "rpc.ico") # Asegurando ruta assets

# --- CONFIGURACIÓN POR DEFECTO ---
DEFAULT_CONFIG = {
    "client_id": "1441601634374385696",
    "update_interval": 5,
    "tolerance_seconds": 60,
    "blacklisted_words": [
        "1080p", "720p", "480p", "4k", "2160p", "hdrip", "web-dl", "bluray",
        "x265", "hevc", "aac", "h264", "webrip", "dual audio", "10bit",
        "anime time", "eng sub"
    ],
    "fixed_duration_minutes": 0
}

def cargar_config():
    """
    Carga la configuración de manera segura manejando errores específicos.
    """
    # 1. Verificar si el archivo existe
    if not os.path.exists(PATH_CONFIG):
        print(f"⚠️ Config no encontrada. Creando nueva en: {PATH_CONFIG}")
        guardar_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    try:
        with open(PATH_CONFIG, "r", encoding="utf-8") as f:
            datos = json.load(f)
            
            # Fusionar con default (por si agregamos opciones nuevas en el futuro)
            config_final = DEFAULT_CONFIG.copy()
            config_final.update(datos)
            return config_final

    except json.JSONDecodeError as e:
        print(f"❌ ERROR CRÍTICO: El archivo config.json está corrupto o mal formateado.")
        print(f"   Detalle: {e}")
        print("➡️ Cargando configuración por defecto temporalmente.")
        return DEFAULT_CONFIG

    except Exception as e:
        print(f"❌ Error inesperado leyendo config: {e}")
        return DEFAULT_CONFIG

def guardar_config(datos):
    """Guarda el diccionario en el archivo JSON con manejo de errores."""
    try:
        with open(PATH_CONFIG, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)
    except PermissionError:
        print("❌ Error: No tengo permisos para escribir en el archivo config.json")
    except Exception as e:
        print(f"❌ Error guardando configuración: {e}")