import os, time, requests
API_KEY = os.getenv("API_FOOTBALL_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@TouchlineT_scores_live")
CHECK_INTERVAL = 900
headers = {"x-apisports-key": API_KEY}
telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
last_scores = {}
def send_telegram(m):
    try:
        requests.post(telegram_url, json={"chat_id": CHANNEL_ID, "text": m}, timeout=10)
    except: pass
def get_live():
    try:
        r = requests.get("https://v3.football.api-sports.io/fixtures?live=all", headers=headers, timeout=15)
        return r.json().get("response", [])
    except: return []
send_telegram("✅ TouchlineT Bot connecté!")
while True:
    for m in get_live():
        fid = m["fixture"]["id"]
        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]
        hg = m["goals"]["home"]
        ag = m["goals"]["away"]
        status = m["fixture"]["status"]["short"]
        minute = m["fixture"]["status"]["elapsed"]
        current = f"{hg}-{ag}"
        prev = last_scores.get(fid)
        if prev is None:
            last_scores[fid] = current
            continue
        if current!= prev:
            last_scores[fid] = current
            send_telegram(f"🚨 BUUUUT {minute}'\n{home} {hg}-{ag} {away}\n{prev} -> {current}")
    time.sleep(CHECK_INTERVAL)
