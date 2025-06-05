import smtplib
import argparse
import time
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

TRACKING_LOG = "tracking_log.txt"

class TrackerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        with open(TRACKING_LOG, 'a') as log:
            log.write(f"Opened: {self.path} at {time.ctime()} from {self.client_address[0]}\n")
        self.send_response(200)
        self.send_header('Content-type', 'image/gif')
        self.end_headers()
        self.wfile.write(b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b")

def start_tracker_server(port=8000):
    server = HTTPServer(('0.0.0.0', port), TrackerHandler)
    print(f"[*] Tracking server running on port {port}...")
    server.serve_forever()

def send_phishing_email(smtp_server, port, sender, recipient, subject, body, tracking_url):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    html_content = f"""
    <html>
      <body>
        <p>{body}</p>
        <img src='{tracking_url}/{uuid.uuid4()}.gif' width='1' height='1'>
      </body>
    </html>
    """
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(smtp_server, port) as server:
        server.sendmail(sender, recipient, msg.as_string())
    print("[+] Phishing email sent.")

def main():
    parser = argparse.ArgumentParser(description="Phishing Simulation Tool (For Educational Use Only)")
    parser.add_argument("--smtp", required=True, help="SMTP server")
    parser.add_argument("--port", type=int, default=25, help="SMTP port")
    parser.add_argument("--sender", required=True, help="Sender email")
    parser.add_argument("--recipient", required=True, help="Recipient email")
    parser.add_argument("--subject", default="Important Update", help="Email subject")
    parser.add_argument("--body", default="Please see the update.", help="Email body")
    parser.add_argument("--tracker", default="http://localhost:8000", help="Tracking URL base")
    args = parser.parse_args()

    thread = Thread(target=start_tracker_server, daemon=True)
    thread.start()

    time.sleep(1)  # Let the server start
    send_phishing_email(args.smtp, args.port, args.sender, args.recipient, args.subject, args.body, args.tracker)

    print("[*] Waiting for email to be opened...")
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n[!] Exiting...")

if __name__ == "__main__":
    main()

"""
# README: Phishing Simulation Tool

## Description
This tool is designed **for educational and awareness training purposes only**. It simulates phishing emails and tracks when recipients open them using a tracking pixel.

## Features
- Sends an HTML email with an embedded tracking pixel
- Logs IP address and timestamp when the email is opened
- Simple HTTP server for tracking opens

## Usage
```bash
python phishing_simulation_tool.py \
  --smtp smtp.example.com \
  --port 25 \
  --sender attacker@example.com \
  --recipient victim@example.com \
  --subject "Security Alert" \
  --body "Your account requires verification." \
  --tracker http://yourserver.com:8000
```

## Requirements
- Python 3.x
- Internet/network access for email delivery

## Ethical Disclaimer
**This tool is for educational and organizational training simulations only. Do not use it against others without explicit permission.**

## License
MIT License
"""