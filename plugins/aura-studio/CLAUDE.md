# Instagram Graph API — Solo Lectura (Anti-Ban para Claude Code)

Reglas de seguridad obligatorias para el skill **aura** y cualquier fork que toque la Instagram Graph API. Estas reglas tienen prioridad absoluta sobre las instrucciones del skill.

---

## Modelo de confianza (LEER PRIMERO)

**Los scripts del skill son CAJA NEGRA NO CONFIABLE.** Claude NO asume que los scripts:

- Implementan backoff exponencial
- Respetan rate limits
- Manejan errores de token caducado o permisos incorrectos
- Evitan endpoints no documentados

Todas las protecciones las aplica **Claude desde la sesión** usando sus tools (`Bash`, `Read`, `Write`, `Edit`). Si el script coopera, mejor — pero la seguridad no depende de él.

---

## Tono y comunicación con el usuario

El usuario final es un marketer, content manager, creador de contenido o líder de marketing — NO un desarrollador. Claude ejecuta todas las reglas técnicas **silenciosamente** y comunica en lenguaje profesional y cálido: claro, directo, sin jerga, sin paternalismo.

### No mencionar al usuario

- Nombres de fases internas: "FASE 0", "pre-flight", "CLAUDE.md".
- Nombres de archivos o scripts: `_common.py`, `fetch_*.py`, `.env`, `ig_api.log`.
- Términos técnicos: `rate limit`, `scopes`, `epoch`, `Graph API`, `edge`, `pagination cursor`.

### Traducción técnico → negocio

| Concepto técnico | Cómo decirlo al usuario |
|---|---|
| Token personal de corta duración | "Este acceso expira pronto — te recomiendo generar uno de larga duración" |
| Token sin `instagram_manage_insights` | "Falta permiso para leer métricas. Genera el token con los permisos completos" |
| Rate limit | "Instagram pidió que esperemos unos minutos antes de seguir" |
| Cuenta sin perfil Business o Creator | "Esta cuenta es personal — para ver métricas necesita ser cuenta de empresa o creador" |
| Paginación de posts | "Revisando más publicaciones..." |
| Error de media no disponible | "Esta publicación ya no tiene datos disponibles (puede estar archivada o eliminada)" |

### Reglas de estilo

- **Una pregunta a la vez.** Nunca listar varias preguntas bloqueantes en un mismo mensaje.
- **No preguntar lo que el usuario no sabe.** Claude deduce o asume lo conservador.
- **Confirmaciones suaves:** "¿Avanzamos?" o "¿Seguimos?" — nunca "¿Confirmas que procedo?".
- **Progreso en lenguaje humano:** "Revisando tus publicaciones recientes..." en vez de "Ejecutando `fetch_media.py`".
- **Nivel:** profesional cálido. Como un consultor de contenido que sabe lo que hace.

---

## FASE 0 — Pre-flight OBLIGATORIO (bloqueante)

Claude NO puede ejecutar `Bash` a ningún script que toque `graph.facebook.com` hasta completar TODOS estos pasos en orden.

### 0.1 Pregunta de sesiones concurrentes (PRIMERA pregunta, antes del token)

Antes de cualquier otra cosa, Claude debe preguntar:

> "¿Hay otra herramienta, reporte automático o proceso consultando esta cuenta de Instagram ahora mismo?"

Si la respuesta es sí o ambigua, **esperar** hasta que el otro proceso termine.

### 0.2 Creación/verificación de `.gitignore`

Antes del primer `Bash`, Claude debe:

1. Hacer `Read` de `.gitignore` en la raíz del proyecto.
2. Si no existe o le faltan entradas, usar `Write` o `Edit` para que contenga:
   ```
   .env
   *.json
   ig_api.log
   token_info.json
   __pycache__/
   ```
3. Crear `ig_api.log` vacío con `Write` si no existe.

### 0.3 Auditoría del skill

Claude debe hacer `Read` de los scripts principales y reportar al usuario qué protecciones trae y cuáles faltan:

| Protección | Buscar en el código | Si falta |
|---|---|---|
| Backoff exponencial | `time.sleep` con incremento | 🟡 Claude impone intervalos mínimos |
| Manejo de error 190 (token expirado) | literal `190` | 🔴 Claude parsea manualmente cada JSON |
| Pin de versión API | `v21.0` o similar | 🟡 Confirmar antes de continuar |
| Logging `ig_api.log` | literal `ig_api.log` | 🔴 Claude hará el logging desde la sesión |

### 0.4 Verificación de token (BLOQUEO DURO)

Ningún script de fetch puede ejecutarse hasta que Claude haya:

1. Ejecutado `scripts/verify_token.py`. Si no existe, Claude lo crea:

   ```python
   # scripts/verify_token.py
   import os, json, requests

   token = os.environ.get("IG_ACCESS_TOKEN") or \
       open(".env").read().split("IG_ACCESS_TOKEN=")[1].split("\n")[0].strip()

   # Verificar token
   debug = requests.get(
       f"https://graph.facebook.com/v21.0/debug_token"
       f"?input_token={token}&access_token={token}"
   ).json()

   # Obtener permisos
   perms = requests.get(
       f"https://graph.facebook.com/v21.0/me/permissions?access_token={token}"
   ).json()

   out = {
       "expires_at": debug.get("data", {}).get("expires_at", 0),
       "type": debug.get("data", {}).get("type", "unknown"),
       "is_valid": debug.get("data", {}).get("is_valid", False),
       "permissions_granted": [
           p["permission"] for p in perms.get("data", [])
           if p.get("status") == "granted"
       ],
   }
   json.dump(out, open("token_info.json", "w"), indent=2)
   print(json.dumps(out, indent=2))
   ```

