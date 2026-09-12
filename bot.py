import os, requests
API_KEY = os.getenv("API_FOOTBALL_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@TouchlineT_scores_live")
headers = {"x-apisports-key": API_KEY}
telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def send_telegram(text):
    try:
        requests.post(telegram_url, json={"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"}, timeout=10)
    except:
        pass

def get_live():
    try:
        r = requests.get("https://v3.football.api-sports.io/fixtures?live=all", headers=headers, timeout=15)
        return r.json().get("response", [])
    except:
        return []

matches = get_live()
if not matches:
    send_telegram("⚽ TouchlineT : Aucun match en live actuellement.")
else:
    msg = "🔴 *LIVE - TouchlineT*\n\n"
    for m in matches[:10]:
        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]
        hg = m["goals"]["home"]
        ag = m["goals"]["away"]
        minute = m["fixture"]["status"]["elapsed"] or m["fixture"]["status"]["short"]
        msg += f"⏱ {minute}' - {home} {hg}-{ag} {away}\n"
    send_telegram(msg)
