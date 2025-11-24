# 🎬 Stremio Discord RPC

**Muestra lo que estás viendo en Stremio directamente en tu perfil de Discord con carátulas reales, estado detallado y sin complicaciones.**

![Python](https://img.shields.io/badge/Made%20with-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Release](https://img.shields.io/github/v/release/anthonybuitrago/stremio-discord-rpc?style=for-the-badge&color=purple)

## ✨ Características

* **🖼️ Carátulas Reales:** Busca automáticamente el póster oficial de la película o anime en Cinemeta.
* **🚀 Auto-Detección:** Se sincroniza con Stremio al instante. Si cambias de video, Discord se actualiza.
* **📺 Modo TV:** Interfaz limpia con el estado "Watching Stremio".
* **🛡️ Anti-Buffer:** No borra tu estado si el video se pausa por carga o problemas de red.
* **🖱️ Bandeja del Sistema:** Se ejecuta en segundo plano con un icono en la barra de tareas para controlarlo fácilmente.
* **🧹 Limpieza Inteligente:** Elimina automáticamente etiquetas basura del nombre (`[1080p]`, `[HEVC]`, `DDP5.1`, etc.).
* **⚙️ Totalmente Configurable:** Archivo `config.json` para personalizar tu experiencia sin tocar código.

## 📥 Instalación (Modo Fácil)

No necesitas instalar Python. Solo descarga y ejecuta.

1.  Ve a la sección de [**Releases**](https://github.com/anthonybuitrago/stremio-discord-rpc/releases) a la derecha.
2.  Descarga el archivo `StremioRPC.exe`.
3.  Guárdalo en una carpeta (ej: Documentos).
4.  ¡Dale doble clic y listo!

*(Opcional: Crea un acceso directo en tu carpeta de Inicio `shell:startup` para que inicie con Windows).*

## ⚙️ Configuración Avanzada (`config.json`)

Al ejecutar el programa por primera vez, se creará un archivo `config.json`. Puedes editarlo para ajustar:

```json
{
    "client_id": "TU_ID_DE_DISCORD",
    "update_interval": 5,          // Segundos entre chequeos
    "tolerance_seconds": 60,       // Tolerancia anti-cierre
    "blacklisted_words": [         // Palabras a borrar del título
        "1080p", "4k", "HDR", "x265", "AMZN", "FLUX"
    ],
    "fixed_duration_minutes": 0    // 0 = Cronómetro real | 24 = Barra fija de anime
}

🛠️ Desarrollo (Para Programadores)
Si quieres modificar el código fuente:

Clona el repositorio.

Instala las dependencias:

Bash

pip install -r requirements.txt
Ejecuta el script:

Bash

python stremio.pyw
📝 Créditos
Desarrollado con ❤️ por Anthony Buitrago. Impulsado por pypresence, requests y la API de Cinemeta.