from datetime import datetime
from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Update,
    ChatMember,
    Chat,
    Bot,
    message
)
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler
)
from ..functions import pass_model_to
import html, os

GET_LANG = range(1)

def lang_command_handler(update: Update, context: CallbackContext, model):
    user = model.User.get_or_none(model.User.id == update.message.from_user.id)
    chat = model.Chat.get_or_none(model.Chat.id == update.message.chat.id)
    if chat:
        lang = chat.lang
    else:
        lang = model.lang.DEFAULT
        chat = model.Chat.create(
            id = update.message.chat.id,
            lang = lang
        )
        chat.save()
    if not user:
        user = model.User.create(
            id = update.message.from_user.id,
            lang = lang
        )
        user.save()
    if update.message.chat.type in ("group", "supergroup", "channel"):
        if context.bot.get_chat_member(
            chat_id = update.message.chat.id, 
            user_id = update.message.from_user.id).status in (ChatMember.ADMINISTRATOR, ChatMember.CREATOR):
            context.user_data["selected_models"] = (chat,)
            update.message.reply_text(
                model.lang.data[lang]["LANG_TEXT"].format(lang = lang),
                reply_markup=model.languages_keyboard
            )
            return GET_LANG
        else:
            update.message.delete()
            return ConversationHandler.END
    elif update.message.chat.type == "private":
        context.user_data["selected_models"] = (user, chat)
        update.message.reply_text(
            model.lang.data[lang]["LANG_TEXT"].format(lang = lang),
            reply_markup=model.languages_keyboard
        )
        return GET_LANG
    else: # WTF :|
        update.message.reply_text("unknown chat type!")
        return ConversationHandler.END

def get_lang_handler(update: Update, context: CallbackContext, model):
    query = update.callback_query
    if query.data not in model.lang.data:
        query.answer("invalid option!")
        return GET_LANG
    if query.message.chat.type in ("group", "supergroup", "channel"):
        if context.bot.get_chat_member(
            chat_id = update.message.chat.id, 
            user_id = update.message.from_user.id).status in (ChatMember.ADMINISTRATOR, ChatMember.CREATOR):
            for selected_model in context.user_data["selected_models"]:
                selected_model.lang = query.data
                selected_model.save()
        else:
            # It makes us sure; but ...
            # does it make sense? and why?
            # (2 point) - good luck!
            query.answer(">O<___>O<")
            return ConversationHandler.END
    elif query.message.chat.type == "private":
        for selected_model in context.user_data["selected_models"]:
            selected_model.lang = query.data
            selected_model.save()
    query.answer(model.lang.data[context.user_data["selected_models"][0].lang]["LANG_QUERY_OK"])
    return GET_LANG

def creator(model):
    handler = ConversationHandler(
        entry_points=[
            CommandHandler(
                ["lang", "language"],
                pass_model_to(lang_command_handler, model)
                )
        ],
        states={
            GET_LANG: [
                CallbackQueryHandler(
                    pass_model_to(get_lang_handler, model),
                    pattern=model.lang.data.__contains__
                )
            ]
        },
        fallbacks=[],
        allow_reentry=True
    )
    return handler
