import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_alert_log():
    log_path = os.path.join(BASE_DIR, "crypto_alert_tool", "alerts_log.json")
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            return json.load(f)
    return {}

def save_alert_log(alert_log):
    log_path = os.path.join(BASE_DIR, "crypto_alert_tool", "alerts_log.json")
    with open(log_path, "w") as f:
        json.dump(alert_log, f, indent=4)

def is_alert_sent(alert_log, date, alert_type):
    return alert_log.get(str(date), "") == alert_type

def log_alert(alert_log, date, alert_type):
    alert_log[str(date)] = alert_type
    save_alert_log(alert_log)

