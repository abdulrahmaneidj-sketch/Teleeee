# ECG Telegram Bot (ready-to-deploy)

**Important:** This package does NOT include any secrets. Add your TELEGRAM_TOKEN and OPENAI_API_KEY as environment variables before running.

## Files in this package
- `main.py` : Bot implementation (reads credentials from environment variables)
- `requirements.txt` : Python dependencies
- `Procfile` : For Railway or Heroku style deployments (worker)
- `README.md` : This file
- `.gitignore`

## Quick local test (recommended)
1. Create a Python virtual environment (Python 3.9+ recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS / Linux
   venv\Scripts\activate    # Windows
   ```
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Set environment variables (do NOT paste keys in public chat)
   ```bash
   export TELEGRAM_TOKEN="your-telegram-token"
   export OPENAI_API_KEY="sk-..."
   ```
   On Windows (PowerShell):
   ```powershell
   $env:TELEGRAM_TOKEN = "your-telegram-token"
   $env:OPENAI_API_KEY = "sk-..."
   ```
4. Run locally
   ```bash
   python main.py
   ```

## Deploying to Railway
1. Create a new Railway project and link your repo / upload files.
2. Add Project Variables in Railway:
   - `TELEGRAM_TOKEN` : your Telegram Bot token (from BotFather)
   - `OPENAI_API_KEY` : your OpenAI secret key (sk-...)
3. Ensure the `Procfile` is present and Railway uses the `worker` service.
4. Deploy. Check **Logs** if the worker crashes.

## Troubleshooting (most common causes of crash)
- **ModuleNotFoundError**: make sure `requirements.txt` is present and Railway installs deps.
- **Missing env vars**: The app will exit if TELEGRAM_TOKEN or OPENAI_API_KEY aren't set.
- **Leaked or revoked keys**: If you previously exposed a key, revoke it on the provider dashboard and create a new one.

## Security notes
- Never share `TELEGRAM_TOKEN` or `OPENAI_API_KEY` in chat. If accidentally exposed, **revoke** and rotate immediately.
- Keep usage limits and billing in mind on OpenAI; monitor your usage.

## Need me to deploy it for you?
I cannot access your Railway account or deploy on your behalf. I can guide you step-by-step while you perform the actions and inspect logs in real time.
