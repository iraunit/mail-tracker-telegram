Email Tracking Application

This is a simple Flask application for tracking email opens. The application generates a tracking pixel that, when opened, sends a notification to a Telegram bot with the email ID, IP address, timestamp, and user location.

Features
	1.	Tracks email opens using a tracking pixel.
	2.	Decodes and validates base64-encoded email IDs.
	3.	Captures user details:
	•	IP address
	•	Location (City, Region, Country, etc.)
	•	Internet Service Provider (ISP)
	•	Coordinates (latitude/longitude)
	•	Time zone
	4.	Sends notifications to a Telegram bot with the collected data.
	5.	Returns a transparent 1x1 GIF as the tracking pixel.

Requirements

Python Libraries
	•	Flask
	•	requests
	•	pyyaml

Install the required packages using:

pip install Flask requests pyyaml

Environment Variables

The application requires the following environment variables to be set:
	1.	TELEGRAM_BOT_TOKEN: Token for your Telegram bot.
	2.	TELEGRAM_CHAT_ID: Chat ID where notifications will be sent.

Set them in your environment:

export TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
export TELEGRAM_CHAT_ID="your_telegram_chat_id"

Usage

Running the Application

Run the Flask app:

python app.py

The application will start on http://127.0.0.1:5000.

Generating the Tracking URL
	1.	Encode the email ID in base64:

import base64
email = "example@example.com"
encoded_email = base64.b64encode(email.encode()).decode()
print(encoded_email)


	2.	Use the encoded email to generate the URL:

http://127.0.0.1:5000/<encoded_email>



Embedding the Tracking Pixel

Embed the URL as an <img> tag in your emails:

<img src="http://127.0.0.1:5000/<encoded_email>" alt="" style="display:none;">

When the email is opened, the tracking pixel will trigger the backend to collect the user’s information.

API Endpoints

GET /<email_id>

Description: Accepts a base64-encoded email ID, decodes and validates it, and sends a tracking notification to Telegram.
	•	Request Parameters:
email_id: A base64-encoded string of the email address.
	•	Response:
Returns a transparent tracking pixel (1x1 GIF).
	•	Error Responses:
	•	400: If the email ID is invalid or improperly encoded.

How It Works
	1.	The user opens the email containing the tracking pixel.
	2.	The server decodes the base64 email ID and validates it.
	3.	Captures IP and geolocation data using the ipinfo.io API.
	4.	Sends the captured data to a Telegram bot.
	5.	Returns the tracking pixel (1x1 transparent GIF).

Sample Telegram Notification

📧 Email Opened!
Email ID: example@example.com
IP Address: 192.168.1.1
Time: 2025-01-16 10:30:00

Location Data:
City: New York
Region: New York
Country: US
Postal Code: 10001
Coordinates: 40.7128,-74.0060
ISP: Verizon Communications
Time Zone: America/New_York

Improvements
	•	Add support for logging to a database.
	•	Enhance error handling for various scenarios (e.g., invalid IP response).
	•	Use a more secure email ID verification mechanism.

Security Note

This project is for educational purposes only. Tracking email opens may be subject to privacy laws like GDPR. Ensure compliance with applicable regulations before deploying.