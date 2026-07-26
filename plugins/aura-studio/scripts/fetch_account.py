"""
Aura Studio — Info de la cuenta de Instagram Business/Creator
"""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(__file__))
from _common import api_get, log, fmt_num

IG_USER_ID = os.environ.get("IG_USER_ID") or \
    next((l.split("=",1)[1].strip() for l in open(".env").read().splitlines()
          if l.startswith("IG_USER_ID=")), None)

if not IG_USER_ID:
    # Auto-detectar desde token_info.json
    try:
        info = json.load(open("token_info.json"))
        accounts = info.get("ig_accounts", [])
        if accounts:
            IG_USER_ID = accounts[0]["ig_id"]
    except FileNotFoundError:
        print(json.dumps({"error": {"message": "IG_USER_ID no encontrado. Ejecuta verify_token.py primero.", "code": -1}}))
        sys.exit(1)

data = api_get(f"{IG_USER_ID}", {
    "fields": "id,name,username,biography,followers_count,follows_count,"
              "media_count,profile_picture_url,website"
})

if "error" in data:
    log("fetch_account.py", IG_USER_ID, "error", error=str(data["error"].get("code","?")))
    print(json.dumps(data, ensure_ascii=False))
    sys.exit(1)

out = {
    "id":              data.get("id"),
    "name":            data.get("name"),
    "username":        data.get("username"),
    "biography":       data.get("biography",""),
    "followers_count": data.get("followers_count", 0),
    "follows_count":   data.get("follows_count", 0),
    "media_count":     data.get("media_count", 0),
    "account_type":    "BUSINESS",
    "website":         data.get("website",""),
}

json.dump(out, open("account_info.json","w",encoding="utf-8"), indent=2)
print(json.dumps(out, indent=2, ensure_ascii=False))
log("fetch_account.py", IG_USER_ID,
    f"followers={fmt_num(out['followers_count'])} media={out['media_count']}")
