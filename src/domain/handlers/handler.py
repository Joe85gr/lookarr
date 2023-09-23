from telegram import Update
from dacite import from_dict
from telegram.ext import CallbackContext, ConversationHandler, ContextTypes
from kink import inject

from src.constants import SEARCH_STARTED, MEDIA_TYPE_SELECTED, DELETE, QUALITY_SELECTED
from src.domain.checkers.authentication_checker import check_user_is_authenticated
from src.domain.checkers.conversation_checker import check_conversation
from src.domain.checkers.idefaults_checker import IDefaultValuesChecker
from src.domain.checkers.search_checker import check_search_is_valid
from src.domain.config.app_config import Config
from src.domain.handlers.interfaces.ihandler import IHandler
from src.domain.handlers.messages_handler import MessagesHandler
from src.domain.handlers.stop_handler import stop_handler
from src.infrastructure.folder import Folder
from src.infrastructure.interfaces.imedia_server_factory import IMediaServerFactory
from src.infrastructure.quality_profiles import QualityProfile
from src.interface.keyboard import Keyboard
from src.logger import ILogger


@inject
class Handler(IHandler):
    def __init__(
            self,
            media_server_factory: IMediaServerFactory,
            logger: ILogger,
            config: Config,
            defaults: IDefaultValuesChecker,
    ):
        self._logger = logger
        self._config = config
        self._media_server_factory = media_server_factory
        self._defaults = defaults

    @check_user_is_authenticated
    @check_search_is_valid()
    async def start_search(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        if self._config.active_media_servers == 0:
            await MessagesHandler.new_message(update, context, "Bro, all media servers are disabled in the config.. 🙄")
            return ConversationHandler.END
        elif self._config.active_media_servers == 1:
            context.user_data["type"] = self._config.default_media_server
            await self.search_media(update, context)
        else:
            keyboard = Keyboard.search()
            await MessagesHandler.new_message(update, context, "What you're looking for? 🧐:", keyboard)

        return SEARCH_STARTED

    @check_user_is_authenticated
    @check_conversation(["reply"])
    async def search_media(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await MessagesHandler.update_query_or_send_new(
            update,
            context,
            f"Looking for '{context.user_data['reply']}'..👀")

        context.user_data["type"] = update.callback_query.data

        media_server = self._media_server_factory.get_media_server(context.user_data["type"])

        results = media_server.media_server.search(context.user_data["reply"])

        if not results:
            await MessagesHandler.update_query_or_send_new(update, context, f"Sorry, I couldn't fine any result for "
                                                                            f"'{context.user_data['reply']}' 😔")
            stop_handler.clear_user_data(update, context, False)
            return ConversationHandler.END

        context.user_data["position"] = 0
        context.user_data["results"] = results

        return await self.show_medias(update, context)

    @check_user_is_authenticated
    @check_conversation(["update_msg"])
    async def change_option(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query

        match query.data:
            case "Next":
                context.user_data["position"] += 1
            case "Previous":
                context.user_data["position"] -= 1

        return await self.show_medias(update, context)

    async def get_folders(self, update: Update, context: CallbackContext, default_folder_action):
        await MessagesHandler.delete_current_and_add_new(context, update, ".. 👀")

        media_server = self._media_server_factory.get_media_server(context.user_data["type"])
        valid_values = media_server.media_server.get_root_folders()
        default_is_valid = self._defaults.is_valid(profile_name="path",
                                                   profile_name_identifier="path",
                                                   profile_key_identifier="path",
                                                   valid_values=valid_values,
                                                   media_server=media_server,
                                                   context=context
                                                   )

        if default_is_valid:
            context.user_data["path"] = media_server.media_server.defaults["path"]
            return await default_folder_action(update, context)

        folders = media_server.media_server.get_root_folders()

        results = [from_dict(data_class=Folder, data=folder) for folder in folders]

        keyboard = Keyboard.folders(results, context.user_data["type"])
        await MessagesHandler.delete_current_and_add_new(context, update, "Select Path:", keyboard)

    async def get_quality_profiles(self, update: Update, context: CallbackContext, default_profile_action):
        media_server = self._media_server_factory.get_media_server(context.user_data["type"])

        query = update.callback_query

        if not "path" in context.user_data:
            context.user_data["path"] = query.data.removeprefix(f"{context.user_data['type']}GetQualityProfiles: ")

        valid_values = media_server.media_server.get_quality_profiles()
        has_default = self._defaults.is_valid("quality_profile", "name", "id", valid_values, media_server, context)

        if has_default:
            return await default_profile_action(update, context)

        qualityProfiles = media_server.media_server.get_quality_profiles()

        results = [from_dict(data_class=QualityProfile, data=entry) for entry in qualityProfiles]

        keyboard = Keyboard.quality_profiles(results, context.user_data["type"])

        await MessagesHandler.delete_current_and_add_new(context, update, "Select Quality Profile:", keyboard)

        return QUALITY_SELECTED

    @check_user_is_authenticated
    @check_conversation(["update_msg", "type"])
    async def add_to_library(self, update: Update, context: CallbackContext):
        await MessagesHandler.delete_current_and_add_new(context, update, ".. 👀")

        media_server = self._media_server_factory.get_media_server(context.user_data["type"])

        content_added = media_server.media_server.add_to_library(context.user_data)

        position = context.user_data["position"]
        title_added = context.user_data['results'][position]['title']

        if content_added:
            message = f"{title_added} added to your Library! 🥳"
        else:
            message = f"Unfortunately I was unable to add '{title_added}' to your library 😔"

        await MessagesHandler.delete_current_and_add_new(context, update, message)

        stop_handler.clear_user_data(update, context)
        return ConversationHandler.END

    @check_user_is_authenticated
    @check_conversation(["update_msg", "type"])
    async def confirm_delete(self, update: Update, context: CallbackContext):
        await MessagesHandler.delete_current_and_add_new(context, update, ".. 👀")

        position = context.user_data["position"]
        title_to_remove = context.user_data['results'][position]['title']
        message = f"You sure you want to remove {title_to_remove} from your Library? 😱"

        keyboard = Keyboard.delete()

        await MessagesHandler.delete_current_and_add_new(context, update, message, keyboard)

        return DELETE

    @check_user_is_authenticated
    @check_conversation(["update_msg", "type"])
    async def delete(self, update: Update, context: CallbackContext):
        await MessagesHandler.delete_current_and_add_new(context, update, ".. 👀")

        media_server = self._media_server_factory.get_media_server(context.user_data["type"])

        position = context.user_data["position"]
        id_to_remove = context.user_data['results'][position]['id']
        title_to_remove = context.user_data['results'][position]['title']

        contentRemoved = media_server.media_server.remove_from_library(id_to_remove)

        if contentRemoved:
            message = f"{title_to_remove} has been removed from your Library! 😤"
        else:
            message = f"Unfortunately I was unable to remove '{title_to_remove}' to your library 😔 try again.."

        await MessagesHandler.delete_current_and_add_new(context, update, message)

        stop_handler.clear_user_data(update, context, False)
        return ConversationHandler.END

    @check_user_is_authenticated
    async def show_medias(self, update: Update, context: CallbackContext):
        position = context.user_data["position"]

        media_server = self._media_server_factory.get_media_server(context.user_data["type"])

        results = [from_dict(data_class=media_server.media_server.media_type, data=entry)
                   for entry in context.user_data['results']]

        current = results[position]
        context.user_data["id"] = current.id

        keyboard = Keyboard.medias(
            current.is_in_library,
            current.hasFile,
            len(results),
            position,
            context.user_data["type"]
        )

        message = f"\n\n<b>{current.title} ({current.year})</b>"

        if current.is_in_library:
            message += f"\n\n\U00002705 Already in library! 😄"
            if current.hasFile:
                message += f" Ready to watch! 🥳"
            elif current.hasFile is not None:
                message += f"\n\n⚠️ It looks like you still can't watch it though.. 🙄"

        if current.overview:
            message += f"\n\n{current.overview}"

        message = self._ensure_is_within_char_limit(message)
        await MessagesHandler.delete_current(update, context)

        await MessagesHandler.send_photo(
            context,
            update,
            message,
            keyboard,
            current.remotePoster,
            current.defaultPoster)

        return MEDIA_TYPE_SELECTED

    @staticmethod
    def _ensure_is_within_char_limit(message: str):
        if len(message) >= 900:
            message = message[:900].rsplit(' ', 1)[0] + "[...]"
        return message
