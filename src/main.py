#!/usr/bin/env python
from os import environ, path, makedirs

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from src.domain.handlers.conversation import SearchHandler
from src.domain.config.app_config import ConfigLoader
from src.domain.handlers.authentication import AuthHandler
from src.domain.handlers.help import HelpHandler
from src.domain.handlers.stop import StopHandler
from src.domain.authentication import Auth
from src.domain.validators.env_validator import EnvValidator
from src.infrastructure.db.sqlite import Database
from src.infrastructure.media_server_factory import MediaServerFactory


config = ConfigLoader.set_config()
auth = Auth(Database())
mediaServerFactory = MediaServerFactory(config)
authenticationHandler = AuthHandler(auth, config.lookarr)
helpHandler = HelpHandler()
stopHandler = StopHandler(authenticationHandler)
conversationHandler = SearchHandler(authenticationHandler, stopHandler, config, mediaServerFactory)


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

    updater.dispatcher.add_handler(CommandHandler(config.lookarr.search_all_command, conversationHandler.search))
    updater.dispatcher.add_handler(CallbackQueryHandler(conversationHandler.searchMedia, pattern="Movie"))
    updater.dispatcher.add_handler(CallbackQueryHandler(conversationHandler.goToPreviousOrNextOption,
                                                        pattern="Next|Previous"))
    updater.dispatcher.add_handler(CallbackQueryHandler(conversationHandler.getFolders, pattern="Add"))
    updater.dispatcher.add_handler(CallbackQueryHandler(conversationHandler.getQualityProfiles, pattern="Path"))
    updater.dispatcher.add_handler(CallbackQueryHandler(conversationHandler.addToLibrary, pattern="Quality"))
    updater.dispatcher.add_handler(CallbackQueryHandler(conversationHandler.confirmDelete,
                                                        pattern="ConfirmDelete"))
    updater.dispatcher.add_handler(CallbackQueryHandler(conversationHandler.delete, pattern="Delete"))
    updater.dispatcher.add_handler(CallbackQueryHandler(stopHandler.stop, pattern="Stop"))
    # updater.dispatcher.add_handler(CallbackQueryHandler(handlers.add, pattern="Add_This"))
    updater.dispatcher.add_handler(CommandHandler('help', helpHandler.help))
    updater.dispatcher.add_handler(CommandHandler('auth', authenticationHandler.authenticate))

    # Start bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    initialise()
    main()
