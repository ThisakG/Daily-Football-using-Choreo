import os
import time
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# --- Config ---
API_KEY = os.environ.get("FOOTBALL_API_KEY")  # Football-Data.org free API key
SMTP_PASS = os.environ.get("SMTP_PASS")
EMAIL_TO = os.environ.get("EMAIL_TO")
EMAIL_FROM = os.environ.get("EMAIL_FROM")
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))

# Leagues to fetch (you have access on free plan)
LEAGUES = {
    "PL": "PL",   # Premier League
    "PD": "PD",   # La Liga
    "CL": "CL"    # Champions League
}

# Validate environment variables
if not API_KEY or not SMTP_PASS or not EMAIL_TO or not EMAIL_FROM:
    raise ValueError("Missing required environment variables")

# Today's date in UTC
today_utc = datetime.utcnow().date()
today_str = today_utc.isoformat()

matches_by_league = {}

# --- Fetch matches ---
for code, league in LEAGUES.items():
    url = f"https://api.football-data.org/v4/competitions/{league}/matches?dateFrom={today_str}&dateTo={today_str}"
    headers = {"X-Auth-Token": API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        matches = []
        now_utc = datetime.utcnow()
        for match in data.get("matches", []):
            match_time = datetime.fromisoformat(match["utcDate"].replace("Z", "+00:00"))
            if match_time >= now_utc:
                matches.append(match)
        matches_by_league[code] = matches

    except Exception as e:
        print(f"[ERROR] Could not fetch {code}: {e}")
        matches_by_league[code] = []

    time.sleep(1)  # avoid hitting rate limits

# --- Prepare email ---
html_body = f"<h2>⚽ Upcoming Football Matches for {today_str}</h2>"

for league, matches in matches_by_league.items():
    html_body += f"<h3>{league}</h3>"
    if not matches:
        html_body += "<p>No upcoming matches today.</p>"
        continue
    html_body += "<ul>"
    for match in matches:
        home = match["homeTeam"]["name"]
        away = match["awayTeam"]["name"]
        match_time = datetime.fromisoformat(match["utcDate"].replace("Z", "+00:00")).strftime("%H:%M")
        highlight = "style='color:red;font-weight:bold;'" if "Barcelona" in (home, away) else ""
        html_body += f"<li {highlight}>{home} vs {away} — {match_time} UTC</li>"
    html_body += "</ul>"

# --- Send email ---
msg = MIMEText(html_body, "html")
msg["Subject"] = f"Upcoming Football Matches - {today_str}"
msg["From"] = EMAIL_FROM
msg["To"] = EMAIL_TO

try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_FROM, SMTP_PASS)
        server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())
    print("Daily Football email sent!")
except Exception as e:
    print(f"[ERROR] Could not send email: {e}")
