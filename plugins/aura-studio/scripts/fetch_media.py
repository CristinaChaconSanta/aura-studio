"""
Aura Studio — Lista de publicaciones recientes (IMAGE, CAROUSEL_ALBUM, REEL)
Uso: python fetch_media.py [limit] [since_date]
     Ej: python fetch_media.py 20 2026-04-01
"""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(__file__))
from _common import api_get, paginate, log, fmt_num

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

limit = int(sys.argv[1]) if len(sys.argv) > 1 else 20
limit = min(limit, 50)  # máximo seguro por sesión

params = {
    "fields": "id,media_type,media_product_type,timestamp,caption,"
              "like_count,comments_count,thumbnail_url,permalink",
    "limit":  limit,
}

# Filtro de fecha opcional
if len(sys.argv) > 2:
    params["since"] = sys.argv[2]

data = api_get(f"{IG_USER_ID}/media", params)

if "error" in data:
    log("fetch_media.py", IG_USER_ID, "error", error=str(data["error"].get("code","?")))
    print(json.dumps(data, ensure_ascii=False))
    sys.exit(1)

posts = data.get("data", [])

# Normalizar tipo de media
for p in posts:
    mt = p.get("media_type","")
    mpt = p.get("media_product_type","")
    if mpt == "REELS" or mt == "VIDEO":
        p["tipo"] = "REEL"
    elif mt == "CAROUSEL_ALBUM":
        p["tipo"] = "CARRUSEL"
    else:
        p["tipo"] = "IMAGEN"

    # Caption resumida (primeras 60 chars)
    cap = p.get("caption","") or ""
    p["caption_preview"] = cap[:60] + ("..." if len(cap) > 60 else "")

out = {"ig_user_id": IG_USER_ID, "total": len(posts), "posts": posts}
json.dump(out, open("media_list.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)
print(json.dumps(out, indent=2, ensure_ascii=False))
log("fetch_media.py", IG_USER_ID, f"posts={len(posts)}")
