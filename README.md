# phishing_simulation_tool
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
