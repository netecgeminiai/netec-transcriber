import yt_dlp
import os
import json
import argparse

def json_to_netscape_cookies(json_file, txt_file):
    """
    Convierte un archivo de cookies JSON (exportado por J2TEAM o EditThisCookie) 
    al formato Netscape HTTP Cookie File (.txt) que requiere yt-dlp.
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            raw_data = f.read().strip()
            
        # Si el archivo ya es texto plano de Netscape pero le pusieron .json
        if raw_data.startswith("# Netscape HTTP"):
            with open(txt_file, 'w', encoding='utf-8') as out:
                out.write(raw_data)
            return True
            
        cookies = json.loads(raw_data)
        
        # Si es un diccionario, buscar la lista adentro
        if isinstance(cookies, dict):
            for key, val in cookies.items():
                if isinstance(val, list):
                    cookies = val
                    break
                    
        if not isinstance(cookies, list):
            print("[ERROR] El JSON no contiene una lista de cookies válida.")
            print(f"Tipo detectado: {type(cookies)}")
            return False
            
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write("# Netscape HTTP Cookie File\n")
            
            for cookie in cookies:
                if not isinstance(cookie, dict):
                    print(f"[WARNING] Saltando un elemento que no es diccionario: {cookie}")
                    continue
                
                domain = cookie.get('domain', '')
                include_subdomains = 'TRUE' if domain.startswith('.') else 'FALSE'
                path = cookie.get('path', '/')
                secure = 'TRUE' if cookie.get('secure', False) else 'FALSE'
                expiration = str(int(cookie.get('expirationDate', 0))) if cookie.get('expirationDate') else '0'
                name = cookie.get('name', '')
                value = cookie.get('value', '')
                
                line = f"{domain}\t{include_subdomains}\t{path}\t{secure}\t{expiration}\t{name}\t{value}\n"
                f.write(line)
        return True
    except Exception as e:
    except Exception as e:
        print(f"[ERROR] Fallo al convertir cookies JSON a TXT: {e}")
        return False

def descargar_audio_autenticado(url, json_cookies_file="cookies.json"):
    print(f"[*] Iniciando extracción de: {url}")
    
    if not os.path.exists(json_cookies_file):
        print(f"[ERROR] No se encontró el archivo '{json_cookies_file}'.")
        return None

    txt_cookies_file = "cookies_convertidas.txt"
    print("[*] Convirtiendo cookies JSON al formato soportado (Netscape TXT)...")
    if not json_to_netscape_cookies(json_cookies_file, txt_cookies_file):
        return None

    # Configuración de yt-dlp para extraer SOLO audio y usar cookies
    ydl_opts = {
        'format': 'bestaudio/best',
        'cookiefile': txt_cookies_file, 
        'outtmpl': 'audio_extraido.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }],
        'quiet': False,
        'no_warnings': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print("\n[+] ¡Éxito! Audio extraído y guardado como 'audio_extraido.mp3'")
            return "audio_extraido.mp3"
    except Exception as e:
        print(f"\n[ERROR] Falló la extracción: {e}")
        return None
    finally:
        # Limpieza por seguridad
        if os.path.exists(txt_cookies_file):
            os.remove(txt_cookies_file)

if __name__ == "__main__":
    print("===========================================")
    print(" 🎙️  NETEC TRANSCRIBER (MODO JSON COOKIES) ")
    print("===========================================\n")
    
    url_test = input("Ingresa la URL del video privado: ")
    
    if url_test.strip():
        descargar_audio_autenticado(url_test.strip(), "cookies.json")
    else:
        print("URL no válida.")
