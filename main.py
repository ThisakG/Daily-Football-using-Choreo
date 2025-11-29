import os # provide access to environment variables and OS
import time # providing time related functions
import requests # providing HTTP requests
import smtplib # library that provides SMTP service
from email.mime.text import MIMEText # providing email handling functions
from datetime import datetime, timedelta # providing date and time (UTC) 

# --- Config from Choreo environment variables ---
API_KEY = os.environ.get("FOOTBALL_API_KEY") # football news API via https://www.football-data.org/
SMTP_PASS = os.environ.get("SMTP_PASS") # service password obtained through google account app passwords
EMAIL_TO = os.environ.get("EMAIL_TO")  # to whom the mail is sent
EMAIL_FROM = os.environ.get("EMAIL_FROM") # sender of the mail
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com") # email service
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587)) # service port
LEAGUES = ["PL","PD","SA","BL1","FL1","MLS", "CL"] # the required leauges

# Date range – FIXED
today = datetime.utcnow().date()
today_str = today.strftime("%Y-%m-%d")
tomorrow_str = (today + timedelta(days=1)).strftime("%Y-%m-%d")

if not API_KEY or not SMTP_PASS:
    raise ValueError("Missing FOOTBALL_API_KEY or SMTP_PASS in environment variables")

ALLOWED_LEAGUES = ["PL", "PD", "SA", "BL1", "FL1", "MLS", "CL"]
for league in LEAGUES:
    if league not in ALLOWED_LEAGUES:
        raise ValueError(f"Invalid league code: {league}")

matches_by_league = {}
now_utc = datetime.utcnow()

for league in LEAGUES:
    url = (
        f"https://api.football-data.org/v4/matches?"
        f"competitions={league}&dateFrom={today_str}&dateTo={tomorrow_str}"
    )
    headers = {"X-Auth-Token": API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=12)

        if response.status_code == 429:
            print(f"[RATE LIMIT] League {league} was rate-limited.")
            matches_by_league[league] = []
            continue

        response.raise_for_status()
        data = response.json()

        all_matches = data.get("matches", [])

        # Debug print
        print(f"[DEBUG] {league}: API returned {len(all_matches)} matches.")

        upcoming_matches = []
        for match in all_matches:
            match_time = datetime.fromisoformat(
                match["utcDate"].replace("Z", "+00:00")
            )
            if match_time >= now_utc:
                upcoming_matches.append(match)

        matches_by_league[league] = upcoming_matches

    except Exception as e:
        print(f"[ERROR] League {league} fetch failed:", e)
        matches_by_league[league] = []

    time.sleep(1)  # rate-limit friendly   # waiting 1 second between requests

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
