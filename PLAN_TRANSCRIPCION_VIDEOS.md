# 🎙️ Plan Arquitectónico: Plataforma de Transcripción de Videos (Netec Transcriber)

**Objetivo:** Desarrollar un pipeline automatizado, seguro y escalable para extraer el audio de videos alojados en línea y convertirlos en transcripciones de texto exactas (diarizadas por orador y con marcas de tiempo), maximizando la reducción de costos operativos para Netec.

---

## 🛑 1. El Diagnóstico Técnico (El Problema)
Actualmente, los videos educativos o corporativos de Netec están alojados en la nube (ej. AWS S3, Vimeo, YouTube oculto, o OpenLMS).
Transcribir esto manualmente consume cientos de horas-hombre. Si usamos servicios SaaS de terceros (como Sonix o Rev), nos cobrarán una tarifa recurrente alta por minuto de audio procesado y pondremos en riesgo la privacidad de nuestro material B2B.

**La Solución:** Construir nuestro propio motor "Serverless" basado en modelos de IA Open Source de transcripción de última generación (Whisper).

---

## ⚙️ 2. Arquitectura de la Solución (3 Etapas)

### Etapa 1: Ingesta y Extracción (Download & Strip)
No podemos enviar un archivo de video MP4 de 2 GB a una API de Inteligencia Artificial; fallará por exceso de peso.
*   **Herramienta a usar:** `yt-dlp` (para descargar el video desde la URL segura) y `FFmpeg` (para separar el audio del video).
*   **El Proceso:** El sistema recibe el enlace del video, descarga solo la pista de audio y la comprime de `.mp4` a formato `.mp3` o `.ogg` (reduciendo un archivo de 2GB a un archivo ligero de 30MB).

### Etapa 2: El Motor de Transcripción (Whisper AI)
Una vez que tenemos el audio puro, necesitamos que la Inteligencia Artificial lo escuche y lo escriba.
*   **La Tecnología Core:** **OpenAI Whisper (Modelos Open Source locales o API).** Whisper es el motor de reconocimiento de voz (ASR) más avanzado y preciso del mundo para el español.
*   **Decisión Estratégica (Costo vs Velocidad):**
    *   *Opción A (Ultra Barata pero compleja):* Correr el modelo `Whisper-Large-v3` directamente en nuestros propios servidores Linux de Netec. Costo: $0, pero requiere instalar tarjetas gráficas (GPUs) costosas en nuestro servidor.
    *   *Opción B (Equilibrada y Rápida):* Usar la API oficial de OpenAI (`whisper-1`). Nos cobran $0.006 USD por minuto de audio. Procesar un curso de 10 horas costará apenas ~$3 dólares. **(Opción Recomendada para MVP)**.

### Etapa 3: Post-Procesamiento (Diarización y Limpieza)
Un bloque de texto crudo de 10 páginas no sirve de mucho.
*   **Marcas de Tiempo (Timestamps):** El motor generará subtítulos en formato `.srt` o `.vtt` (para inyectarlos directo en el LMS de Netec).
*   **Formato Inteligente:** Enviaremos el bloque de texto gigante a **Gemini Pro**, dándole la siguiente instrucción: *"Eres un corrector de estilo. Ponle comas, puntos, separa en párrafos y elimina las muletillas (ehh, mmm) del instructor, sin alterar los términos técnicos de la certificación"*.

---

## 📅 Roadmap de Implementación (MVP en 1 Semana)

*   **Día 1-2 (El Extractor):**
    Escribiré un script en Python (`transcriber.py`) que reciba la URL del video. El script instalará internamente el binario estático de FFmpeg en el servidor, descargará el video, lo desnudará dejándolo en `.mp3` y eliminará el video original para no saturar el disco duro.
*   **Día 3-4 (El Cerebro Whisper):**
    Conectaré el script de Python con la API de OpenAI Whisper, pasándole el MP3 particionado y obteniendo el texto transcrito con marcas de tiempo.
*   **Día 5 (Corrector Cognitivo):**
    Conectaré la salida de Whisper a nuestra API de Gemini para que limpie ortográficamente el archivo y te entregue un PDF / Markdown listo para usar en manuales o en el *Exam-Creator*.

---

## 🚦 Siguiente Paso Ejecutivo
Si apruebas este plan de arquitectura, te propongo escribir ahora mismo la **Prueba de Concepto (PoC)** en Python. 
Si tienes a la mano un enlace público o de YouTube de algún video corto de prueba, lo usamos como conejillo de indias.
