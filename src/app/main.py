#!/usr/bin/env python
from os import environ, path, makedirs

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from src.app.commands.handlers import CommonHandlers
from src.app.config.config_loader import ConfigLoader
from src.domain.authentication import Auth
from src.domain.validators.env_validator import EnvValidator
from src.infrastructure.sqlite import Database

config = ConfigLoader.set_config()
auth = Auth(Database())

common_handlers = CommonHandlers(auth, config)


def initialise() -> None:
    if not path.exists("logs"):
        makedirs("logs")

    Database.initialise()
    env = EnvValidator()
    env.verify_required_env_variables_exist(config.radarr.enabled)
    if not env.is_valid:
        raise ValueError(
            f"Unable to start app as the following required env variables are missing: {''.join(env.reasons)}")


def main() -> None:
    updater = Updater(environ.get("TELEGRAM_BOT_KEY"))

    updater.dispatcher.add_handler(CommandHandler(config.lookarr.search_all_command, common_handlers.search_type))
    updater.dispatcher.add_handler(CommandHandler(config.lookarr.search_series_command, common_handlers.search_type))
    updater.dispatcher.add_handler(CommandHandler(config.lookarr.search_movie_command, common_handlers.search_type))
    updater.dispatcher.add_handler(CallbackQueryHandler(common_handlers.searchMedia, pattern="Movie"))
    updater.dispatcher.add_handler(CallbackQueryHandler(common_handlers.goToPreviousOrNextOption, pattern="Next|Previous"))
    updater.dispatcher.add_handler(CallbackQueryHandler(common_handlers.getFolders, pattern="Add"))
    updater.dispatcher.add_handler(CallbackQueryHandler(common_handlers.getQualityProfiles, pattern="Path"))
    updater.dispatcher.add_handler(CallbackQueryHandler(common_handlers.add, pattern="Quality"))
    updater.dispatcher.add_handler(CallbackQueryHandler(common_handlers.stop, pattern="Stop"))
    # updater.dispatcher.add_handler(CallbackQueryHandler(common_handlers.add, pattern="Add_This"))
    updater.dispatcher.add_handler(CommandHandler('help', common_handlers.help_command))
    updater.dispatcher.add_handler(CommandHandler('auth', common_handlers.auth))

    # Start bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    initialise()
    main()
