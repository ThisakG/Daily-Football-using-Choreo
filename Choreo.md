# Choreo Deployment Instructions

## 1. Fork the Repository
Fork this repository to your GitHub account.

## 2. Log In to Choreo
Log in to your WSO2 Choreo account.

## 3. Create a Scheduled Task
- Go to **Create → Scheduled Task**.

## 4. Provide Component Details
- **Name:** daily-football-email  
- **Build:** Python  
- **Project Directory:** Root (where `main.py` resides)  
- **Branch:** main  

## 5. Add Environment Variables

| Variable           | Description                        | Secret |
|-------------------|------------------------------------|--------|
| FOOTBALL_API_KEY  | Your football API key              | Yes    |
| EMAIL_TO          | Recipient email address            | No     |
| EMAIL_FROM        | Sender email address               | No     |
| SMTP_PASS         | SMTP app password                  | Yes    |
| SMTP_SERVER       | SMTP server (default: smtp.gmail.com) | No  |
| SMTP_PORT         | SMTP port (default: 587)           | No     |

> Make sure to toggle sensitive values as **secrets**.

## 6. Deploy the Component
Click **Deploy** and wait for the build to complete.

## 7. Manual Test Run
Go to **Execute → Run it** to test that the service sends an email successfully.

## 8. Set a Schedule
Configure a daily schedule, e.g.:

- **Every day at 08:00 AM**

This triggers automatic email delivery.

---

# Dependencies

- Python 3.x  
- `requests` library  

---

# Notes & Best Practices

- **Never commit API keys or SMTP passwords to GitHub.**  
- Always store sensitive values using **Choreo secrets**.
- Adjust rate limiting in `main.py` (e.g., `time.sleep(1)`) based on API limits.
- Customize tracked leagues by editing the `LEAGUES` list.
- For production, ensure the sender email uses **app passwords** (Gmail 2FA recommended).
