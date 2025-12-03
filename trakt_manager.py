import requests
import logging

TRAKT_API_URL = "https://api.trakt.tv"

def get_user_activity(username, client_id):
    """
    Obtiene la actividad actual del usuario desde Trakt.
    Retorna un diccionario con la info o None si no está viendo nada.
    """
    headers = {
        "Content-Type": "application/json",
        "trakt-api-version": "2",
        "trakt-api-key": client_id
    }
    
    try:
        url = f"{TRAKT_API_URL}/users/{username}/watching"
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 204:
            # 204 significa "No Content" -> No está viendo nada
            return None
            
        if response.status_code == 200:
            data = response.json()
            
            # Tipo: 'movie' o 'episode'
            media_type = data.get("type")
            if not media_type: return None
            
            info = {
                "source": "trakt",
                "type": media_type,
                "action": data.get("action", "watching"), # watching, scrobble, checkin
                "started_at": data.get("started_at"),
                "expires_at": data.get("expires_at")
            }
            
            if media_type == "movie":
                movie = data.get("movie", {})
                info["title"] = movie.get("title")
                info["year"] = movie.get("year")
                info["imdb_id"] = movie.get("ids", {}).get("imdb")
                info["tmdb_id"] = movie.get("ids", {}).get("tmdb")
                
            elif media_type == "episode":
                show = data.get("show", {})
                episode = data.get("episode", {})
                
                info["show_title"] = show.get("title")
                info["episode_title"] = episode.get("title")
                info["season"] = episode.get("season")
                info["episode"] = episode.get("number")
                info["imdb_id"] = show.get("ids", {}).get("imdb") # ID de la serie
                
                # Formato título: "Breaking Bad"
                # Formato estado: "S05E14 - Ozymandias"
                info["title"] = show.get("title")
                info["details"] = f"S{info['season']:02d}E{info['episode']:02d} - {info['episode_title']}"
                
            return info
            
        else:
            logging.warning(f"Trakt API Error: {response.status_code}")
            return None
            
    except Exception as e:
        logging.error(f"Error connecting to Trakt: {e}")
        return None
