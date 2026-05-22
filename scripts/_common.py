"""
Aura Studio — Módulo compartido para Instagram Graph API
"""
import os, json, time, requests
from datetime import datetime

# ── Configuración ──────────────────────────────────────────────────────────────
API_VERSION = "v21.0"
BASE_URL    = f"https://graph.facebook.com/{API_VERSION}"
LOG_FILE    = "ig_api.log"

def get_token():
    token = os.environ.get("IG_ACCESS_TOKEN")
    if not token:
        try:
            for line in open(".env").read().splitlines():
                if line.startswith("IG_ACCESS_TOKEN="):
                    token = line.split("=", 1)[1].strip()
        except FileNotFoundError:
            pass
    if not token:
        print(json.dumps({"error": {"message": "IG_ACCESS_TOKEN no encontrado en env ni en .env", "code": -1}}))
        raise SystemExit(1)
    return token

# ── HTTP con reintentos ────────────────────────────────────────────────────────
def api_get(endpoint, params=None, retries=3):
    """GET con backoff exponencial ante rate limits."""
    token  = get_token()
    params = params or {}
    params["access_token"] = token
    url = f"{BASE_URL}/{endpoint.lstrip('/')}"

    delay = 2
    for attempt in range(retries):
        resp = requests.get(url, params=params)
        data = resp.json()

        # Errores que NO deben reintentarse
        if "error" in data:
            code = data["error"].get("code", 0)
            if code in (190, 10, 368) or (200 <= code <= 299):
                return data

        # Rate limit → esperar y reintentar
        if resp.status_code == 429 or (
            "error" in data and data["error"].get("code") in (4, 17, 32, 613)
        ):
            if attempt < retries - 1:
                time.sleep(delay + (attempt * 2))
                delay *= 2
                continue
        return data

    return data

# ── Paginación automática ──────────────────────────────────────────────────────
def paginate(endpoint, params=None, max_pages=5):
    """Recorre hasta max_pages páginas de resultados."""
    results = []
    data = api_get(endpoint, params)

    if "error" in data:
        return data

    results.extend(data.get("data", []))
    page = 1

    while page < max_pages:
        next_url = data.get("paging", {}).get("next")
        if not next_url:
            break
        resp = requests.get(next_url)
        data = resp.json()
        if "error" in data:
            break
        results.extend(data.get("data", []))
        page += 1
        time.sleep(2)  # intervalo entre páginas

    return results

# ── Logging ───────────────────────────────────────────────────────────────────
def log(script, user_id, summary, error="none"):
    ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"{ts} | {script} | user={user_id} | error={error} | {summary}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)

# ── Formateo ──────────────────────────────────────────────────────────────────
def fmt_num(n):
    try:
        return f"{int(n):,}"
    except (TypeError, ValueError):
        return str(n)

def fmt_pct(num, den):
    try:
        return f"{(int(num) / int(den) * 100):.1f}%"
    except (TypeError, ValueError, ZeroDivisionError):
        return "N/A"

def semaforo(value, green, yellow):
    """Devuelve emoji semáforo. green y yellow son umbrales mínimos."""
    try:
        v = float(str(value).replace("%",""))
        if v >= green:  return "🟢"
        if v >= yellow: return "🟡"
        return "🔴"
    except (TypeError, ValueError):
        return "⚪"
