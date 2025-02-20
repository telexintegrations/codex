# Codex: Telex Coding Challenge Integration

Codex is a [Telex](https://telex.im) integration that posts a coding challenge from [Codewars](https://www.codewars.com) in a specified channel every morning.
This helps developers enhance their problem-solving skills daily.

## Features

- Automatically fetches and posts a new Codewars challenge every day.
- Provides a direct link to the challenge for easy access.
- Encourages continuous skill improvement through daily problem-solving.
- Configurable interval for challenge posting.

## Setup Instructions

### Prerequisites

- Python 3.8+
- [Flask](https://flask.palletsprojects.com/)
- [httpx](https://www.python-httpx.org/)
- Telex account

### Installation

1. Clone this repository:

   ```sh
   git clone https://github.com/tonybnya/codex.git
   cd codex
   ```

2. Create and activate a virtual environment:

   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\\Scripts\\activate
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Create a `.env` file and add the necessary configuration:

   ```sh
   FLASK_PORT=5000
   FLASK_DEBUG=True
   ```

5. Run the Flask server:

   ```sh
   python3 main.py
   ```

### Configuration

The integration exposes a `GET` endpoint `/coding_challenge` where Telex can fetch metadata about the app.

- **Tick URL**: This is the webhook Telex will call periodically.
  - Endpoint: `POST /tick`
  - Payload:

    ```json
    {
      "channel_id": "<telex_channel_id>",
      "return_url": "<telex_webhook_url>",
      "settings": [
        {"label": "interval", "type": "text", "required": true, "default": "0 9 * * *"}
      ]
    }
    ```

## Testing the Integration

You can manually test the integration by triggering a tick request:

```sh
curl -X POST http://localhost:5000/tick -H "Content-Type: application/json" -d '{"channel_id": "your_channel_id", "return_url": "your_return_url", "settings": [{"label": "interval", "type": "text", "required": true, "default": "0 9 * * *"}]}'
```

OR

You can run Unit Tests:

```sh
pytest -v
```

## Deployment

### Using Docker

1. Build the Docker image:

   ```sh
   docker build -t codex .
   ```

2. Run the container:

   ```sh
   docker run -d -p 5003:5003 codex
   ```

### Deploying to a Server

- Set up a reverse proxy with Nginx or Apache.
- Use a process manager like `gunicorn` or `supervisor` to keep the app running.
- Use a Cloud service (like Render, Vercel, AWS).

## Screenshots

![Screenshot 1](https://i.postimg.cc/dVyYrJbz/codex-1.png)
![Screenshot 2](https://i.postimg.cc/KvVb11HP/codex-2.png)
![Screenshot 3](https://i.postimg.cc/1z017J5B/codex-3.png)
![Screenshot 4](https://i.postimg.cc/q7HdG90g/codex-4.png)
![Screenshot 5](https://i.postimg.cc/DZBkn0Gb/codex-5.png)
![Screenshot 6](https://i.postimg.cc/5yyc0J5K/codex-6.png)
![Screenshot 7](https://i.postimg.cc/KjH63WJG/codex-7.png)

## Contributing

Feel free to open issues or submit pull requests for improvements!
