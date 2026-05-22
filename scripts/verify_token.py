"""
Aura Studio — Verificación de token de Instagram
"""
import json, sys
sys.stdout.reconfigure(encoding="utf-8")

from _common import get_token, BASE_URL
import requests

token = get_token()

# 1. Debug token
debug = requests.get(
    f"{BASE_URL}/debug_token",
    params={"input_token": token, "access_token": token}
).json()

# 2. Permisos concedidos
perms = requests.get(
    f"{BASE_URL}/me/permissions",
    params={"access_token": token}
).json()

# 3. Cuentas de Instagram vinculadas
pages = requests.get(
    f"{BASE_URL}/me/accounts",
    params={"access_token": token, "fields": "id,name,instagram_business_account"}
).json()

ig_accounts = []
for page in pages.get("data", []):
    ig = page.get("instagram_business_account")
    if ig:
        ig_accounts.append({"page_id": page["id"], "page_name": page["name"], "ig_id": ig["id"]})

out = {
    "is_valid":    debug.get("data", {}).get("is_valid", False),
    "expires_at":  debug.get("data", {}).get("expires_at", 0),
    "token_type":  debug.get("data", {}).get("type", "unknown"),
    "permissions": [p["permission"] for p in perms.get("data", []) if p.get("status") == "granted"],
    "ig_accounts": ig_accounts,
}

json.dump(out, open("token_info.json", "w", encoding="utf-8"), indent=2)
print(json.dumps(out, indent=2, ensure_ascii=False))
