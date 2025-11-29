# Daily Football Email Updates ⚽
<p>
As an avid football fan, I always do my best to keep up with all the matches that will happen throughout the week mainly through social media, and a couple of footballing apps in my phone. 
Now, it's all fun and games when you have the time to scroll through five or so different apps, but not so much when you start to miss out on match info since life keeps you busy with uni assignments and other committments.   
</p>

<p>
I do not like missing out on the action at all. So as a solution to keep myself updated daily on that matches that will be played on that day, 
I created a scheduled task workflow using WSO2's Choreo: a cloud-native integration and development platform. 
This workflow uses a custom python script automatically fetches football match data from multiple leagues and emails a daily summary in a clean HTML format
</p>
<br>
<p>
🧐What the python script does:
</p>
<p>
The script fetches today’s football matches from an API for several leagues, formats the results into a clean HTML email, and highlights important matches. 
It then connects to an SMTP server using secure credentials and sends the formatted update to your email. 
Choreo runs this script automatically on a schedule so you receive daily match summaries without the need for manual configuration.
</p>
<br>
<p>
Choreo Dashboard: https://console.choreo.dev/organizations/footballmail/projects/dailyfootball/home
</p>

---

## 👓 Features

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

## 👾 Security Features

<p>As a Cybersecurity undergrad, I wanted this workflow to follow good security practices rather than just “function correctly.” To strengthen the reliability and safety of the solution, the below listed mechanisms were added:</p>

### 1. Secrets Handling
- API keys, SMTP credentials, and all sensitive values are **not hardcoded**. Instead they're stored in the Choreo environment variables and are toggled as **secrets**, which encrypt and protect the data.

### 2. Rate Limiting
- A delay is added between API calls to avoid exceeding allowed request quotas.
- This Helps prevent accidental API abuse.

### 3. Input Validation
- Date format (`YYYY-MM-DD`) is validated before making requests.
- Only valid league codes are processed to ensure API safety and predictable outputs.

---

## ⚒ Setup & Local Testing

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


