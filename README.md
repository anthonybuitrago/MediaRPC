  - Fetches album art from **iTunes (US/JP)** and **Deezer** (for music).
- **⚡ Performance**: Optimized to run silently in the background with minimal resource usage.
- **🔄 Robustness**: Auto-reconnects if Discord or Stremio is restarted.
- **📝 Logging**: Detailed logs to help troubleshoot connection issues.

---

## 📥 Installation

### Option 1: The Easy Way (Recommended)
1. Go to the [Releases Page](../../releases).
2. Download the latest `MediaRPC.exe`.
3. Run it! A satellite icon 🛰️ will appear in your system tray.

### Option 2: For Developers (Python)
If you want to run from source or modify the code:

1. Install [Python 3.10+](https://www.python.org/).
2. Clone this repository:
   ```bash
   git clone https://github.com/anthonybuitrago/stremio-discord-rpc.git
   cd stremio-discord-rpc
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the script:
   ```bash
   python main.py
   ```

---

## 🎮 Usage

### For Stremio
1. Open **MediaRPC**.
2. Open **Stremio** and start watching something.
3. Check your Discord profile! It should show "Watching **[Movie/Series Name]**".

### For Music
1. Open **MediaRPC**.
2. Play music on **YouTube Music** (Desktop/Web), **Spotify**, or any player that supports Windows Media Controls.
3. Discord will show "Listening to **[Song Name]**".

> **Note:** Music takes priority over Stremio. If you pause music, Stremio status will return.

---

## ⚙️ Configuration

A `config.json` file is created automatically in the same folder. You can edit it to customize behavior:

```json
{
    "client_id": "1310468962450866226",  // Discord App ID for Stremio
    "music_client_id": "1310468962450866226", // Discord App ID for Music (Optional)
    "update_interval": 15,               // How often to update Discord (seconds)
    "show_search_button": true,          // Show "Search Anime" button
    "enable_music_rpc": true             // Enable/Disable music detection
}
```

---

## 🛠️ Troubleshooting

- **"It's not showing up on Discord!"**
  - Make sure "Activity Privacy" -> "Display current activity as a status message" is **ON** in Discord settings.
  - Check the system tray icon 🛰️. Right-click -> **View Logs** to see if there are errors.

- **"Cover art is missing!"**
  - MediaRPC searches multiple databases (Cinemeta, iTunes, Deezer). If a song/movie is very obscure, it might not find a match.

- **"Stremio status is stuck?"**
  - Right-click the tray icon -> **Restart RPC**.

---

## 📜 License

This project is licensed under the **MIT License**. Feel free to modify and distribute it.