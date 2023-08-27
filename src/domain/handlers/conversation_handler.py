from telegram import Update
from dacite import from_dict
from telegram.ext import CallbackContext, ConversationHandler
from kink import inject

from src.domain.checkers.authentication_checker import check_user_is_authenticated
from src.domain.checkers.conversation_checker import check_conversation, answer_query
from src.domain.checkers.search_checker import check_search_is_valid
from src.domain.config.app_config import ConfigLoader, Config
from src.domain.handlers.messages_handler import MessagesHandler
from src.domain.handlers.stop_handler import stop_handler
from src.infrastructure.folder import Folder
from src.infrastructure.imedia_server_factory import IMediaServerFactory
from src.infrastructure.quality_profiles import QualityProfile
from src.interface.keyboard import Keyboard
from src.logger import ILogger


@inject
class SearchHandler:
    def __init__(
            self,
            media_server_factory: IMediaServerFactory,
            logger: ILogger,
            config: Config,
    ):
        self._logger = logger
        self._config = config
        self._media_server_factory = media_server_factory

    @check_user_is_authenticated
    @check_search_is_valid()
    def search(self, update: Update, context: CallbackContext):
        keyboard = Keyboard.search()

        MessagesHandler.new_message(update, "What you're looking for? 🧐:", keyboard)

    @check_user_is_authenticated
    @check_conversation(["update_msg"])
    def change_option(self, update: Update, context: CallbackContext):
        query = update.callback_query

        match query.data:
            case "Next":
                context.user_data["position"] += 1
            case "Previous":
                context.user_data["position"] -= 1

        self.show_medias(update, context)

    @check_user_is_authenticated
    @check_conversation(["update_msg", "type"])
    def get_folders(self, update: Update, context: CallbackContext):
        media_server = self._media_server_factory.get_media_server(context.user_data["type"])
        folders = media_server.media_server.get_root_folders()

        if not folders:
            MessagesHandler.update_message(
                context,
                update,
                "I couldn't retrieve the available folders 😔 not much I can do really.."
            )
            stop_handler.clear_user_data(update, context)
            return ConversationHandler.END

        results = [from_dict(data_class=Folder, data=folder) for folder in folders]

        keyboard = Keyboard.folders(results)

        MessagesHandler.update_message(context, update, "Select Download Path:", keyboard)

    @check_user_is_authenticated
    @check_conversation(["update_msg", "type"])
    def get_quality_profiles(self, update: Update, context: CallbackContext):
        query = update.callback_query

        media_server = self._media_server_factory.get_media_server(context.user_data["type"])

        if not context.user_data.get("path"):
            context.user_data["path"] = query.data.removeprefix("Path: ")

        qualityProfiles = media_server.media_server.get_quality_profiles()

        results = [from_dict(data_class=QualityProfile, data=entry) for entry in qualityProfiles]

        keyboard = Keyboard.quality_profiles(results)

        MessagesHandler.update_message(context, update, "Select Quality Profile:", keyboard)

    @check_user_is_authenticated
    @check_conversation(["update_msg", "type"])
    def add_to_library(self, update: Update, context: CallbackContext):
        query = update.callback_query

        media_server = self._media_server_factory.get_media_server(context.user_data["type"])

        if not context.user_data.get("quality_profile"):
            context.user_data["quality_profile"] = query.data.removeprefix("Quality: ")

        contentAdded = media_server.media_server.add_to_library(context.user_data['id'], context.user_data['path'],
                                                                context.user_data['quality_profile'])

        position = context.user_data["position"]
        title_added = context.user_data['results'][position]['title']

        if contentAdded:
            message = f"{title_added} added to your Library! 🥳"
        else:
            message = f"Unfortunately I was unable to add '{title_added}' to your library 😔"

        MessagesHandler.update_message(context, update, message)

        stop_handler.clear_user_data(update, context)
        return ConversationHandler.END

    @check_user_is_authenticated
    @check_conversation(["update_msg", "type"])
    def confirm_delete(self, update: Update, context: CallbackContext):
        position = context.user_data["position"]
        title_to_remove = context.user_data['results'][position]['title']
        message = f"You sure you want to remove {title_to_remove} from your Library? 😱"

        keyboard = Keyboard.delete()

        MessagesHandler.update_message(context, update, message, keyboard)

    @check_user_is_authenticated
    @check_conversation(["update_msg", "type"])
    def delete(self, update: Update, context: CallbackContext):
        media_server = self._media_server_factory.get_media_server(context.user_data["type"])

        position = context.user_data["position"]
        id_to_remove = context.user_data['results'][position]['id']
        title_to_remove = context.user_data['results'][position]['title']

        contentRemoved = media_server.media_server.remove_from_library(id_to_remove)

        if contentRemoved:
            message = f"{title_to_remove} has been removed from your Library! 😤"
        else:
            message = f"Unfortunately I was unable to remove '{title_to_remove}' to your library 😔 try again.."

        MessagesHandler.update_message(context, update, message)

        stop_handler.clear_user_data(update, context, False)
        return ConversationHandler.END

    @check_user_is_authenticated
    @answer_query()
    def search_media(self, update: Update, context: CallbackContext) -> None | int:
        query = update.callback_query

        context.user_data["type"] = update.callback_query.data

        if stop_handler.lost_track_of_conversation(update, context, ["type", "reply"]):
            return ConversationHandler.END

        media_server = self._media_server_factory.get_media_server(context.user_data["type"])

        query.edit_message_text(text=f"Looking for '{context.user_data['reply']}'..👀")

        results = media_server.media_server.search(context.user_data["reply"])

        if not results:
            query.edit_message_text(text=f"Sorry, I couldn't fine any result for '{context.user_data['reply']}' 😔")
            stop_handler.clear_user_data(update, context, False)
            return ConversationHandler.END

        context.user_data["position"] = 0
        context.user_data["results"] = results

        query.delete_message()

        self.show_medias(update, context)

    @check_user_is_authenticated
    def show_medias(self, update: Update, context: CallbackContext):
        position = context.user_data["position"]

        if "update_msg" in context.user_data:
            MessagesHandler.update_message(context, update, ".. 👀")

        media_server = self._media_server_factory.get_media_server(context.user_data["type"])

        results = [from_dict(data_class=media_server.data_type, data=entry) for entry in context.user_data['results']]

        current = results[position]
        context.user_data["id"] = current.id

        keyboard = Keyboard.medias(current.is_in_library, current.hasFile, len(results), position)

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
            MessagesHandler.update_message(context, update)

        MessagesHandler.send_photo(context, update, message, keyboard, current.remotePoster, current.defaultPoster)
