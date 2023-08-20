from dacite import from_dict
from telegram.error import BadRequest

from src.domain.checkers.authentication_checker import check_user_is_authenticated
from src.domain.checkers.conversation_checker import check_conversation
from src.domain.checkers.search_checker import check_search_is_valid
from src.domain.handlers.stop_handler import stop_handler
from src.infrastructure.folder import Folder
from src.infrastructure.media_server_factory import IMediaServerFactory
from src.infrastructure.quality_profiles import QualityProfile
from src.logger import Log
from telegram import Update, InlineKeyboardMarkup, constants
from telegram.ext import CallbackContext, ConversationHandler
from src.interface.buttons import Buttons


class SearchHandler:
    def __init__(
            self,
            media_server_factory: IMediaServerFactory
    ):
        self._logger = Log.get_logger(__name__)
        self._buttons = Buttons()
        self._media_server_factory = media_server_factory

    @check_search_is_valid()
    @check_user_is_authenticated()
    def search(self, update: Update, context: CallbackContext):
        keyboard = [
            [self._buttons.series_button(), self._buttons.movie_button()],
            [self._buttons.stop_button()],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text("What you're looking for? 🧐:", reply_markup=reply_markup)

    @check_conversation(["update_msg"])
    @check_user_is_authenticated()
    def goToPreviousOrNextOption(self, update: Update, context: CallbackContext):
        query = update.callback_query

        match query.data:
            case "Next":
                context.user_data["position"] += 1
            case "Previous":
                context.user_data["position"] -= 1

        self.showMedias(update, context)

    @check_conversation(["update_msg", "type"])
    @check_user_is_authenticated()
    def getFolders(self, update: Update, context: CallbackContext):
        query = update.callback_query

        media_server = self._media_server_factory.getMediaServer(context.user_data["type"])
        folders = media_server.media_server.getRootFolders()

        if not folders:
            context.bot.delete_message(chat_id=update.effective_message.chat_id,
                                       message_id=context.user_data["update_msg"])
            context.bot.send_message(chat_id=update.effective_message.chat_id,
                                     text=f"I couldn't retrieve the available '{context.user_data['type']}' "
                                          f"folders 😔 not much I can do really..")
            stop_handler.clearUserData(update, context)
            return ConversationHandler.END

        results = [from_dict(data_class=Folder, data=folder) for folder in folders]

        keyboard = []

        for folder in results:
            keyboard.append([self._buttons.path_button(folder)])

        keyboard.append([self._buttons.stop_button()])

        reply_markup = InlineKeyboardMarkup(keyboard)

        query.delete_message()

        msg = context.bot.sendMessage(
            chat_id=update.effective_message.chat_id,
            text="Select Download Path:",
            reply_markup=reply_markup,
        )

        context.user_data["update_msg"] = msg.message_id

    @check_conversation(["update_msg", "type"])
    @check_user_is_authenticated()
    def getQualityProfiles(self, update: Update, context: CallbackContext):
        query = update.callback_query

        media_server = self._media_server_factory.getMediaServer(context.user_data["type"])

        if not context.user_data.get("path"):
            context.user_data["path"] = query.data.removeprefix("Path: ")

        qualityProfiles = media_server.media_server.getQualityProfiles()

        results = [from_dict(data_class=QualityProfile, data=entry) for entry in qualityProfiles]

        keyboard = []

        for profile in results:
            keyboard.append([self._buttons.quality_profile_button(profile)])

        keyboard.append([self._buttons.stop_button()])

        reply_markup = InlineKeyboardMarkup(keyboard)

        context.bot.delete_message(chat_id=update.effective_message.chat_id,
                                   message_id=context.user_data["update_msg"])

        msg = context.bot.sendMessage(
            chat_id=update.effective_message.chat_id,
            text="Select Quality Profile:",
            reply_markup=reply_markup,
        )

        context.user_data["update_msg"] = msg.message_id

    @check_conversation(["update_msg", "type"])
    @check_user_is_authenticated()
    def addToLibrary(self, update: Update, context: CallbackContext):
        query = update.callback_query

        media_server = self._media_server_factory.getMediaServer(context.user_data["type"])

        if not context.user_data.get("quality_profile"):
            context.user_data["quality_profile"] = query.data.removeprefix("Quality: ")

        contentAdded = media_server.media_server.addToLibrary(context.user_data['id'], context.user_data['path'],
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

        stop_handler.clearUserData(update, context)
        return ConversationHandler.END

    @check_conversation(["update_msg", "type"])
    @check_user_is_authenticated()
    def confirmDelete(self, update: Update, context: CallbackContext):
        position = context.user_data["position"]
        title_to_remove = context.user_data['results'][position]['title']
        message = f"You sure you want to remove {title_to_remove} from your Library? 😱"

        keyboard = [
            [self._buttons.yes_button()],
            [self._buttons.no_button()]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        context.bot.delete_message(chat_id=update.effective_message.chat_id,
                                   message_id=context.user_data["update_msg"])

        msg = context.bot.sendMessage(
            chat_id=update.effective_message.chat_id,
            text=message,
            reply_markup=reply_markup,
        )

        context.user_data["update_msg"] = msg.message_id

    @check_conversation(["update_msg", "type"])
    @check_user_is_authenticated()
    def delete(self, update: Update, context: CallbackContext):
        media_server = self._media_server_factory.getMediaServer(context.user_data["type"])

        position = context.user_data["position"]
        id_to_remove = context.user_data['results'][position]['id']
        title_to_remove = context.user_data['results'][position]['title']

        contentRemoved = media_server.media_server.removeFromLibrary(id_to_remove)

        if contentRemoved:
            message = f"{title_to_remove} has been removed from your Library! 😤"
        else:
            message = f"Unfortunately I was unable to remove '{title_to_remove}' to your library 😔 try again.."

        context.bot.delete_message(chat_id=update.effective_message.chat_id,
                                   message_id=context.user_data["update_msg"])

        context.bot.send_message(chat_id=update.effective_message.chat_id, text=message)

        stop_handler.clearUserData(update, context, False)
        return ConversationHandler.END

    @check_user_is_authenticated()
    def searchMedia(self, update: Update, context: CallbackContext) -> None | int:
        query = update.callback_query
        query.answer()

        context.user_data["type"] = query.data

        if stop_handler.lostTrackOfConversation(update, context, ["type", "reply"]):
            return ConversationHandler.END

        media_server = self._media_server_factory.getMediaServer(context.user_data["type"])

        query.edit_message_text(text=f"Looking for '{context.user_data['reply']}'..👀")

        results = media_server.media_server.search(context.user_data["reply"])

        if not results:
            query.edit_message_text(text=f"Sorry, I couldn't fine any result for '{context.user_data['reply']}' 😔")
            stop_handler.clearUserData(update, context, False)
            return ConversationHandler.END

        context.user_data["position"] = 0
        context.user_data["results"] = results

        query.delete_message()

        self.showMedias(update, context)

    @check_user_is_authenticated()
    def showMedias(self, update: Update, context: CallbackContext):
        position = context.user_data["position"]

        if "update_msg" in context.user_data:
            context.bot.delete_message(chat_id=update.effective_message.chat_id,
                                       message_id=context.user_data["update_msg"])

            mgs = context.bot.send_message(chat_id=update.effective_message.chat_id, text=".. 👀")
            context.user_data["update_msg"] = mgs.message_id

        media_server = self._media_server_factory.getMediaServer(context.user_data["type"])

        results = [from_dict(data_class=media_server.data_type, data=entry) for entry in context.user_data['results']]

        current = results[position]
        context.user_data["id"] = current.id

        if not current.is_in_library:
            keyboard = [[self._buttons.add_button()]]
        elif current.hasFile:
            keyboard = [[self._buttons.delete_button()]]
        else:
            keyboard = [[self._buttons.delete_button("Cancel Download")]]

        if len(results) > 1 and len(results) > position == 0:  # show next
            keyboard.append([self._buttons.next_button()])
        elif len(results) - 1 == position:  # show previous
            keyboard.append([self._buttons.previous_button()])
        else:
            keyboard.append([self._buttons.previous_button(), self._buttons.next_button()])

        keyboard.append([self._buttons.stop_button()])
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
