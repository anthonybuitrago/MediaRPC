import time
import re
import requests
import urllib.parse
import os
import sys
import subprocess
from config_manager import PATH_LOG

def log(mensaje):
    """Escribe mensajes en el archivo de registro y en consola."""
    texto = f"[{time.strftime('%H:%M:%S')}] {mensaje}"
    try:
        print(texto)
        with open(PATH_LOG, "a", encoding="utf-8") as f:
            f.write(texto + "\n")
    except: pass

def gestionar_logs():
    try:
        if os.path.exists(PATH_LOG) and os.path.getsize(PATH_LOG) > 1 * 1024 * 1024:
            with open(PATH_LOG, "w", encoding="utf-8") as f:
                f.write(f"[{time.strftime('%H:%M:%S')}] 🧹 Log limpiado automáticamente.\n")
    except: pass

# --- LIMPIEZA DE NOMBRE (SMART CUT V38.1) ---
def extraer_datos_video(nombre_crudo):
    """
    Devuelve una tupla: (nombre_limpio, tipo_detectado)
    tipo_detectado puede ser: 'serie', 'peli', o 'auto'
    """
    if not nombre_crudo or str(nombre_crudo).lower() == "none":
        return None, "auto"

    nombre = nombre_crudo.replace(".", " ")
    nombre = re.sub(r'\[.*?\]', '', nombre)
    nombre = re.sub(r'\(.*?\)', '', nombre)
    
    tipo_detectado = "auto" # Por defecto no sabemos

    # 1. BUSCAR EPISODIO (PRIORIDAD MÁXIMA)
    # S01E01, 1x01, o " - 01 " (típico anime)
    match_episodio = re.search(r'( S\d+E\d+ | \d+x\d+ | [ \-_]0?(\d{1,4})(?:[ \-_\[\.]) )', nombre, re.IGNORECASE)
    
    # 2. BUSCAR SOLO TEMPORADA (NUEVO: "S01" sin episodio)
    match_temporada = re.search(r'( S\d{1,2} | Season \d{1,2} )', nombre, re.IGNORECASE)

    # 3. BUSCAR AÑO
    match_anio = re.search(r'\b(19\d{2}|20\d{2})\b', nombre)

    if match_episodio:
        # Si tiene episodio, ES SERIE
        tipo_detectado = "serie"
        indice = match_episodio.start()
        nombre = nombre[:indice]
        
    elif match_temporada:
        # Si tiene "S01" pero no episodio, ES SERIE (Fix Made in Abyss)
        tipo_detectado = "serie"
        indice = match_temporada.start()
        nombre = nombre[:indice]

    elif match_anio:
        # Si tiene año Y NO TIENE NADA DE ARRIBA, es Peli
        tipo_detectado = "peli"
        indice = match_anio.end()
        nombre = nombre[:indice]
    
    nombre = nombre.replace("mkv", "").replace("mp4", "").replace("avi", "")
    nombre = re.sub(r'\s+', ' ', nombre).strip()
    nombre = nombre.strip(".-_ ")

    if len(nombre) < 2: return "Stremio", "auto"
    return nombre, tipo_detectado

def formato_velocidad(bytes_sec):
    try:
        if bytes_sec > 1024 * 1024:
            return f"{bytes_sec / (1024 * 1024):.1f} MB/s"
        elif bytes_sec > 1024:
            return f"{bytes_sec / 1024:.0f} KB/s"
        else:
            return "0 KB/s"
    except: return "0 KB/s"

def extraer_minutos(texto_runtime):
    try:
        numeros = re.findall(r'\d+', str(texto_runtime))
        if numeros: return int(numeros[0])
    except: pass
    return 0

def obtener_metadatos(nombre_busqueda, tipo_forzado="auto"):
    datos = {"poster": "stremio_logo", "runtime": 0, "name": nombre_busqueda}
    
    if not nombre_busqueda or nombre_busqueda == "Stremio" or nombre_busqueda == "None": 
        return datos
    
    try:
        query = urllib.parse.quote(nombre_busqueda)
        
        # FUNCIÓN AUXILIAR PARA BUSCAR
        def buscar_en(tipo_api):
            url = f"https://v3-cinemeta.strem.io/catalog/{tipo_api}/top/search={query}.json"
            resp = requests.get(url, timeout=2)
            data = resp.json()
            if 'metas' in data and len(data['metas']) > 0:
                item = data['metas'][0]
                datos["poster"] = item.get('poster', 'stremio_logo')
                datos["runtime"] = extraer_minutos(item.get('runtime', 0))
                datos["name"] = item.get('name', nombre_busqueda)
                return True
            return False

        # LÓGICA DE PRIORIDAD
        if tipo_forzado == "serie":
            # Si sabemos que es serie, buscamos SOLO series primero
            if buscar_en("series"): return datos
            if buscar_en("movie"): return datos # Respaldo
            
        elif tipo_forzado == "peli":
            # Si sabemos que es peli
            if buscar_en("movie"): return datos
            if buscar_en("series"): return datos
            
        else:
            # Si no sabemos (auto), probamos los dos
            if buscar_en("movie"): return datos
            if buscar_en("series"): return datos

    except Exception as e:
        log(f"⚠️ Error Metadata: {e}")
    
    return datos

# --- LÓGICA AUTO-START ---
def get_startup_path():
    return os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup', 'StremioRPC.lnk')

def check_autostart():
    return os.path.exists(get_startup_path())

def toggle_autostart(icon, item):
    link_path = get_startup_path()
    
    if getattr(sys, 'frozen', False):
        target = sys.executable
    else:
        target = os.path.abspath(sys.argv[0])
        
    work_dir = os.path.dirname(target)

    if os.path.exists(link_path):
        try:
            os.remove(link_path)
            log("🗑️ Auto-start desactivado.")
        except Exception as e:
            log(f"Error borrando link: {e}")
    else:
        try:
            ps_script = f"$s=(New-Object -COM WScript.Shell).CreateShortcut('{link_path}');$s.TargetPath='{target}';$s.WorkingDirectory='{work_dir}';$s.Save()"
            subprocess.run(["powershell", "-Command", ps_script], creationflags=0x08000000)
            log("✅ Auto-start activado.")
        except Exception as e:
            log(f"Error creando link: {e}")