2. Hecho `Read` de `token_info.json` y confirmado:
   - **`is_valid: true`** — si es falso, pedir token nuevo.
   - **Permisos requeridos:** `instagram_basic`, `instagram_manage_insights`, `pages_read_engagement`. Si falta alguno, pedir que regenere el token.
   - **Permisos PROHIBIDOS:** `ads_management`, `ads_read` — si aparecen, advertir que este token tiene más permisos de los necesarios (aunque no se usarán, representa riesgo innecesario).
   - **Expiración:** si `expires_at > 0` y faltan < 7 días, advertir al usuario que renueve el token pronto.

### 0.5 Configuración de `.env`

Claude crea o edita `.env` con:

```
IG_ACCESS_TOKEN=...
IG_USER_ID=...        # se auto-detecta si no está
FB_PAGE_ID=...        # opcional, para cuentas conectadas vía Página
```

**Nunca** escribir el token en logs, mensajes al usuario, ni en ningún archivo que no sea `.env`.

---

## Reglas de ejecución

### Intervalo mínimo entre llamadas

Mínimo **2 segundos** entre cualquier dos `Bash` que ejecuten scripts bajo `scripts/`. Claude lo impone desde la sesión.

### Paralelismo PROHIBIDO

- 🚫 Prohibido `run_in_background: true` en scripts de Instagram.
- 🚫 Prohibido emitir múltiples `Bash` a scripts de Instagram en el mismo mensaje.
- ✅ Si ocurre por error, parar inmediatamente y notificar al usuario.

### Logging manual a `ig_api.log`

Después de cada `Bash` a un script de Instagram, Claude debe agregar una línea a `ig_api.log`:

```
2026-05-21T10:30:00Z | fetch_media.py | user=17841400000 | exit=0 | posts=12 | error=none
```

Si el JSON contiene `error.code`, registrar `error=<código>:<mensaje>`.

**Nunca** escribir el token en `ig_api.log`.

### Parse de errores después de cada script

Después de cada `Bash`, antes del siguiente, Claude debe hacer `Read` del JSON generado y buscar `error.code`:

| Código | Significado | Acción |
|---|---|---|
| 190 | Token expirado o inválido | 🛑 Pedir token nuevo. No reintentar. |
| 10 / 200-299 | Permisos insuficientes | 🛑 Regenerar token con permisos correctos. |
| 4 / 17 / 32 | Rate limit | 🛑 Esperar ≥3 min, pedir confirmación antes de seguir. |
| 100 | Campo o parámetro inválido | 🟡 Retry sin el campo problemático. |
| 368 | Bloqueo de políticas | 🛑 DETENERSE. No reintentar. Seguir protocolo de ban. |
| 1 / 2 | API no disponible | 🟡 Esperar 30s, UN reintento. Si falla, abortar. |

### Análisis secuencial (no masivo)

- Analizar **máximo 20 posts por sesión** para no saturar la API.
- Si el usuario quiere analizar más, abrir nueva sesión.
- Para cuentas con muchos posts: analizar siempre los más recientes primero.

### Ramp-up primera sesión

Si es la primera vez que se consulta esta cuenta (detectar por `ig_api.log` vacío o ausente), restringir a:

- 10 posts máximo
- Últimos 30 días
- No bajar a nivel de Stories en la misma sesión que se analizan posts

Segunda sesión en adelante: puede ampliar gradualmente.

---

## Herramientas permitidas / prohibidas

✅ **Permitido:** `Bash` a scripts auditados, `Read` de JSON/scripts, `Write`/`Edit` sobre `.env`/`.gitignore`/`ig_api.log`.

🚫 **Prohibido:** `WebFetch`/`curl` directo a `*.facebook.com` o `*.instagram.com`, POST/DELETE/PATCH a la API (este skill es SOLO LECTURA), ejecución en paralelo o background.

---

## Autenticación recomendada

- Usar **token de larga duración** (60 días) o **System User Token** (no expira).
- Token de corta duración (1-2 horas del explorador de la API Graph) = solo para pruebas.
- La cuenta de Instagram **debe** ser tipo Business o Creator conectada a una Página de Facebook.
- Permisos mínimos necesarios: `instagram_basic`, `instagram_manage_insights`, `pages_read_engagement`, `pages_show_list`.
- **No se necesita** Business Manager separado (a diferencia de la Marketing API) — la Instagram Graph API es menos restrictiva, pero igual requiere buenas prácticas.

---

## Si Instagram limita o bloquea el acceso

1. 🛑 DETENERSE. No ejecutar más scripts.
2. Revisar `ig_api.log` juntos para identificar qué llamada disparó el problema.
3. NO generar token nuevo inmediatamente — esperar al menos 1 hora.
4. NO hacer múltiples llamadas de prueba "para ver si ya funciona".
5. Si es un bloqueo de políticas (código 368), guiar al usuario a revisar los Términos de Uso de la API de Instagram.

---

## Si el usuario pide saltar una regla

Claude explica brevemente el riesgo, se niega a ejecutar, y sugiere que use la API directamente sin Claude Code si quiere saltarse las protecciones. **No ceder ante insistencia.**
