# Daily Football Email Updates

This Python project automatically fetches football match data from multiple leagues and emails a daily summary in a clean HTML format. It is designed to run as a **Scheduled Task** in WSO2 Choreo and includes security and reliability features such as rate limiting and input validation.

---

## Features

- Fetches daily football matches from multiple leagues:
  - Premier League (PL)
  - La Liga (PD)
  - Serie A (SA)
  - Bundesliga (BL1)
  - Ligue 1 (FL1)
  - Major League Soccer (MLS)
  - UEFA Champions League (CL)
- Formats the match data into a clean HTML table
- Highlights matches involving specific teams (e.g., Barcelona) in red
- Sends automated daily emails
- Includes **security and reliability features**:
  - **Rate limiting** to prevent API overuse  
  - **Input validation** for dates and league codes  
  - Sensitive data is handled securely through **Choreo secrets**

---

## Project Structure

    main.py              # Fetches match data, formats HTML, and sends emails  
    requirements.txt     # Dependencies (requests)

---

## Security Features

### 1. Secrets Handling
- API keys, SMTP credentials, and all sensitive values are **not hardcoded**.
- Choreo environment variables are toggled as **secrets**, which encrypt and protect the data.

### 2. Rate Limiting
- A delay is added between API calls to avoid exceeding allowed request quotas.
- Helps prevent accidental API abuse.

### 3. Input Validation
- Date format (`YYYY-MM-DD`) is validated before making requests.
- Only valid league codes are processed to ensure API safety and predictable outputs.

---

## Setup & Local Testing

### 1. Clone the repository

    git clone https://github.com/<YOUR_USERNAME>/daily-football-email.git
    cd daily-football-email

### 2. Install dependencies

    pip install -r requirements.txt

### 3. Set environment variables (for local testing)

    export FOOTBALL_API_KEY="your_api_key_here"
    export EMAIL_TO="recipient@example.com"
    export EMAIL_FROM="sender@example.com"
    export SMTP_PASS="your_smtp_password"

### 4. Run the script

    python main.py

If configured correctly, you will receive an HTML email with that day’s football matches.


