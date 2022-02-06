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

GET_SOURCE_CODE, GET_LANG, GET_TITLE, GET_DESCRIPTION, CONFIRM = range(5)

def paste_command_handler(update: Update, context: CallbackContext, model):
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
        update.message.delete()
        code = generate_random_code(not_in=model.afoot_pastes)
        if update.message.reply_to_message:
            model.afoot_pastes[code] = {
                "message": update.message.reply_to_message.reply_text(
                    model.lang.data[chat.lang]["PASTE_CHAT_ENTRY"],
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(
                            text=model.lang.data[chat.lang]["PASTE_CHAT_REDIRECT"],
                            url=f"https://t.me/{context.bot.username}?start={code}"
                        )
                    ]])
                )
            }
        else:
            model.afoot_pastes[code] = {
                "message": context.bot.send_message(
                    chat_id = update.message.chat.id,
                    text = model.lang.data[chat.lang]["PASTE_CHAT_ENTRY"],
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton(
                            text=model.lang.data[chat.lang]["PASTE_CHAT_REDIRECT"],
                            url=f"https://t.me/{context.bot.username}?start={code}"
                        )
                    ]])
                )
            }
        return ConversationHandler.END
    elif update.message.chat.type == "private":
        context.user_data["lang"] = lang
        context.user_data["user"] = user
        context.user_data["chat"] = chat
        update.message.reply_text(model.lang.data[user.lang]["PASTE_PRIVATE_ENTRY"])
        return GET_SOURCE_CODE
    else: # WTF :/
        update.message.reply_text("unknown chat type!")
        return ConversationHandler.END

def get_source_code_state_handler(update: Update, context: CallbackContext, model):
    lang = context.user_data["lang"]
    if update.message.document:
        path = update.message.document.get_file().download()
        try:
            with open(path, 'r') as f:
                text = f.read()
            os.remove(path)
        except UnicodeDecodeError:
            update.message.reply_text(model.lang.data[lang]["PASTE_GET_SOURCE_CODE_FILE_ERROR"])
            return GET_SOURCE_CODE
    else:
        text = update.message.text
    context.user_data["source_code"] = text
    escaped_text = f"<code>{html.escape(text)}</code>"
    if len(escaped_text) > 4096:
        escaped_text = f"<code>{html.escape(text[:2040]+chr(10)+'...'+chr(10)+text[-2040:])}</code>"
    update.message.reply_text(
        escaped_text,
        parse_mode = "HTML"
    ).reply_text(
        model.lang.data[lang]["PASTE_GET_SOURCE_CODE_CONFIRM"],
        reply_markup=model.programming_languages_keyboard
    )
    return GET_LANG

def get_lang_handler(update: Update, context: CallbackContext, model):
    lang = context.user_data["lang"]
    query = update.callback_query
    context.user_data["prg_lang"] = query.data
    query.message.edit_text(
        text = model.lang.data[lang]["PASTE_GET_LANG_CONFIRM"],
        reply_markup=InlineKeyboardMarkup([[]])
    )
    return GET_TITLE

def get_lang_back_handler(update: Update, context: CallbackContext, model):
    lang = context.user_data["lang"]
    update.message.reply_text(
        model.lang.data[lang]["PASTE_GET_LANG_BACK_MESSAGE"]
    )
    return GET_SOURCE_CODE

def skip_get_title_state_handler(update: Update, context: CallbackContext, model):
    lang = context.user_data["lang"]
    context.user_data["title"] = ""
    update.message.reply_text(
        model.lang.data[lang]["PASTE_GET_TITLE_TEMP_CONFIRM"]
    )
    return GET_DESCRIPTION

def get_title_state_handler(update: Update, context: CallbackContext, model):
    lang = context.user_data["lang"]
    if len(update.message.text) > 50:
        update.message.reply_text(
            model.lang.data[lang]["PASTE_GET_TITLE_BAD_LANGHT"]
        )
        return GET_TITLE
    context.user_data["title"] = update.message.text
    update.message.reply_text(
        model.lang.data[lang]["PASTE_GET_TITLE_CONFIRM"]
    )
    return GET_DESCRIPTION

def skip_get_description_state_handler(update: Update, context: CallbackContext, model):
    lang = context.user_data["lang"]
    context.user_data["description"] = ""
    update.message.reply_text(
        model.lang.data[lang]["PASTE_GET_DESCRIPTION_TEMP_CONFIRM"],
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(model.lang.data[lang]["PASTE_GET_DESCRIPTION_KEYBOARD_POSITIVE"], callback_data="+"),
            InlineKeyboardButton(model.lang.data[lang]["PASTE_GET_DESCRIPTION_KEYBOARD_NEGITIVE"], callback_data="-")
        ]])
    )
    return CONFIRM

def get_description_state_handler(update: Update, context: CallbackContext, model):
    lang = context.user_data["lang"]
    context.user_data["description"] = update.message.text
    update.message.reply_text(
        model.lang.data[lang]["PASTE_GET_DESCRIPTION_CONFIRM"],
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(model.lang.data[lang]["PASTE_GET_DESCRIPTION_KEYBOARD_POSITIVE"], callback_data="+"),
            InlineKeyboardButton(model.lang.data[lang]["PASTE_GET_DESCRIPTION_KEYBOARD_NEGITIVE"], callback_data="-")
        ]])
    )
    return CONFIRM

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
            id = res["id"],
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
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    text=model.lang.data[lang]["PASTE_CONFIRM_SHARE_CODE_BUTTON"],
                    switch_inline_query=paste.id
                )
            ]])
        )
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
                "paste",
                pass_model_to(paste_command_handler, model)
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
