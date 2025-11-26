import os
import time
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# --- Config from environment ---
API_KEY = os.environ.get("FOOTBALL_API_KEY")
LEAGUES = os.environ.get("LEAGUES", "PL,PD,SA,BL1,FL1,MLS,CL").split(",")
EMAIL_TO = os.environ.get("EMAIL_TO")
EMAIL_FROM = os.environ.get("EMAIL_FROM")
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_PASS = os.environ.get("SMTP_PASS")

# --- Input validation ---
today = datetime.today().strftime('%Y-%m-%d')

# Validate date format
try:
    datetime.strptime(today, "%Y-%m-%d")
except ValueError:
    raise ValueError(f"Invalid date format: {today}")

# Validate leagues
ALLOWED_LEAGUES = ["PL","PD","SA","BL1","FL1","MLS", "CL"]
for league in LEAGUES:
    if league not in ALLOWED_LEAGUES:
        raise ValueError(f"Invalid league code: {league}")

# --- Fetch matches with rate limiting ---
matches_by_league = {}
for league in LEAGUES:
    url = f"https://api.football-data.org/v2/matches?competitions={league}&dateFrom={today}&dateTo={today}"
    headers = {"X-Auth-Token": API_KEY}
    response = requests.get(url, headers=headers)
    matches_by_league[league] = response.json().get("matches", []) if response.status_code == 200 else []
    time.sleep(1)  # Rate limiting: wait 1 second between requests

# --- Format HTML email ---
html_body = "<h2>⚽ Today's Football Matches</h2>"
for league, matches in matches_by_league.items():
    html_body += f"<h3>{league}</h3>"
    if not matches:
        html_body += "<p>No matches today.</p>"
        continue
    html_body += "<table border='1' cellpadding='5' cellspacing='0'><tr><th>Time</th><th>Home</th><th>Away</th></tr>"
    for match in matches:
        home = match['homeTeam']['name']
        away = match['awayTeam']['name']
        time_str = match['utcDate'].split("T")[1][:5]
        style = " style='color:red;font-weight:bold;'" if "Barcelona" in (home, away) else ""
        html_body += f"<tr{style}><td>{time_str}</td><td>{home}</td><td>{away}</td></tr>"
    html_body += "</table>"

# --- Send Email ---
msg = MIMEText(html_body, "html")
msg['Subject'] = f"Daily Football Update - {today}"
msg['From'] = EMAIL_FROM
msg['To'] = EMAIL_TO

with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls()
    server.login(EMAIL_FROM, SMTP_PASS)
    server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())

print("Daily Football email sent!")
