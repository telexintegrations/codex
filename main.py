"""
Main application.
"""
import asyncio
import logging
import os
import random
from typing import List
import httpx
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from pydantic import BaseModel
from utils import katas


# load environment variables from .env
load_dotenv()

# configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# initialize Flask app
app = Flask(__name__)


class Setting(BaseModel):
    """ Setting model. """
    label: str
    type: str
    required: bool
    default: str


class MonitorPayload(BaseModel):
    """ Payload model. """
    channel_id: str
    return_url: str
    settings: List[Setting]


# list of allowed origins
allowed_origins = [
    "https://telex.im",
    "https://staging.telex.im",
    "http://telextest.im",
    "http://staging.telextest.im"
]

# enable CORS for specific origins
CORS(app, origins=allowed_origins)


@app.route("/", methods=["GET"])
def root():
    """ Root endpoint returning a JSON message. """
    logger.info("Root endpoint accessed")
    return jsonify(
        {
            "app_name": "Codex",
            "description": "A Telex integration/plugin that sends a coding challenge in a channel every morning to sharpen developer skills.",
            "type": "Interval Integration",
            "category": "Development & Code Management"
        }
    )


@app.route("/coding_challenge", methods=["GET"])
def get_coding_challenge():
    """ Endpoint to get a coding challenge. """
    app_url = "https://tonybnya-codex.onrender.com/coding_challenge"
    codewars_base_url = "https://www.codewars.com/kata"
    kata_id = random.choice(katas)

    kata = f"{codewars_base_url}/{kata_id}"
    return jsonify(
        {
            "data": {
                "date": {
                    "created_at": "2025-02-19",
                    "updated_at": "2025-02-19"
                },
                "descriptions": {
                    "app_description": "Posts a coding challenge every morning to sharpen developer skills.",
                    "app_logo": "https://i.postimg.cc/5Nn52jM9/codex.png",
                    "app_name": "Codex",
                    "app_url": app_url,
                    "background_color": "#151515"
                },
                "integration_category": "Development & Code Management",
                "integration_type": "interval",
                "is_active": True,
                "author": "Tony B. NYA",
                "key_features": [
                    "Automatically fetches a new Codewars challenge every day.",
                    "Provides a direct link to the challenge for easy access.",
                    "Encourages continuous skill improvement through daily problem-solving."
                ],
                "settings": [
                    {
                        "label": "interval",
                        "type": "text",
                        "required": True,
                        "default": "* * * * *"
                    }
                ],
                "tick_url": f"{kata}/tick",
            }
        }
    )


# def coding_challenge(payload: MonitorPayload):
async def coding_challenge(payload: MonitorPayload):
    """Monitor websites and send a report to the return URL."""
    codewars_base_url = "https://www.codewars.com/kata"
    kata_id = random.choice(katas)

    kata = f"{codewars_base_url}/{kata_id}"

    data = {
        "message": kata,
        "username": "Coding Challenge",
        "event_name": "Uptime Check",
        "status": "error"
    }

    async with httpx.AsyncClient() as client:
        await client.post(payload.return_url, json=data)


@app.route("/tick", methods=["POST"])
def tick():
    """Flask route to handle monitoring requests."""
    try:
        payload = MonitorPayload(**request.json)
        asyncio.create_task(coding_challenge(payload))
        return jsonify({"message": "Coding Challenge delivered"}), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    # load configuration from environment variables
    debug_mode = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    port = int(os.getenv("FLASK_PORT", 5003))

    logger.info(f"Starting Flask app on port {port} with debug={debug_mode}")
    app.run(debug=debug_mode, host="0.0.0.0", port=port)
