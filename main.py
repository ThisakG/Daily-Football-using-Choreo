import os
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# --- Email config ---
SMTP_PASS = os.environ.get("SMTP_PASS")
EMAIL_TO = os.environ.get("EMAIL_TO")
EMAIL_FROM = os.environ.get("EMAIL_FROM")
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
API_KEY = os.environ.get("API_FOOTBALL_KEY")

if not SMTP_PASS or not API_KEY:
    raise ValueError("Missing SMTP_PASS or API_FOOTBALL_KEY")

# League IDs (API-Football)
LEAGUES = {
    "PL": 39,
    "PD": 140,
    "SA": 135,
    "BL1": 78,
    "FL1": 61,
    "MLS": 253,
    "CL": 2
}

today = datetime.utcnow().strftime("%Y-%m-%d")
matches_by_league = {}

headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}

for code, league_id in LEAGUES.items():
    url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?league={league_id}&season={datetime.utcnow().year}&date={today}"
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        matches = data.get("response", [])
        
        upcoming = []
        for m in matches:
            home = m["fixture"]["home"]["name"]
            away = m["fixture"]["away"]["name"]
            kickoff = m["fixture"]["date"]  # ISO format
            upcoming.append((home, away, kickoff))
        
        matches_by_league[code] = upcoming
    except Exception as e:
        print(f"[ERROR] Could not fetch {code}: {e}")
        matches_by_league[code] = []

# Build HTML email
html_body = f"<h2>⚽ Upcoming Football Matches for {today}</h2>"

for code, matches in matches_by_league.items():
    html_body += f"<h3>{code}</h3>"
    if not matches:
        html_body += "<p>No upcoming matches today.</p>"
        continue
    
    html_body += "<ul>"
    for home, away, kickoff in matches:
        match_time = kickoff.split("T")[1][:5]
        highlight = "style='color:red;font-weight:bold;'" if "Barcelona" in (home, away) else ""
        html_body += f"<li {highlight}>{home} vs {away} — {match_time} UTC</li>"
    html_body += "</ul>"

# Send email
msg = MIMEText(html_body, "html")
msg["Subject"] = f"Upcoming Football Matches - {today}"
msg["From"] = EMAIL_FROM
msg["To"] = EMAIL_TO

with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls()
    server.login(EMAIL_FROM, SMTP_PASS)
    server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())

print("Daily Football email sent!")
