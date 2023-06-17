import dataclasses
import json

from dacite import from_dict
from telegram.error import BadRequest

from src.infrastructure.folder import Folder
from src.infrastructure.mediaServer import System
from src.infrastructure.movie import Movie
from src.infrastructure.quality_profiles import QualityProfile
from src.infrastructure.radarr import Radarr
from src.logger import Log
from telegram import Update, InlineKeyboardMarkup, constants
from telegram.ext import CallbackContext, ConversationHandler
from src.app.interface.buttons import Buttons
from src.app.config.all_config import Config

from src.domain.authentication import Auth
from src.domain.user import UserReply


class CommonHandlers:
    def __init__(
            self,
            auth: Auth,
            config: Config):
        self.logger = Log.get_logger("src.app.common_handlers.command_handlers.CommonHandlers")
        self.auth = auth
        self.buttons = Buttons()
        self.config = config
        self.radarr = Radarr(config.radarr)
        self.__systems = {
            "Movie": System(self.radarr, Movie)
        }

    def __get_system(self, key: str) -> System:
        return self.__systems[key]

    def search_type(self, update: Update, context: CallbackContext) -> None | int:
        self.check_if_auth(update)

        user_reply = UserReply(update.message.text)

        if not user_reply.is_valid:
            update.message.reply_text(
                "Well, I'm unsure what you want me to search..🧐\nwrite /search <search criteria> "
                "to get some results.")
            self.clear_user_data(update, context)
            return ConversationHandler.END

        context.user_data["reply"] = user_reply.value

        keyboard = [
            [self.buttons.series_button(), self.buttons.movie_button()],
            [self.buttons.stop_button()],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text("What you're looking for? 🧐:", reply_markup=reply_markup)

    def check_if_auth(self, update: Update) -> None | int:
        user = update.effective_user

        if not self.auth.user_is_authenticated_strict(user.id, self.config):
            self.logger.info(f"unauthorised user {user.id}")
            return ConversationHandler.END
        elif not self.auth.user_is_authenticated(user.id):
            update.message.reply_text(
                "Well, shit! 😄 seems you're not authenticated! Write /auth <password> to authenticate!")
            return ConversationHandler.END

    def auth(self, update: Update, context: CallbackContext) -> None | int:
        user = update.effective_user
        user_reply = UserReply(update.message.text)

        if not self.auth.user_is_authenticated_strict(user.id, self.config):
            self.logger.info(f"unauthorised user {user.id}. Won't reply :D")
            return ConversationHandler.END
        elif self.auth.user_is_authenticated(user.id):
            update.message.reply_text(
                text="What you want?? You're already authenticated! Do you like passwords or something 🤣")
        elif not user_reply.is_valid:
            update.message.reply_text(text=f"You need to write /auth <password> 😒 don't make me repeat myself..")
        elif not self.auth.authenticate_user(user.id, user_reply.value):
            update.message.reply_text(text=f"Sorry pal, wrong password 😝 try again.")
        else:
            update.message.reply_text(text=f"Nice one! You're in buddy 😌")

    def goToPreviousOrNextOption(self, update: Update, context: CallbackContext) -> None | int:
        query = update.callback_query
        query.answer()

        if not context.user_data.get("update_msg"):
            self.clear_user_data(update, context)
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
            self.clear_user_data(update, context)
            return ConversationHandler.END

        system = self.__get_system(context.user_data["type"])
        folders = system.mediaServer.getRootFolders()

        if not folders:
            context.bot.delete_message(chat_id=update.effective_message.chat_id,
                                       message_id=context.user_data["update_msg"])
            context.bot.send_message(chat_id=update.effective_message.chat_id,
                                     text=f"I couldn't retrieve the available '{context.user_data['type']}' "
                                          f"folders 😔 not much I can do really..")
            self.clear_user_data(update, context)
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
            self.clear_user_data(update, context)
            return ConversationHandler.END

        system = self.__get_system(context.user_data["type"])

        if not context.user_data.get("path"):
            context.user_data["path"] = query.data.removeprefix("Path: ")

        qualityProfiles = system.mediaServer.getQualityProfiles()

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

    def add(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()

        if not context.user_data.get("update_msg") or not context.user_data["type"]:
            self.clear_user_data(update, context)
            return ConversationHandler.END

        system = self.__get_system(context.user_data["type"])

        if not context.user_data.get("quality_profile"):
            context.user_data["quality_profile"] = query.data.removeprefix("Quality: ")

        contentAdded = system.mediaServer.addToLibrary(context.user_data['id'], context.user_data['path'],
                                                       context.user_data['quality_profile'])

        if contentAdded:
            message = f"{context.user_data['reply']} added to your Library! 🥳"
        else:
            message = f"Unfortunately I was unable to add '{context.user_data['reply']}' to your library 😔"

        context.bot.delete_message(chat_id=update.effective_message.chat_id,
                                   message_id=context.user_data["update_msg"])

        context.bot.send_message(chat_id=update.effective_message.chat_id, text=message)

    @staticmethod
    def help_command(update: Update, context: CallbackContext) -> None:
        update.message.reply_text("Use /start to tests this bot.")

    def stop(self, update, context):
        self.check_if_auth(update)

        self.clear_user_data(update, context)

        context.bot.send_message(chat_id=update.effective_message.chat_id, text="Ok, nothing to do for me then 🌝")

        return ConversationHandler.END

    def clear_user_data(self, update: Update, context: CallbackContext):
        msg = update.effective_message

        try:
            context.bot.delete_message(chat_id=update.effective_message.chat_id, message_id=msg.message_id)
        except Exception as e:
            self.logger.error(f"could not delete message id {msg.message_id}", e)

        items = [item for item in context.user_data]
        [context.user_data.pop(item) for item in items]

    def searchMedia(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()

        context.user_data["type"] = query.data

        system = self.__get_system(context.user_data["type"])

        query.edit_message_text(text=f"Looking for '{context.user_data['reply']}'..👀")

        results = system.mediaServer.search(context.user_data["reply"])

        context.user_data["position"] = 0
        context.user_data["results"] = results

        query.delete_message()

        self.showMedias(update, context)

    def showMedias(self, update: Update, context: CallbackContext):
        position = context.user_data["position"]
        system = self.__get_system(context.user_data["type"])

        results = [from_dict(data_class=system.dataType, data=entry) for entry in context.user_data['results']]

        context.user_data["id"] = results[position].id

        if not results[position].hasFile and results[position].added == '0001-01-01T00:01:00Z':
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
        message = f"\n\n<b>{results[position].title} ({results[position].year})</b>"

        if results[position].hasFile or not results[position].added == '0001-01-01T00:01:00Z':
            message += f"\n\n\U00002705 Already in library! 😄"

        if results[position].overview:
            message += f"\n\n{results[position].overview}"

        if len(message) >= 900:
            message = message[:900].rsplit(' ', 1)[0] + "[...]"

        if "update_msg" in context.user_data:
            context.bot.delete_message(chat_id=update.effective_message.chat_id,
                                       message_id=context.user_data["update_msg"])

        try:
            msg = context.bot.sendPhoto(
                chat_id=update.effective_message.chat_id,
                photo=results[position].remotePoster,
                caption=message,
                parse_mode=constants.PARSEMODE_HTML,
                reply_markup=markup
            )
        except BadRequest:
            msg = context.bot.sendPhoto(
                chat_id=update.effective_message.chat_id,
                photo=results[position].defaultPoster,
                caption=message,
                parse_mode=constants.PARSEMODE_MARKDOWN,
                reply_markup=markup
            )

        context.user_data["update_msg"] = msg.message_id
