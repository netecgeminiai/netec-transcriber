import yt_dlp
import os
import argparse

def descargar_audio_autenticado(url, cookies_file="cookies.txt"):
    """
    Descarga el audio de un video detrás de un paywall usando cookies del navegador.
    """
    print(f"[*] Iniciando extracción de: {url}")
    print(f"[*] Usando archivo de cookies: {cookies_file}")
    
    if not os.path.exists(cookies_file):
        print(f"[ERROR] No se encontró el archivo '{cookies_file}'.")
        print("    Por favor, exporta las cookies de tu navegador con la extensión 'Get cookies.txt LOCALLY'.")
        return None

    # Configuración de yt-dlp para extraer SOLO audio y usar cookies
    ydl_opts = {
        'format': 'bestaudio/best',
        'cookiefile': cookies_file, # LA MAGIA OCURRE AQUÍ
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
            print("\n[+] ¡Éxito! Audio extraído y convertido a 'audio_extraido.mp3'")
            return "audio_extraido.mp3"
    except Exception as e:
        print(f"\n[ERROR] Falló la extracción: {e}")
        return None

if __name__ == "__main__":
    # URL de prueba (Dion Training - ITIL 5)
    # Ejemplo de uso: python transcriber_auth.py https://members.diontraining.com/...
    
    print("===========================================")
    print(" 🎙️  NETEC TRANSCRIBER (MODO AUTENTICADO) ")
    print("===========================================\n")
    
    url_test = input("Ingresa la URL del video privado: ")
    
    if url_test.strip():
        descargar_audio_autenticado(url_test.strip(), "cookies.txt")
        print("\nSiguiente fase (Mock): Enviar 'audio_extraido.mp3' a OpenAI Whisper...")
    else:
        print("URL no válida.")
