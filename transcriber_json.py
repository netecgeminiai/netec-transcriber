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
                
                line = str(domain) + '\t' + str(include_subdomains) + '\t' + str(path) + '\t' + str(secure) + '\t' + str(expiration) + '\t' + str(name) + '\t' + str(value) + '\n'
                f.write(line)
        return True
    except Exception as e:
        print(f'[ERROR] Fallo al parsear JSON: {e}')
        return False
