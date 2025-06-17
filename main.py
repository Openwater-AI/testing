from flask import Flask, request, jsonify
import os
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fetch verify token from environment (default is for local dev/testing)
VERIFY_TOKEN = os.getenv("STRAVA_VERIFY_TOKEN", "openwater-secret-token")

app = Flask(__name__)

@app.route("/strava-webhook", methods=["GET", "POST"])
def strava_webhook():
    if request.method == "GET":
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        mode = request.args.get("hub.mode")

        if verify_token == VERIFY_TOKEN and mode == "subscribe":
            logger.info("✅ Verified webhook GET — returning challenge: %s", challenge)
            return jsonify({"hub.challenge": challenge}), 200
        else:
            logger.warning("❌ Unauthorized GET attempt")
            return "Unauthorized", 403

    if request.method == "POST":
        logger.info("📬 Webhook Received, Slim!")
        data = request.get_json()
        if data is None:
            logger.warning("⚠️ No JSON received in POST")
        else:
            logger.info("Payload: %s", data)
        return '', 200

@app.route("/strava-webhook-new", methods=["GET", "POST"])
def strava_webhook_new():
    if request.method == "GET":
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        mode = request.args.get("hub.mode")

        if verify_token == VERIFY_TOKEN and mode == "subscribe":
            logger.info("✅ Verified NEW webhook GET — returning challenge: %s", challenge)
            return jsonify({"hub.challenge": challenge}), 200
        else:
            logger.warning("❌ Unauthorized GET attempt on NEW webhook")
            return "Unauthorized", 403

    if request.method == "POST":
        logger.info("📬 NEW Webhook Received, Slim!")
        data = request.get_json()
        if data is None:
            logger.warning("⚠️ No JSON received in POST (NEW)")
        else:
            logger.info("Payload (NEW): %s", data)
        return '', 200

@app.route("/oauth/callback", methods=["GET"])
def oauth_callback():
    code = request.args.get("code")
    scope = request.args.get("scope")
    logger.info("Received OAuth code: %s, scope: %s", code, scope)
    return f"OAuth code received: {code}", 200

@app.route("/")
def home():
    return "🏃 Strava Webhook Listener Running Like A Boss", 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)