"""
Aura Studio — Métricas de Stories activas (últimas 24h)
Las Stories solo tienen datos mientras están publicadas.
Uso: python fetch_stories.py
"""
import json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(__file__))
from _common import api_get, log, semaforo

IG_USER_ID = os.environ.get("IG_USER_ID") or \
    next((l.split("=",1)[1].strip() for l in open(".env").read().splitlines()
          if l.startswith("IG_USER_ID=")), None)

if not IG_USER_ID:
    try:
        info = json.load(open("token_info.json"))
        IG_USER_ID = info["ig_accounts"][0]["ig_id"]
    except Exception:
        print(json.dumps({"error": {"message": "IG_USER_ID no encontrado.", "code": -1}}))
        sys.exit(1)

followers = 0
try:
    acc = json.load(open("account_info.json", encoding="utf-8"))
    followers = int(acc.get("followers_count", 0))
except FileNotFoundError:
    pass

# ── Obtener Stories activas ───────────────────────────────────────────────────
resp = api_get(f"{IG_USER_ID}/stories", {
    "fields": "id,media_type,timestamp,caption"
})

if "error" in resp:
    print(json.dumps(resp, ensure_ascii=False))
    sys.exit(1)

stories = resp.get("data", [])

if not stories:
    out = {"message": "No hay Stories activas en este momento.", "stories": []}
    json.dump(out, open("stories.json","w",encoding="utf-8"), indent=2)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.exit(0)

enriched = []

for story in stories:
    sid = story["id"]
    metrics_resp = api_get(f"{sid}/insights", {
        "metric": "reach,exits,replies,taps_forward,taps_back"
    })
    time.sleep(2)

    metrics = {}
    if "error" not in metrics_resp:
        for item in metrics_resp.get("data", []):
            metrics[item["name"]] = item.get("values", [{}])[-1].get("value", item.get("value", 0))

    reach        = int(metrics.get("reach", 0))
    exits        = int(metrics.get("exits", 0))
    replies      = int(metrics.get("replies", 0))
    taps_forward = int(metrics.get("taps_forward", 0))
    taps_back    = int(metrics.get("taps_back", 0))

    exit_rate    = round(exits        / reach * 100, 2) if reach else 0
    forward_rate = round(taps_forward / reach * 100, 2) if reach else 0
    back_rate    = round(taps_back    / reach * 100, 2) if reach else 0
    reach_rate   = round(reach / followers * 100, 2)    if followers else 0

    # Semáforos — exit rate: menor es mejor (invertido)
    sem_exit    = "🟢" if exit_rate < 15 else ("🟡" if exit_rate < 35 else "🔴")
    sem_forward = "🟢" if forward_rate < 20 else ("🟡" if forward_rate < 40 else "🔴")
    sem_reach   = semaforo(reach_rate, 15.0, 7.0)

    enriched.append({
        **story,
        "metrics": {
            "reach":        reach,
            "exits":        exits,
            "replies":      replies,
            "taps_forward": taps_forward,
            "taps_back":    taps_back,
        },
        "rates": {
            "exit_rate":    exit_rate,
            "forward_rate": forward_rate,
            "back_rate":    back_rate,
            "reach_rate":   reach_rate,
        },
        "semaforos": {
            "exit":    sem_exit,
            "forward": sem_forward,
            "reach":   sem_reach,
        },
    })

out = {
    "ig_user_id":    IG_USER_ID,
    "total_stories": len(enriched),
    "nota":          "Las Stories solo tienen métricas mientras están activas (24h).",
    "stories":       enriched,
}

json.dump(out, open("stories.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)
print(json.dumps(out, indent=2, ensure_ascii=False))
log("fetch_stories.py", IG_USER_ID, f"stories={len(enriched)}")
