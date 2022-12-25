#!/usr/bin/env python
from os import environ, path, makedirs

from pydantic import ValidationError
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from src.app.commands.command_handlers import Commands
from src.app.config.config_loader import ConfigLoader
from src.domain.authentication import Auth
from src.domain.validators.env_validator import EnvValidator
from src.infrastructure.sqlite import Database

config = ConfigLoader.set_config()
auth = Auth(Database())

commands = Commands(auth, config)


def initialise() -> None:
    if not path.exists("logs"):
        makedirs("logs")

    Database.initialise()
    env = EnvValidator()
    env.verify_required_env_variables_exist(config.radarr.enabled)
    if not env.is_valid:
        raise ValidationError(
            f"Unable to start app as the following required env variables are missing: {''.join(env.reasons)}")


def main() -> None:
    updater = Updater(environ.get("TELEGRAM_BOT_KEY"))

    updater.dispatcher.add_handler(CommandHandler(config.lookarr.search_all_command, commands.search_all_command))
    updater.dispatcher.add_handler(CommandHandler(config.lookarr.search_series_command, commands.search_all_command))
    updater.dispatcher.add_handler(CommandHandler(config.lookarr.search_movie_command, commands.search_all_command))
    updater.dispatcher.add_handler(CallbackQueryHandler(commands.button_pressed))
    updater.dispatcher.add_handler(CommandHandler('help', commands.help_command))
    updater.dispatcher.add_handler(CommandHandler('auth', commands.auth_command))

    # Start bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    initialise()
    main()
