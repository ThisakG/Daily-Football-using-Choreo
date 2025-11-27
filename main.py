import os
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from time import sleep

# --- Config ---
API_KEY = os.environ.get("API_KEY")
LEAGUES = ["PL","PD","SA","BL1","FL1","MLS", "CL"]
EMAIL_TO = os.environ.get("EMAIL_TO")
EMAIL_FROM = os.environ.get("EMAIL_FROM")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_PASS = os.environ.get("SMTP_PASS")

# Validate required values
if not API_KEY or not SMTP_PASS:
    raise ValueError("Missing API_KEY or SMTP_PASS in environment variables")

# --- Date Range: Yesterday + Today (fixes timezone issues) ---
today = datetime.utcnow().date()
yesterday = today - timedelta(days=1)

date_from = yesterday.strftime("%Y-%m-%d")
date_to = today.strftime("%Y-%m-%d")

# --- Fetch matches ---
matches_by_league = {}

for league in LEAGUES:
    url = (
        f"https://api.football-data.org/v2/matches"
        f"?competitions={league}&dateFrom={date_from}&dateTo={date_to}"
    )

    headers = {"X-Auth-Token": API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            matches = response.json().get("matches", [])
            matches_by_league[league] = matches
        else:
            matches_by_league[league] = []
    except Exception:
        matches_by_league[league] = []

    sleep(0.5)  # rate limiting safety

# --- Format HTML email ---
html_body = f"<h2>⚽ Daily Football Update ({date_from} → {date_to})</h2>"

for league, matches in matches_by_league.items():
    html_body += f"<h3>{league}</h3>"
    
    if not matches:
        html_body += "<p>No matches in this period.</p>"
        continue
    
    html_body += "<ul>"
    for match in matches:
        home = match["homeTeam"]["name"]
        away = match["awayTeam"]["name"]
        utc_time = match["utcDate"]

        # Extract HH:MM for readability
        time_str = utc_time.split("T")[1][:5]

        highlight = (
            "style='color:red;font-weight:bold;'"
            if "Barcelona" in (home, away) else ""
        )

        html_body += f"<li {highlight}>{home} vs {away} — {time_str} UTC</li>"
    html_body += "</ul>"

# --- Send Email ---
msg = MIMEText(html_body, "html")
msg["Subject"] = f"Daily Football Update ({date_from} → {date_to})"
msg["From"] = EMAIL_FROM
msg["To"] = EMAIL_TO

server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
server.starttls()
server.login(EMAIL_FROM, SMTP_PASS)
server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())
server.quit()

print("Daily Football email sent!")
