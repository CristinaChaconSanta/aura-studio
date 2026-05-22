"""
Aura Studio — Métricas detalladas por publicación
Lee media_list.json y enriquece cada post con sus insights.
Uso: python fetch_insights.py
"""
import json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(__file__))
from _common import api_get, log, fmt_pct, semaforo

# ── Campos por tipo de contenido ──────────────────────────────────────────────
METRICS_IMAGE    = "reach,likes,comments,shares,saved,total_interactions"
METRICS_CAROUSEL = "reach,likes,comments,shares,saved,total_interactions"
METRICS_REEL     = "reach,likes,comments,shares,saved,total_interactions,views,ig_reels_avg_watch_time"

# ── Cargar lista de posts ─────────────────────────────────────────────────────
try:
    media_data = json.load(open("media_list.json", encoding="utf-8"))
except FileNotFoundError:
    print(json.dumps({"error": {"message": "media_list.json no encontrado. Ejecuta fetch_media.py primero.", "code": -1}}))
    sys.exit(1)

posts     = media_data.get("posts", [])
ig_user   = media_data.get("ig_user_id", "unknown")

# ── Cargar seguidores para calcular rates ─────────────────────────────────────
followers = 0
try:
    acc = json.load(open("account_info.json", encoding="utf-8"))
    followers = int(acc.get("followers_count", 0))
except FileNotFoundError:
    pass

enriched = []

for i, post in enumerate(posts):
    media_id = post["id"]
    tipo     = post.get("tipo", "IMAGEN")

    if tipo == "REEL":
        metric_str = METRICS_REEL
    elif tipo == "CARRUSEL":
        metric_str = METRICS_CAROUSEL
    else:
        metric_str = METRICS_IMAGE

    resp = api_get(f"{media_id}/insights", {"metric": metric_str, "period": "lifetime"})
    time.sleep(2)  # intervalo mínimo entre llamadas

    metrics = {}
    if "error" not in resp:
        for item in resp.get("data", []):
            metrics[item["name"]] = item.get("values", [{}])[-1].get("value", item.get("value", 0))

    # ── Calcular rates ────────────────────────────────────────────────────────
    reach    = int(metrics.get("reach", 0))
    saves    = int(metrics.get("saved", 0))
    shares   = int(metrics.get("shares", 0))
    likes    = int(metrics.get("likes", 0))
    comments = int(metrics.get("comments", 0))
    total_int= int(metrics.get("total_interactions", 0))
    views    = int(metrics.get("views", 0))
    avg_watch= float(metrics.get("ig_reels_avg_watch_time", 0))  # en milisegundos

    eng_rate   = round(total_int / reach * 100, 2) if reach else 0
    save_rate  = round(saves    / reach * 100, 2) if reach else 0
    share_rate = round(shares   / reach * 100, 2) if reach else 0
    reach_rate = round(reach / followers * 100, 2) if followers else 0
    avg_watch_s= round(avg_watch / 1000, 1)  # convertir ms → segundos

    # ── Semáforos ─────────────────────────────────────────────────────────────
    sem_eng   = semaforo(eng_rate,   5.0, 2.0)
    sem_save  = semaforo(save_rate,  3.0, 1.0)
    sem_share = semaforo(share_rate, 1.5, 0.5)
    sem_reach = semaforo(reach_rate, 15.0, 7.0)

    estado_general = "🟢" if sem_eng == "🟢" and sem_reach != "🔴" else \
                     "🔴" if sem_eng == "🔴" and sem_reach == "🔴" else "🟡"

    enriched_post = {
        **post,
        "metrics": {
            "reach":          reach,
            "likes":          likes,
            "comments":       comments,
            "shares":         shares,
            "saves":          saves,
            "total_interactions": total_int,
        },
        "rates": {
            "engagement_rate": eng_rate,
            "save_rate":       save_rate,
            "share_rate":      share_rate,
            "reach_rate":      reach_rate,
        },
        "semaforos": {
            "engagement": sem_eng,
            "saves":      sem_save,
            "shares":     sem_share,
            "reach":      sem_reach,
            "general":    estado_general,
        },
    }

    # Campos exclusivos de Reels
    if tipo == "REEL":
        enriched_post["metrics"]["views"]         = views
        enriched_post["metrics"]["avg_watch_sec"] = avg_watch_s
        views_rate = round(views / followers * 100, 2) if followers else 0
        enriched_post["rates"]["views_rate"]      = views_rate
        enriched_post["semaforos"]["views_rate"]  = semaforo(views_rate, 20.0, 8.0)

    enriched.append(enriched_post)
    print(f"  [{i+1}/{len(posts)}] {post.get('tipo','?')} {post.get('timestamp','')[:10]} — eng {eng_rate}% {sem_eng}", flush=True)

# ── Calcular promedios de cuenta ───────────────────────────────────────────────
def avg(lst): return round(sum(lst) / len(lst), 2) if lst else 0

promedios = {
    "engagement_rate": avg([p["rates"]["engagement_rate"] for p in enriched]),
    "save_rate":       avg([p["rates"]["save_rate"]       for p in enriched]),
    "share_rate":      avg([p["rates"]["share_rate"]      for p in enriched]),
    "reach_rate":      avg([p["rates"]["reach_rate"]      for p in enriched]),
    "reach":           avg([p["metrics"]["reach"]         for p in enriched]),
}

out = {
    "ig_user_id": ig_user,
    "followers":  followers,
    "total_posts_analizados": len(enriched),
    "promedios_cuenta": promedios,
    "posts": enriched,
}

json.dump(out, open("insights.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(json.dumps(out, indent=2, ensure_ascii=False))
log("fetch_insights.py", ig_user,
    f"posts={len(enriched)} avg_eng={promedios['engagement_rate']}% avg_reach_rate={promedios['reach_rate']}%")
