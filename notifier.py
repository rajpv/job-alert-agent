"""
Email Notification Module
Sends job alert emails via Gmail SMTP.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import pandas as pd
import config


def build_email_html(jobs_df: pd.DataFrame) -> str:
    """
    Build a clean, readable HTML email body from the jobs DataFrame.
    """
    job_count = len(jobs_df)
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; }}
            h2 {{ color: #2c5282; }}
            .summary {{ background: #ebf8ff; padding: 12px; border-radius: 8px; margin-bottom: 20px; }}
            .job-card {{
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 16px;
                margin-bottom: 12px;
                background: #fff;
            }}
            .job-title {{ font-size: 16px; font-weight: bold; color: #2b6cb0; margin: 0 0 4px 0; }}
            .company {{ font-size: 14px; color: #4a5568; margin: 0 0 4px 0; }}
            .details {{ font-size: 13px; color: #718096; margin: 0; }}
            .apply-btn {{
                display: inline-block;
                background: #3182ce;
                color: #fff !important;
                padding: 8px 16px;
                border-radius: 6px;
                text-decoration: none;
                font-size: 13px;
                margin-top: 8px;
            }}
            .footer {{ font-size: 12px; color: #a0aec0; margin-top: 30px; }}
        </style>
    </head>
    <body>
        <h2>🔔 New Job Alert</h2>
        <div class="summary">
            <strong>{job_count} new posting{"s" if job_count != 1 else ""}</strong> found on {timestamp}
        </div>
    """

    for _, job in jobs_df.iterrows():
        title = job.get("title", "N/A")
        company = job.get("company", "N/A")
        location = job.get("location", "N/A")
        site = str(job.get("site", "N/A")).capitalize()
        job_url = job.get("job_url", "#")
        date_posted = job.get("date_posted", "")

        # Format date if available
        date_str = ""
        if pd.notna(date_posted) and date_posted:
            try:
                date_str = pd.to_datetime(date_posted).strftime("%b %d, %Y")
            except Exception:
                date_str = str(date_posted)

        html += f"""
        <div class="job-card">
            <p class="job-title">{title}</p>
            <p class="company">{company}</p>
            <p class="details">📍 {location} &nbsp;|&nbsp; 🌐 {site}
            {"&nbsp;|&nbsp; 📅 " + date_str if date_str else ""}</p>
            <a class="apply-btn" href="{job_url}" target="_blank">View & Apply →</a>
        </div>
        """

    html += """
        <div class="footer">
            <p>This alert was sent by your Job Alert Agent.<br>
            Monitoring: LinkedIn, Indeed, Google Jobs</p>
        </div>
    </body>
    </html>
    """
    return html


def send_email_alert(jobs_df: pd.DataFrame) -> bool:
    """
    Send an email alert with the new job postings.
    Returns True if email was sent successfully.
    """
    if jobs_df.empty:
        print("No new jobs to send.")
        return False

    # Get credentials from environment variables
    sender_email = os.environ.get("GMAIL_ADDRESS", config.SENDER_EMAIL)
    app_password = os.environ.get("GMAIL_APP_PASSWORD", "")

    if not app_password:
        print("ERROR: GMAIL_APP_PASSWORD environment variable not set.")
        print("Please set it with: export GMAIL_APP_PASSWORD='your-16-char-app-password'")
        return False

    # Build the email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🔔 Job Alert: {len(jobs_df)} New Posting{'s' if len(jobs_df) != 1 else ''}"
    msg["From"] = sender_email
    msg["To"] = config.RECIPIENT_EMAIL

    # Attach HTML body
    html_body = build_email_html(jobs_df)
    msg.attach(MIMEText(html_body, "html"))

    # Send via Gmail SMTP
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, config.RECIPIENT_EMAIL, msg.as_string())
        print(f"✅ Email sent to {config.RECIPIENT_EMAIL} with {len(jobs_df)} jobs")
        return True
    except smtplib.SMTPAuthenticationError:
        print("ERROR: Gmail authentication failed.")
        print("Make sure you're using an App Password, not your regular password.")
        print("Create one at: https://myaccount.google.com/apppasswords")
        return False
    except Exception as e:
        print(f"ERROR sending email: {e}")
        return False


if __name__ == "__main__":
    # Test with sample data
    print("=" * 60)
    print("EMAIL NOTIFIER - TEST")
    print("=" * 60)

    sample_data = {
        "site": ["linkedin", "indeed"],
        "title": ["Recruiting Manager", "Senior TA Manager"],
        "company": ["Google", "Meta"],
        "location": ["San Francisco, CA", "Remote"],
        "job_url": ["https://linkedin.com/jobs/123", "https://indeed.com/jobs/456"],
        "date_posted": ["2026-04-02", "2026-04-02"],
    }
    sample_df = pd.DataFrame(sample_data)

    # Preview the HTML
    html = build_email_html(sample_df)
    with open("data/test_email.html", "w") as f:
        f.write(html)
    print("Test email HTML saved to data/test_email.html")
    print("To actually send, set GMAIL_APP_PASSWORD and run again.")
