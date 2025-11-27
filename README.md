# Daily Football Email Updates

This Python project automatically fetches football match data from multiple leagues and emails a daily summary in a clean HTML format. It is designed to run as a **Scheduled Task** in WSO2 Choreo and includes security and reliability features such as rate limiting and input validation.

---

## **Features**

- Fetches daily football matches from multiple leagues:
  - Premier League (PL)
  - La Liga (PD)
  - Serie A (SA)
  - Bundesliga (BL1)
  - Ligue 1 (FL1)
  - Major League Soccer (MLS)
  - UEFA Champions League (CL)
- Formats the match data in a clean HTML table
- Highlights matches involving specific teams (e.g., Barcelona) in red
- Sends automated daily emails
- Includes **security and reliability features**:
  - **Rate limiting** to prevent API overuse
  - **Input validation** for dates and league codes
  - Sensitive data is handled securely through **Choreo secrets**

---

## **Project Structure**


- `main.py`  
  Fetches match data, formats HTML, and sends emails.
- `requirements.txt`  
  Contains `requests` library for API calls.

---

## **Security Features**

1. **Secrets Handling**  
   - API keys, SMTP credentials, and other sensitive values are **never hardcoded**.
   - Choreo environment variables are toggled as **secrets** to encrypt and protect them.

2. **Rate Limiting**  
   - Adds a delay between API requests to respect API limits.
   - Helps prevent accidental abuse of football data APIs.

3. **Input Validation**  
   - Validates the date format (`YYYY-MM-DD`) before making API calls.
   - Ensures only valid league codes are queried.

---

## **Setup & Local Testing**

1. Clone the repository:

```bash
git clone https://github.com/<YOUR_USERNAME>/daily-football-email.git
cd daily-football-email
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set environment variables locally (optional for testing):

bash
Copy code
export FOOTBALL_API_KEY="your_api_key_here"
export EMAIL_TO="recipient@example.com"
export EMAIL_FROM="sender@example.com"
export SMTP_PASS="your_smtp_password"
Run the script:

bash
Copy code
python main.py
You should receive an HTML email with today’s football matches.




