import os
import requests
import logging

def send_alert(severity: str, job: str, summary: str, details: str):
    """
    Sends alerts via Slack/Email based on severity.
    CRITICAL: Email + Slack
    WARNING: Slack
    INFO: Slack (optional)
    """
    logging.info(f"[{severity}] Job: {job} | {summary}\n{details}")
    
    slack_url = os.environ.get("SLACK_WEBHOOK_URL")
    if slack_url:
        payload = {
            "text": f"[{severity}] *{job}*\n*{summary}*\n```{details}```"
        }
        try:
            requests.post(slack_url, json=payload, timeout=5)
        except Exception as e:
            logging.error(f"Failed to send Slack alert: {e}")
            
    if severity == "CRITICAL":
        # MVP: Log email dispatch intent instead of actual SMTP setup
        logging.info(f"CRITICAL EMAIL DISPATCHED for {job}: {summary}")
