# Lookarr
Telegram bot for managing Sonarr and Radarr. 

-- Still under development. --

## How to run
Requires env variables:
- TELEGRAM_BOT_KEY
- LOOKARR_AUTH_PASSWORD

Rename config-sample.yml to config.yml before running

/auth <LOOKARR_AUTH_PASSWORD> is required when calling the bot the first time.

Adding chat ids on the "strict_mode_allowed_ids" section within the config file enables "strict mode". This means the bot will stay silent if it's contacted by users which are not in the strict_mode_allowed_ids list.

Entrypoint: src/app/main.py
