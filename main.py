import os
import logging
from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from utils import integration, katas


# load environment variables from .env
load_dotenv()

# configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# initialize Flask app
app = Flask(__name__)

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
    """ Root endpoint returning a JSON message """
    logger.info("Root endpoint accessed")
    return jsonify(
        {
            "app_name": "Codex",
            "description": "A Telex integration/plugin that sends a coding challenge in a channel every morning to sharpen developer skills.",
            "type": "Interval Integration",
            "category": "Development & Code Management"
        }
    )


if __name__ == "__main__":
    # load configuration from environment variables
    debug_mode = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    port = int(os.getenv("FLASK_PORT", 5003))

    logger.info(f"Starting Flask app on port {port} with debug={debug_mode}")
    app.run(debug=debug_mode, host="0.0.0.0", port=port)
