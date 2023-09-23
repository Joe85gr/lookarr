from telegram import Update, InlineKeyboardMarkup, constants
from telegram.ext import CallbackContext
from telegram.error import BadRequest


class MessagesHandler:
    @staticmethod
    async def send_photo(
            context: CallbackContext,
            update: Update,
            caption: str,
            keyboard: list,
            photo: str,
            default_photo: str
    ):
        markup = InlineKeyboardMarkup(keyboard)

        try:
            msg = await context.bot.sendPhoto(
                chat_id=update.effective_message.chat_id,
                photo=photo,
                caption=caption,
                parse_mode=constants.ParseMode.HTML,
                reply_markup=markup
            )
        except BadRequest:
            msg = await context.bot.sendPhoto(
                chat_id=update.effective_message.chat_id,
                photo=default_photo,
                caption=caption,
                parse_mode=constants.ParseMode.HTML,
                reply_markup=markup
            )

        context.user_data["update_msg"] = msg.message_id

    @staticmethod
    async def new_message(
            update: Update,
            context: CallbackContext,
            reply: str,
            keyboard: list = None
    ):
        if keyboard is None:
            keyboard = []

        reply_markup = InlineKeyboardMarkup(keyboard)

        msg = await update.message.reply_text(reply, reply_markup=reply_markup)
        context.user_data["update_msg"] = msg.message_id

    @staticmethod
    async def update_query_or_send_new(
            update: Update,
            context: CallbackContext,
            reply: str
    ):
        query = update.callback_query
        if query:
            await query.edit_message_text(text=reply)
        else:
            await MessagesHandler.new_message(update, context, reply)

    @staticmethod
    async def delete_current(update: Update, context: CallbackContext):
        if "update_msg" in context.user_data:
            try:
                await context.bot.delete_message(chat_id=update.effective_message.chat_id,
                                                 message_id=context.user_data["update_msg"])
            except BadRequest:
                pass

    @staticmethod
    async def delete_current_and_add_new(
            context: CallbackContext,
            update: Update,
            reply: str = None,
            keyboard: list = None
    ):
        try:
            await MessagesHandler.delete_current(update, context)
        except BadRequest:
            pass

        if reply:
            if keyboard is None:
                keyboard = []

            reply_markup = InlineKeyboardMarkup(keyboard)
            msg = await context.bot.send_message(
                chat_id=update.effective_message.chat_id,
                text=reply,
                reply_markup=reply_markup,
            )
            context.user_data["update_msg"] = msg.message_id
