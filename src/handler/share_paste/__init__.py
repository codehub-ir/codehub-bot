from telegram import (
    InlineQueryResultArticle,
    ParseMode,
    InputTextMessageContent,
    Update,
)
from telegram.ext import (
    Updater,
    InlineQueryHandler,
    CommandHandler,
    CallbackContext
)
import requests
from ..functions import pass_model_to, codehub

def inline_query_handler(update: Update, context: CallbackContext, model):
    query = update.inline_query.query
    user = model.User.get_or_none(model.User.id == update.inline_query.from_user.id)
    if not user:
        update.inline_query.answer([])
        return
    lang = user.lang
    res = [
        InlineQueryResultArticle(
            id=paste.id,
            title=paste.title + f"({paste.lang})",
            description=paste.description,
            input_message_content=InputTextMessageContent(
                model.lang.data[lang]["START_CONFIRM_RESULT_FOR_CHAT"].format(
                    title = paste.title,
                    description = paste.description,
                    lang = paste.lang,
                    time = str(paste.created_on),
                    url = f"https://codehub.pythonanywhere.com/snippet/{paste.id}"
                ),
                disable_web_page_preview=True
            )
        )
        for paste in user.pastes
        if query in paste.title or query == paste.id or query == paste.lang
    ]
    update.inline_query.answer(res)

def creator(model):
    handler = InlineQueryHandler(pass_model_to(inline_query_handler, model))
    return handler
