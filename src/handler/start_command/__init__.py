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
from ..functions import pass_model_to, generate_random_code, codehub
import html, os
from ..add_paste import (
    get_source_code_state_handler,
    get_lang_back_handler,
    get_lang_handler,
    skip_get_title_state_handler,
    get_title_state_handler,
    skip_get_description_state_handler,
    get_description_state_handler,
)

GET_SOURCE_CODE, GET_LANG, GET_TITLE, GET_DESCRIPTION, CONFIRM = range(5)

def start_command_handler(update: Update, context: CallbackContext, model):
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
        # I don't have any idea for this part; sorry :/
        update.message.delete()
        return ConversationHandler.END
    elif update.message.chat.type == "private":
        if context.args:
            context.user_data["lang"] = lang
            context.user_data["user"] = user
            context.user_data["chat"] = chat
            context.user_data["status_code"] = context.args[0]
            update.message.reply_text(model.lang.data[user.lang]["PASTE_PRIVATE_ENTRY"])
            return GET_SOURCE_CODE
        else:
            update.message.reply_text(
                model.lang.data[user.lang]["START_TEXT"].format(username = context.bot.username)
            )
            return ConversationHandler.END
    else: # WTF :/
        update.message.reply_text("unknown chat type!")
        return ConversationHandler.END

def confirm_state_handler(update: Update, context: CallbackContext, model):
    lang = context.user_data["lang"]
    query = update.callback_query
    if query.data == "+":
        res = codehub.snippet_create(
            title = context.user_data["title"],
            description = context.user_data["description"],
            lang = context.user_data["prg_lang"],
            body = context.user_data["source_code"]
        )
        paste = model.Paste.create(
            title = res["title"],
            description = res["description"],
            lang = res["lang"],
            created_on = datetime.strptime(
                res["created_on"],
                "%Y-%m-%dT%H:%M:%S.%f%z" # damn pattern :/
            ),
            user = context.user_data["user"],
            chat = context.user_data["chat"]
        )
        paste.save()
        query.message.edit_text(
            model.lang.data[lang]["PASTE_CONFIRM_RESULT"].format(
                title = res["title"],
                description = res["description"],
                lang = res["lang"],
                time = res["created_on"],
                url = f"https://codehub.pythonanywhere.com/snippet/{res['id']}"
            ),
            reply_markup=InlineKeyboardMarkup([])
        )
        model.afoot_pastes[context.user_data["status_code"]]["message"].edit_text(
            model.lang.data[lang]["START_CONFIRM_RESULT_FOR_CHAT"].format(
                title = res["title"],
                description = res["description"],
                lang = res["lang"],
                time = res["created_on"],
                url = f"https://codehub.pythonanywhere.com/snippet/{res['id']}"
            ),
            reply_markup=InlineKeyboardMarkup([])
        )
        del model.afoot_pastes[context.user_data["status_code"]]
    else:
        query.message.edit_text(
            model.lang.data[lang]["PASTE_CONFIRM_CANCELED"],
            reply_markup=InlineKeyboardMarkup([])
        )
    return ConversationHandler.END

def creator(model):
    handler = ConversationHandler(
        entry_points=[
            CommandHandler(
                "start",
                pass_model_to(start_command_handler, model)
                )
        ],
        states={
            GET_SOURCE_CODE: [
                MessageHandler(
                    Filters.text | Filters.document,
                    pass_model_to(get_source_code_state_handler, model)
                    )
            ],
            GET_LANG: [
                CallbackQueryHandler(
                    pass_model_to(get_lang_handler, model),
                    pattern=(
                        'arduino', 'bash', 'c', 'cpp', 'csharp', 'css', 'dart',
                        'docker', 'docker-compose', 'go', 'html', 'java', 
                        'js', 'json', 'lua', 'md', 'mysql', 'php', 'python', 'rb'
                    ).__contains__
                ),
                CommandHandler(
                    "back",
                    pass_model_to(get_lang_back_handler, model)
                    )
            ],
            GET_TITLE: [
                CommandHandler(
                    "skip",
                    pass_model_to(skip_get_title_state_handler, model)
                    ),
                MessageHandler(
                    Filters.text,
                    pass_model_to(get_title_state_handler, model)
                    )
            ],
            GET_DESCRIPTION: [
                CommandHandler(
                    "skip",
                    pass_model_to(skip_get_description_state_handler, model)
                    ),
                MessageHandler(
                    Filters.text,
                    pass_model_to(get_description_state_handler, model)
                    )
            ],
            CONFIRM: [
                CallbackQueryHandler(
                    pass_model_to(confirm_state_handler, model),
                    pattern=("+","-").__contains__
                )
            ]
        },
        fallbacks=[]
    )
    return handler
