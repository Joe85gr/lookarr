#!/usr/bin/env python
from os import environ, path, makedirs

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from src.domain.handlers.conversation_handler import SearchHandler
from src.domain.config.app_config import config
from src.domain.handlers.authentication_handler import AuthHandler
from src.domain.handlers.help_handler import HelpHandler
from src.domain.handlers.stop_handler import stop_handler
from src.domain.validators.env_validator import EnvValidator
from src.infrastructure.db.sqlite import db
from src.infrastructure.media_server_factory import MediaServerFactory


mediaServerFactory = MediaServerFactory()
authenticationHandler = AuthHandler()
helpHandler = HelpHandler()

conversationHandler = SearchHandler(mediaServerFactory)


def initialise() -> None:
    if not path.exists("logs"):
        makedirs("logs")

    db.initialise()
    env = EnvValidator()
    env.verify_required_env_variables_exist(config.radarr.enabled)
    if not env.is_valid:
        raise ValueError(
            f"Unable to start app as the following required env variables are missing: {''.join(env.reasons)}")


def main() -> None:
    updater = Updater(environ.get("TELEGRAM_BOT_KEY"))

    updater.dispatcher.add_handler(CommandHandler(config.lookarr.search_all_command, conversationHandler.search))
    updater.dispatcher.add_handler(CallbackQueryHandler(conversationHandler.search_media, pattern="Movie"))
    updater.dispatcher.add_handler(CallbackQueryHandler(conversationHandler.change_option,
                                                        pattern="Next|Previous"))
    updater.dispatcher.add_handler(CallbackQueryHandler(conversationHandler.get_folders, pattern="Add"))
    updater.dispatcher.add_handler(CallbackQueryHandler(conversationHandler.get_quality_profiles, pattern="Path"))
    updater.dispatcher.add_handler(CallbackQueryHandler(conversationHandler.add_to_library, pattern="Quality"))
    updater.dispatcher.add_handler(CallbackQueryHandler(conversationHandler.confirm_delete,
                                                        pattern="ConfirmDelete"))
    updater.dispatcher.add_handler(CallbackQueryHandler(conversationHandler.delete, pattern="Delete"))
    updater.dispatcher.add_handler(CallbackQueryHandler(stop_handler.stop, pattern="Stop"))
    # updater.dispatcher.add_handler(CallbackQueryHandler(handlers.add, pattern="Add_This"))
    updater.dispatcher.add_handler(CommandHandler('help', helpHandler.help))
    updater.dispatcher.add_handler(CommandHandler('auth', authenticationHandler.authenticate))

    # Start bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    initialise()
    main()
