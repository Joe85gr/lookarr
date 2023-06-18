from dacite import from_dict
from telegram.error import BadRequest

from src.app.handlers.authentication import AuthHandler
from src.app.handlers.stop import StopHandler
from src.infrastructure.folder import Folder
from src.infrastructure.media_server_factory import IMediaServerFactory
from src.infrastructure.quality_profiles import QualityProfile
from src.logger import Log
from telegram import Update, InlineKeyboardMarkup, constants
from telegram.ext import CallbackContext, ConversationHandler
from src.app.interface.buttons import Buttons
from src.app.config.app_config import Config
from src.domain.user import UserReply


class SearchHandler:
    def __init__(
            self,
            auth_handler: AuthHandler,
            stop_handler: StopHandler,
            config: Config,
            media_server_factory: IMediaServerFactory
    ):
        self.logger = Log.get_logger(__name__)
        self.auth_handler = auth_handler
        self.stop_handler = stop_handler
        self.buttons = Buttons()
        self.config = config
        self.media_server_factory = media_server_factory

    def searchType(self, update: Update, context: CallbackContext) -> None | int:
        self.auth_handler.check_if_auth(update)

        user_reply = UserReply(update.message.text)

        if not user_reply.is_valid:
            update.message.reply_text(
                "Well, I'm unsure what you want me to search..🧐\nwrite /search <search criteria> "
                "to get some results.")
            self.stop_handler.clearUserData(update, context)
            return ConversationHandler.END

        context.user_data["reply"] = user_reply.value

        keyboard = [
            [self.buttons.series_button(), self.buttons.movie_button()],
            [self.buttons.stop_button()],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text("What you're looking for? 🧐:", reply_markup=reply_markup)

    def goToPreviousOrNextOption(self, update: Update, context: CallbackContext) -> None | int:
        query = update.callback_query
        query.answer()

        if not context.user_data.get("update_msg"):
            self.stop_handler.clearUserData(update, context)
            return ConversationHandler.END

        if query.data == "Next":
            context.user_data["position"] += 1
        elif query.data == "Previous":
            context.user_data["position"] -= 1

        self.showMedias(update, context)

    def getFolders(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()

        if not context.user_data.get("update_msg") or not context.user_data["type"]:
            self.stop_handler.clearUserData(update, context)
            return ConversationHandler.END

        system = self.media_server_factory.getMediaServer(context.user_data["type"])
        folders = system.media_server.getRootFolders()

        if not folders:
            context.bot.delete_message(chat_id=update.effective_message.chat_id,
                                       message_id=context.user_data["update_msg"])
            context.bot.send_message(chat_id=update.effective_message.chat_id,
                                     text=f"I couldn't retrieve the available '{context.user_data['type']}' "
                                          f"folders 😔 not much I can do really..")
            self.stop_handler.clearUserData(update, context)
            return ConversationHandler.END

        results = [from_dict(data_class=Folder, data=folder) for folder in folders]

        keyboard = []

        for folder in results:
            keyboard.append([self.buttons.path_button(folder)])

        keyboard.append([self.buttons.stop_button()])

        reply_markup = InlineKeyboardMarkup(keyboard)

        query.delete_message()

        msg = context.bot.sendMessage(
            chat_id=update.effective_message.chat_id,
            text="Select Download Path:",
            reply_markup=reply_markup,
        )

        context.user_data["update_msg"] = msg.message_id

    def getQualityProfiles(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()

        if not context.user_data.get("update_msg") or not context.user_data["type"]:
            self.stop_handler.clearUserData(update, context)
            return ConversationHandler.END

        system = self.media_server_factory.getMediaServer(context.user_data["type"])

        if not context.user_data.get("path"):
            context.user_data["path"] = query.data.removeprefix("Path: ")

        qualityProfiles = system.media_server.getQualityProfiles()

        results = [from_dict(data_class=QualityProfile, data=entry) for entry in qualityProfiles]

        keyboard = []

        for profile in results:
            keyboard.append([self.buttons.quality_profile_button(profile)])

        keyboard.append([self.buttons.stop_button()])

        reply_markup = InlineKeyboardMarkup(keyboard)

        context.bot.delete_message(chat_id=update.effective_message.chat_id,
                                   message_id=context.user_data["update_msg"])

        msg = context.bot.sendMessage(
            chat_id=update.effective_message.chat_id,
            text="Select Quality Profile:",
            reply_markup=reply_markup,
        )

        context.user_data["update_msg"] = msg.message_id

    def addToLibrary(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()

        if not context.user_data.get("update_msg") or not context.user_data["type"]:
            self.stop_handler.clearUserData(update, context)
            return ConversationHandler.END

        system = self.media_server_factory.getMediaServer(context.user_data["type"])

        if not context.user_data.get("quality_profile"):
            context.user_data["quality_profile"] = query.data.removeprefix("Quality: ")

        contentAdded = system.media_server.addToLibrary(context.user_data['id'], context.user_data['path'],
                                                        context.user_data['quality_profile'])

        position = context.user_data["position"]
        title_added = context.user_data['results'][position]['title']

        if contentAdded:
            message = f"{title_added} added to your Library! 🥳"
        else:
            message = f"Unfortunately I was unable to add '{title_added}' to your library 😔"

        context.bot.delete_message(chat_id=update.effective_message.chat_id,
                                   message_id=context.user_data["update_msg"])

        context.bot.send_message(chat_id=update.effective_message.chat_id, text=message)

    def searchMedia(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()

        context.user_data["type"] = query.data

        system = self.media_server_factory.getMediaServer(context.user_data["type"])

        query.edit_message_text(text=f"Looking for '{context.user_data['reply']}'..👀")

        results = system.media_server.search(context.user_data["reply"])

        context.user_data["position"] = 0
        context.user_data["results"] = results

        query.delete_message()

        self.showMedias(update, context)

    def showMedias(self, update: Update, context: CallbackContext):
        position = context.user_data["position"]
        system = self.media_server_factory.getMediaServer(context.user_data["type"])

        results = [from_dict(data_class=system.data_type, data=entry) for entry in context.user_data['results']]

        current = results[position]
        context.user_data["id"] = current.id

        if not current.is_in_library:
            keyboard = [[self.buttons.add_button()]]
        else:
            keyboard = [[self.buttons.delete_button()]]

        if len(results) > 1 and len(results) > position == 0:  # show next
            keyboard.append([self.buttons.next_button()])
        elif len(results) - 1 == position:  # show previous
            keyboard.append([self.buttons.previous_button()])
        else:
            keyboard.append([self.buttons.previous_button(), self.buttons.next_button()])

        keyboard.append([self.buttons.stop_button()])
        markup = InlineKeyboardMarkup(keyboard)
        message = f"\n\n<b>{current.title} ({current.year})</b>"

        if current.is_in_library:
            message += f"\n\n\U00002705 Already in library! 😄"
            if current.hasFile:
                message += f" Ready to watch! 🥳"
            else:
                message += f"\n\n⚠️ It looks like it's still downloading 🙄"

        if current.overview:
            message += f"\n\n{current.overview}"

        if len(message) >= 900:
            message = message[:900].rsplit(' ', 1)[0] + "[...]"

        if "update_msg" in context.user_data:
            context.bot.delete_message(chat_id=update.effective_message.chat_id,
                                       message_id=context.user_data["update_msg"])

        try:
            msg = context.bot.sendPhoto(
                chat_id=update.effective_message.chat_id,
                photo=current.remotePoster,
                caption=message,
                parse_mode=constants.PARSEMODE_HTML,
                reply_markup=markup
            )
        except BadRequest:
            msg = context.bot.sendPhoto(
                chat_id=update.effective_message.chat_id,
                photo=current.defaultPoster,
                caption=message,
                parse_mode=constants.PARSEMODE_HTML,
                reply_markup=markup
            )

        context.user_data["update_msg"] = msg.message_id
