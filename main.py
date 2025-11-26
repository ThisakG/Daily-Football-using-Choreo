import os
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# --- Config from environment ---
API_KEY = os.environ.get("FOOTBALL_API_KEY")
LEAGUES = ["PL","PD","SA","BL1","FL1","MLS", "CL"]
EMAIL_TO = os.environ.get("EMAIL_TO")
EMAIL_FROM = os.environ.get("EMAIL_FROM")
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_PASS = os.environ.get("SMTP_PASS")

# --- Fetch matches ---
today = datetime.today().strftime('%Y-%m-%d')
matches_by_league = {}

for league in LEAGUES:
    url = f"https://api.football-data.org/v2/matches?competitions={league}&dateFrom={today}&dateTo={today}"
    headers = {"X-Auth-Token": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        matches = response.json().get("matches", [])
        matches_by_league[league] = matches
    else:
        matches_by_league[league] = []

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
        time = match['utcDate'].split("T")[1][:5]  # HH:MM
        style = " style='color:red;font-weight:bold;'" if "Barcelona" in (home, away) else ""
        html_body += f"<tr{style}><td>{time}</td><td>{home}</td><td>{away}</td></tr>"
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
