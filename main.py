# -*- coding: utf-8 -*-

__coder__ = "Moshen-FN"
codehub = "codehub.pythonanywhere.com"

from telegram.ext import CommandHandler, MessageHandler, Updater, Filters
import requests
from os import remove
import func_conf, text_conf

conn = func_conf.connection_gen()
c = conn.cursor()
func_conf.table_gen(c)
func_conf.reset_temp_files()

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

def python_doc_func(update, context):
    update.message.document.get_file().download("./temp_file.py")
    with open("./temp_file.py") as pff:
        req = requests.post(text_conf.url,
                        data=func_conf.param_gen(update.message.from_user.first_name,
                                                 pff.read(),"python"))
        update.message.reply_text(req.json()["link"])
    try:
        remove("temp_file.py")
    except:
        pass

def text_doc_func(update, context):
    try:
        update.message.document.get_file().download("./temp_file_text.txt")
        with open("./temp_file_text.txt") as tff:
            req = requests.post(text_conf.url,
                            data=func_conf.param_gen(update.message.from_user.first_name,
                                                    tff.read(),"text"))

            update.message.reply_text(req.json()["link"])
        try:
            remove("temp_file_text.txt")
        except:
            pass
    except Exception as error:
        print(error)

updater = Updater(text_conf.token, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start_func))
updater.dispatcher.add_handler(MessageHandler(Filters.text, paste_func))
updater.dispatcher.add_handler(MessageHandler(Filters.document.py, python_doc_func))
updater.dispatcher.add_handler(MessageHandler(Filters.document.txt, text_doc_func))
print("Running ...")
updater.start_polling()
updater.idle()
