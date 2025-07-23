import psutil
import smtplib
import json
import time
import threading
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import os

logging.basicConfig(
    filename='trading_monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_config(config_file='config.json'):
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load config: {e}")
        raise

def send_email_alert(subject, body, config):
    try:
        msg = MIMEMultipart()
        msg['From'] = config['smtp']['sender_email']
        msg['To'] = ', '.join(config['support_emails'])
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(config['smtp']['server'], config['smtp']['port']) as server:
            server.starttls()
            server.login(config['smtp']['sender_email'], config['smtp']['app_password'])
            server.sendmail(config['smtp']['sender_email'], config['support_emails'], msg.as_string())
        logging.info(f"Email alert sent: {subject}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

def send_daily_report(config, metrics_history):
    report = "Daily Trading Infrastructure Report\n\n"
    report += f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n"
    
    for metric, values in metrics_history.items():
        if values:
            avg = sum(values) / len(values)
            report += f"{metric}: Average = {avg:.2f}%\n"
    
    send_email_alert("Daily Trading Infrastructure Report", report, config)
    logging.info("Daily report sent")

def is_process_running(process_name):
    for proc in psutil.process_iter(['name']):
        if process_name.lower() in proc.info['name'].lower():
            return True
    return False

def monitor_system(config, metrics_history):
    thresholds = config['thresholds']
    processes = config['processes']
    
    while True:
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent

            metrics_history['CPU Usage'].append(cpu_usage)
            metrics_history['RAM Usage'].append(ram_usage)
            metrics_history['Disk Usage'].append(disk_usage)

            if cpu_usage > thresholds['cpu']:
                send_email_alert(
                    "High CPU Usage Alert",
                    f"CPU usage exceeded threshold: {cpu_usage}% (Threshold: {thresholds['cpu']}%)",
                    config
                )
            if ram_usage > thresholds['ram']:
                send_email_alert(
                    "High RAM Usage Alert",
                    f"RAM usage exceeded threshold: {ram_usage}% (Threshold: {thresholds['ram']}%)",
                    config
                )
            if disk_usage > thresholds['disk']:
                send_email_alert(
                    "High Disk Usage Alert",
                    f"Disk usage exceeded threshold: {disk_usage}% (Threshold: {thresholds['disk']}%)",
                    config
                )

            for process in processes:
                if not is_process_running(process):
                    send_email_alert(
                        f"Process Down Alert: {process}",
                        f"Critical trading process {process} is not running!",
                        config
                    )

        except Exception as e:
            logging.error(f"Error in monitoring: {e}")
        
        time.sleep(config['monitoring_interval'])

def schedule_daily_report(config, metrics_history):
    while True:
        now = datetime.datetime.now()
        target_time = datetime.datetime.strptime(config['daily_report_time'], '%H:%M').replace(
            year=now.year, month=now.month, day=now.day
        )
        if now >= target_time:
            send_daily_report(config, metrics_history)
            metrics_history.clear()
            metrics_history.update({'CPU Usage': [], 'RAM Usage': [], 'Disk Usage': []})
            target_time += datetime.timedelta(days=1)
        time.sleep(60)

def main():
    config = load_config()
    metrics_history = {'CPU Usage': [], 'RAM Usage': [], 'Disk Usage': []}

    monitor_thread = threading.Thread(target=monitor_system, args=(config, metrics_history))
    monitor_thread.daemon = True
    monitor_thread.start()

    report_thread = threading.Thread(target=schedule_daily_report, args=(config, metrics_history))
    report_thread.daemon = True
    report_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Shutting down monitoring system")
        print("Shutting down...")

if __name__ == "__main__":
    main()
