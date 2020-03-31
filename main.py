# -*- coding: utf-8 -*-

__coder__ = "Moshen-FN"
codehub = "codehub.pythonanywhere.com"

from telegram.ext import CommandHandler, MessageHandler, Updater, Filters
import requests
import func_conf, text_conf

conn = func_conf.connection_gen()
c = conn.cursor()
func_conf.table_gen(c)

def start_func(update, context):
    update.message.reply_text(text_conf.start_text)
    
    func_conf.insert__(c,conn, update.message.from_user.id,
                       update.message.from_user.first_name,
                       func_conf.simple_time_gen()
                       )
    
def paste_func(update, context):
    req = requests.post(text_conf.url,
                        data=func_conf.param_gen(update.message.from_user.first_name,
                                                 update.message.text,
                                                 "python")
                        )
    try:
        update.message.reply_text(req.json()["link"])
    except:
        update.message.reply_text(text_conf.exception_gi)


updater = Updater(text_conf.token, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start_func))
updater.dispatcher.add_handler(MessageHandler(Filters.text, paste_func))
print("Running ...")
updater.start_polling()
updater.idle()
