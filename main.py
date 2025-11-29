import os
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta, timezone

# --- Email Config ---
SMTP_PASS = os.environ.get("SMTP_PASS")
EMAIL_TO = os.environ.get("EMAIL_TO")
EMAIL_FROM = os.environ.get("EMAIL_FROM")
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
API_KEY = os.environ.get("API_FOOTBALL_KEY")  # Get from RapidAPI

if not SMTP_PASS or not API_KEY:
    raise ValueError("Missing SMTP_PASS or API_FOOTBALL_KEY")

# League IDs (API-Football)
LEAGUES = {
    "PL": 39,    # Premier League
    "PD": 140,   # La Liga
    "SA": 135,   # Serie A
    "BL1": 78,   # Bundesliga
    "FL1": 61,   # Ligue 1
    "MLS": 253,  # Major League Soccer
    "CL": 2      # UEFA Champions League
}

# UTC now and today/tomorrow range
now_utc = datetime.now(timezone.utc)
today_start = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)
tomorrow_start = today_start + timedelta(days=1)

matches_by_league = {}

# API-Football headers
headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

for code, league_id in LEAGUES.items():
    url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?league={league_id}&season=2025&from={today_start.isoformat()}&to={tomorrow_start.isoformat()}"
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        matches = data.get("response", [])
        
        print(f"\n[DEBUG] {code}: API returned {len(matches)} total matches")
        print(f"[DEBUG] Search window: {today_start.isoformat()} to {tomorrow_start.isoformat()}")
        print(f"[DEBUG] Current UTC time: {now_utc.isoformat()}")
        
        upcoming = []
        for m in matches:
            kickoff_str = m["fixture"]["date"]
            kickoff = datetime.fromisoformat(kickoff_str.replace("Z","+00:00")).replace(tzinfo=timezone.utc)
            
            print(f"[DEBUG] Match: {m['teams']['home']['name']} vs {m['teams']['away']['name']} at {kickoff.isoformat()}")
            print(f"[DEBUG] Passes filter? now_utc <= kickoff < tomorrow_start: {now_utc} <= {kickoff} < {tomorrow_start} = {now_utc <= kickoff < tomorrow_start}")
            
            if now_utc <= kickoff < tomorrow_start:
                home = m["teams"]["home"]["name"]
                away = m["teams"]["away"]["name"]
                upcoming.append((home, away, kickoff))
        
        print(f"[DEBUG] {code}: {len(upcoming)} matches passed the filter")
        matches_by_league[code] = upcoming
    except Exception as e:
        print(f"[ERROR] Could not fetch {code}: {e}")
        matches_by_league[code] = []

# Build HTML email
today_str = now_utc.strftime("%Y-%m-%d")
html_body = f"<h2>⚽ Upcoming Football Matches for {today_str}</h2>"

for code, matches in matches_by_league.items():
    html_body += f"<h3>{code}</h3>"
    if not matches:
        html_body += "<p>No upcoming matches today.</p>"
        continue

    html_body += "<ul>"
    for home, away, kickoff in matches:
        match_time = kickoff.strftime("%H:%M")
        highlight = "style='color:red;font-weight:bold;'" if "Barcelona" in (home, away) else ""
        html_body += f"<li {highlight}>{home} vs {away} — {match_time} UTC</li>"
    html_body += "</ul>"

# Send email
msg = MIMEText(html_body, "html")
msg["Subject"] = f"Upcoming Football Matches - {today_str}"
msg["From"] = EMAIL_FROM
msg["To"] = EMAIL_TO

with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls()
    server.login(EMAIL_FROM, SMTP_PASS)
    server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())

print("Daily Football email sent!")
