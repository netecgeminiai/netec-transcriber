# Memoria Codex - netec-transcriber

Ultima actualizacion: 2026-06-01

## Proposito del repo

Pipeline para extraer audio de videos alojados en linea y convertirlos en transcripciones limpias con posibilidad de timestamps, diarizacion y salida util para cursos, subtitulos o insumos de Exam-Creator.

## Estado observado

- Remoto: `https://github.com/netecgeminiai/netec-transcriber.git`
- Rama local: `main`
- Estado local al 2026-06-01: limpio, pero 1 commit detras de `origin/main`.
- Commit remoto pendiente observado: `b83c027`, que agrega bypass Cloudflare con impersonation/User-Agent en `transcriber_json.py`.

## Estructura relevante

- `PLAN_TRANSCRIPCION_VIDEOS.md`: plan arquitectonico y roadmap del MVP.
- `transcriber_auth.py`: flujo autenticado.
- `transcriber_json.py`: flujo de transcripcion/salida JSON.
- `requirements.txt`: dependencias Python.
- `start_env.bat`: activacion local del entorno.
- `cookies.json`: archivo sensible potencial; revisar si debe seguir versionado.

## Historial reciente relevante

- Reparacion de bloque main eliminado durante limpieza.
- Reparaciones de indentacion y sintaxis.
- Correcciones alrededor de strings problematicos, f-strings y `.format()`.
- En remoto existe una mejora para evadir bloqueos Cloudflare en sitios protegidos.

## Proximos pasos sugeridos

- Hacer `git pull` para incorporar el bypass Cloudflare si se necesita procesar sitios protegidos.
- Revisar `cookies.json` y confirmar si contiene datos sensibles; si aplica, mover a `.gitignore` y regenerarlo localmente.
- Definir salida objetivo: texto limpio, JSON, SRT/VTT, Markdown o insumo directo para cursos/examenes.
- Agregar una prueba con video corto y publico para validar el flujo completo sin exponer material privado.

## Como retomar

Leer este archivo y `PLAN_TRANSCRIPCION_VIDEOS.md`. Antes de tocar scripts, revisar `git status --short --branch` y decidir si conviene bajar el commit remoto pendiente.
