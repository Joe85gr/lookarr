#!/usr/bin/env python

from os import environ

from kink import inject
from src.dependencies.di import initialise

from src.domain.handlers.interfaces.iauthentication_handler import IAuthHandler
from src.domain.handlers.interfaces.iconversation_handler import ISearchHandler

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from src.domain.config.app_config import Config
from src.domain.handlers.interfaces.ihelp_handler import IHelpHandler
from src.domain.handlers.interfaces.istop_handler import IStopHandler


@inject
def main(
        config: Config,
        authentication_handler: IAuthHandler,
        conversation_handler: ISearchHandler,
        stop_handler: IStopHandler,
        help_handler: IHelpHandler
) -> None:

    updater = Updater(environ.get("TELEGRAM_BOT_KEY"))

    updater.dispatcher.add_handler(CommandHandler(config.lookarr.search_all_command, conversation_handler.search))
    updater.dispatcher.add_handler(CallbackQueryHandler(conversation_handler.search_media, pattern="Movie"))
    updater.dispatcher.add_handler(CallbackQueryHandler(conversation_handler.change_option,
                                                        pattern="Next|Previous"))
    updater.dispatcher.add_handler(CallbackQueryHandler(conversation_handler.get_folders, pattern="Add"))
    updater.dispatcher.add_handler(CallbackQueryHandler(conversation_handler.get_quality_profiles, pattern="Path"))
    updater.dispatcher.add_handler(CallbackQueryHandler(conversation_handler.add_to_library, pattern="Quality"))
    updater.dispatcher.add_handler(CallbackQueryHandler(conversation_handler.confirm_delete,
                                                        pattern="ConfirmDelete"))
    updater.dispatcher.add_handler(CallbackQueryHandler(conversation_handler.delete, pattern="Delete"))
    updater.dispatcher.add_handler(CallbackQueryHandler(stop_handler.stop, pattern="Stop"))
    # updater.dispatcher.add_handler(CallbackQueryHandler(handlers.add, pattern="Add_This"))
    updater.dispatcher.add_handler(CommandHandler('help', help_handler.help))
    updater.dispatcher.add_handler(CommandHandler('auth', authentication_handler.authenticate))

    # Start bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    initialise()
    main()
