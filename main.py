import os
import time
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

# --- Email Config ---
SMTP_PASS = os.environ.get("SMTP_PASS")
EMAIL_TO = os.environ.get("EMAIL_TO")
EMAIL_FROM = os.environ.get("EMAIL_FROM")
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))

if not SMTP_PASS:
    raise ValueError("Missing SMTP_PASS")

# FOTMob league IDs
LEAGUES = {
    "PL": 47,
    "PD": 87,
    "SA": 55,
    "BL1": 54,
    "FL1": 53,
    "MLS": 186,
    "CL": 42
}

# Today's date (UTC)
today = datetime.utcnow().date()
today_str = today.strftime("%Y-%m-%d")

matches_by_league = {}

for code, league_id in LEAGUES.items():

    url = f"https://www.fotmob.com/api/leagues?id={league_id}&ccode=WW"
    
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()

        fixtures = data["matches"]["allMatches"]
        upcoming = []

        now_utc = datetime.utcnow()

        for m in fixtures:
            if "time" not in m:
                continue
            if "utcTime" not in m["time"]:
                continue

            kickoff = datetime.fromisoformat(m["time"]["utcTime"].replace("Z", "+00:00"))

            # Only future matches today
            if kickoff.date() == today and kickoff >= now_utc:
                upcoming.append((m, kickoff))

        matches_by_league[code] = upcoming

    except Exception as e:
        print(f"[ERROR] Could not fetch league {code}: {e}")
        matches_by_league[code] = []

    time.sleep(1)
# HTML format to be set on email body
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
        match_time = match["utcDate"].split("T")[1][:5]
        highlight = "style='color:red;font-weight:bold;'" if "Barcelona" in (home, away) else ""
        html_body += f"<li {highlight}>{home} vs {away} — {match_time} UTC</li>"
    html_body += "</ul>"

# sending email with obtained match info
msg = MIMEText(html_body, "html")
msg["Subject"] = f"Upcoming Football Matches - {today_str}"
msg["From"] = EMAIL_FROM
msg["To"] = EMAIL_TO

with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls()
    server.login(EMAIL_FROM, SMTP_PASS)
    server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())

# print message on logs upon successful task execution
print("Daily Football email sent!")
