import base64
import os
import re
from datetime import datetime
from io import BytesIO

import requests
import yaml
from flask import Flask, send_file, request, jsonify

app = Flask(__name__)
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')


def is_valid_email(email):
    return re.match(EMAIL_REGEX, email) is not None


def create_tracking_pixel():
    pixel = BytesIO()
    pixel.write(
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b')
    pixel.seek(0)
    return pixel


def send_telegram_notification(email_id, ip_address, location_data):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = (
        f"📧 Email Opened!\n"
        f"Email ID: {email_id}\n"
        f"IP Address: {ip_address}\n"
        f"Time: {timestamp}"
        f"\n\nLocation Data: {location_data}"
    )

    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }

    try:
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        print(f"Error sending Telegram notification: {e}")
        return None


@app.route('/<email_id>')
def track_email(email_id):
    decoded_email = ""
    try:
        email = base64.b64decode(email_id).decode('utf-8')
        decoded_email = email
        if not is_valid_email(decoded_email):
            return jsonify({"error": "Invalid email address"}), 400

    except Exception as e:
        return jsonify({"error": "Invalid email address"}), 400

    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    location_data = {}
    try:
        response = requests.get(f'https://ipinfo.io/{ip_address}/json')
        if response.status_code == 200:
            data = response.json()
            location_data = {
                "IP": ip_address,
                "City": data.get("city", "Unknown"),
                "Region": data.get("region", "Unknown"),
                "Country": data.get("country", "Unknown"),
                "Postal Code": data.get("postal", "Unknown"),
                "Coordinates": data.get("loc", "Unknown"),
                "ISP": data.get("org", "Unknown"),
                "Time Zone": data.get("timezone", "Unknown"),
            }
    except Exception as e:
        print(f"Error fetching location: {e}")

    location_data_yaml = yaml.dump(location_data, default_flow_style=False)
    send_telegram_notification(decoded_email, ip_address, location_data_yaml)

    tracking_pixel = create_tracking_pixel()
    return send_file(
        tracking_pixel,
        mimetype='image/gif',
        as_attachment=False
    )


if __name__ == '__main__':
    app.run(debug=True)
