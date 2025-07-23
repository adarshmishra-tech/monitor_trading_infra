Trading Infrastructure Monitor & Alert System
============================================

This is the ultimate tool for monitoring trading infrastructure on Kali Linux, designed for low-latency trading environments. It tracks system metrics (CPU, RAM, disk usage) and trading process liveness, sends real-time email alerts via SMTP/Gmail when issues are detected, and generates daily reports. The system is multi-threaded for efficiency and configurable via a JSON file.

Features
--------
- Monitors CPU, RAM, and disk usage with configurable thresholds
- Tracks critical trading processes for liveness
- Sends instant email alerts for threshold breaches or process failures
- Generates daily reports summarizing average system metrics
- Multi-threaded for non-blocking operation
- Logs all events to 'trading_monitor.log' for auditing
- Configurable via 'config.json'

Prerequisites
-------------
- Kali Linux (tested on 2025.1a)
- Python 3.11 or higher
- psutil library
- Internet connection for SMTP email delivery
- Gmail account with App Password for SMTP

Installation Steps
------------------
1. Update Kali Linux package repository:
   ```
   sudo apt update
   ```
   Note: If you encounter a missing key error (e.g., 827C8569F2518CC677FECA1AED65462EC8D5E4C5), download the new Kali repository signing key:
   ```
   wget -q -O - https://archive.kali.org/archive-key.asc | sudo apt-key add -
   sudo apt update
   ```

2. Install Python 3 and pip:
   ```
   sudo apt install python3 python3-pip
   ```

3. Install the psutil library:
   ```
   pip3 install psutil
   ```

4. Save the provided `monitor_trading_infra.py` and `config.json` files in the same directory (e.g., `/home/kali/trading_monitor/`).

5. Configure Gmail for SMTP:
   - Log in to your Gmail account.
   - Enable 2-Step Verification in Google Account settings.
   - Generate an App Password at https://myaccount.google.com/security (select "Other" app, name it "Trading Monitor").
   - Update `config.json` with your Gmail address and App Password:
     ```
     "sender_email": "your-email@gmail.com",
     "app_password": "your-app-password"
     ```

6. Customize `config.json`:
   - Update `support_emails` with recipient email addresses.
   - Adjust `thresholds` for CPU, RAM, and disk usage (percentage).
   - Specify `processes` to monitor (e.g., ["trading_app", "market_data_service"]).
   - Set `monitoring_interval` (seconds) for how often to check metrics.
   - Set `daily_report_time` (HH:MM, 24-hour format) for daily report generation.

Running the Tool
----------------
1. Navigate to the directory containing `monitor_trading_infra.py` and `config.json`:
   ```
   cd /home/kali/trading_monitor
   ```

2. Run the script:
   ```
   python3 monitor_trading_infra.py
   ```

3. The tool will:
   - Start monitoring system metrics and processes.
   - Log events to `trading_monitor.log`.
   - Send email alerts if thresholds are exceeded or processes are down.
   - Send a daily report at the specified time.

4. To stop the tool, press `Ctrl+C`. The system will shut down gracefully.

Troubleshooting
---------------
- Check `trading_monitor.log` for errors.
- Ensure `config.json` is valid JSON and contains correct SMTP credentials.
- Verify internet connectivity for email delivery.
- If processes are not detected, ensure process names match exactly (case-insensitive).
- For SMTP issues, confirm Gmail App Password and 2-Step Verification settings.

Security Notes
--------------
- This tool is designed for Kali Linux, optimized for security professionals.
- Ensure `config.json` permissions are restricted (e.g., `chmod 600 config.json`) to protect sensitive SMTP credentials.
- Regularly update Kali Linux and Python dependencies for security patches.

Support
-------
For issues or feature requests, contact the support team listed in `config.json` or refer to Kali Linux documentation at https://www.kali.org.
