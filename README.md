2.  Ensure Python 3.10+ is installed.
3.  Install the required dependencies using the command:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the script:
    ```bash
    python main.py
```

# Internal Libraries Used
* **threading:** Used to run the Stremio monitoring loop and the GUI loop concurrently without blocking.

* **json**: For parsing API responses and managing the local configuration file.

* **re:** For regular expression pattern matching and string sanitization.

* **os & sys:** For file system operations and path management across different environments (Source vs. Frozen EXE).

* **time:** For managing update intervals and heartbeat logic.

* **urllib.parse:** For encoding URL queries safely.

# Usage
The system is designed with a "Set and Forget" philosophy.

Upon execution, the application runs silently in the background. A purple satellite/link icon will appear in the Windows System Tray (near the clock).

* **Automatic Detection:** Simply open Stremio and start watching a video. The status will update automatically on Discord.

* **System Tray Menu:** Right-clicking the tray icon reveals a menu with options to:

* **View Logs:** Opens the stremio_log.txt file for debugging.

* **Exit:** Safely terminates the background process and closes the connection to Discord.

* **Configuration:** You can modify the config.json file to change the Discord Client ID, update interval, or add words to the cleanup blacklist. Changes require an application restart.

# Contributions to Consider
* **GUI for Configuration:** Develop a graphical settings window using libraries like customtkinter to allow users to modify the JSON configuration without editing the text file directly.

* **Enhanced Metadata:** Implement additional API fallbacks (e.g., TMDB or IMDB) for cases where Cinemeta might not return a result.

# License
This project is distributed under the terms of the MIT License.

The MIT License is a permissive free software license originating at the Massachusetts Institute of Technology (MIT). It puts only very limited restriction on reuse and has, therefore, an excellent license compatibility. It permits reuse within proprietary software provided that all copies of the licensed software include a copy of the MIT License terms and the copyright notice.

# Additional Resources
* **Stremio API:** https://github.com/Stremio/stremio-addon-sdk/blob/master/docs/api/responses/meta.md

* **Discord RPC Documentation:** https://discord.com/developers/docs/rich-presence/how-to

* **PyInstaller Documentation:** https://pyinstaller.org/en/stable/