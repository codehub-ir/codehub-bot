import os
from telegram import (
    ChatMember,
    Message,
    Update
)
from telegram.ext import (
    CommandHandler,
    CallbackContext,
)
from telegram.error import (
    RetryAfter,
    TimedOut,
    BadRequest,
)
from ..functions import pass_model_to
import html, datetime, time
from dotenv import load_dotenv
load_dotenv()

frames = [
    """________________________
|U                    U|
|U  .______________.  U|
|U  |norooz mobarak|  U|
|U  \——————————————/  U|
|U      |       |     U|
|U       \(^o^)/      U|
|U                    U|
|U____________________U|""",
    """________________________
|U____                U|
|U\ n \               U|
|U \ o \              U|
|U  \ r \             U|
|U   \ o \            U|
|U    \ o \           U|
|U     \ z \          U|
|U      \   \         U|
|U       \ m \        U|
|U        \ o \       U|
|U         \ b \      U|
|U          \ a \     U|
|U           \ r \    U|
|U            \ a \   U|
|U       ______\ k \  U|
|U      |       \———\ U|
|U      |         /   U|
|U      |(^o^)———|    U|
|U      (active)      U|
|U____________________U|""",
    """_______________________
|U       | n |       U|
|U       | o |       U|
|U       | r |       U|
|U       | o |       U|
|U       | o |       U|
|U       | z |       U|
|U       |   |       U|
|U       | m |       U|
|U       | o |       U|
|U       | b |       U|
|U       | a |       U|
|U       | r |       U|
|U       | a |       U|
|U       | k |       U|
|U       \———/       U|
|U       /   \       U|
|U      |     |      U|
|U      |(^o^)|      U|
|U      (active)     U|
|U___________________U|""",
    """________________________
|U                ____U|
|U               / n /U|
|U              / o / U|
|U             / r /  U|
|U            / o /   U|
|U           / o /    U|
|U          / z /     U|
|U         /   /      U|
|U        / m /       U|
|U       / o /        U|
|U      / b /         U|
|U     / a /          U|
|U    / r /           U|
|U   / a /            U|
|U  / k / _____       U|
|U /———/       |      U|
|U  \          |      U|
|U   |———(^o^)/       U|
|U      (active)      U|
|U____________________U|""",
    """________________________
|U                    U|
|U  .______________.  U|
|U  |ʞɐɹɐqoɯ zooɹou|  U|
|U  \——————————————/  U|
|U      |       |     U|
|U       \(X#X)/      U|
|U   (take a breath)  U|
|U____________________U|""",
    """________________________
|U____                U|
|U\ ʞ \               U|
|U \ ɐ \              U|
|U  \ ɹ \             U|
|U   \ ɐ \            U|
|U    \ q \           U|
|U     \ o \          U|
|U      \ ɯ \         U|
|U       \   \        U|
|U        \ z \       U|
|U         \ o \      U|
|U          \ o \     U|
|U           \ ɹ \    U|
|U            \ o \   U|
|U       ______\ u \  U|
|U      |       \———\ U|
|U      |         /   U|
|U      |(^o^)———|    U|
|U      (active)      U|
|U____________________U|""",
    """_______________________
|U       | ʞ |       U|
|U       | ɐ |       U|
|U       | ɹ |       U|
|U       | ɐ |       U|
|U       | q |       U|
|U       | o |       U|
|U       | ɯ |       U|
|U       |   |       U|
|U       | z |       U|
|U       | o |       U|
|U       | o |       U|
|U       | ɹ |       U|
|U       | o |       U|
|U       | u |       U|
|U       \———/       U|
|U       /   \       U|
|U      |     |      U|
|U      |(^o^)|      U|
|U      (active)     U|
|U___________________U|""",
    """________________________
|U                ____U|
|U               / ʞ /U|
|U              / ɐ / U|
|U             / ɹ /  U|
|U            / ɐ /   U|
|U           / q /    U|
|U          / o /     U|
|U         / ɯ /      U|
|U        /   /       U|
|U       / z /        U|
|U      / o /         U|
|U     / o /          U|
|U    / ɹ /           U|
|U   / o /            U|
|U  / u / _____       U|
|U /———/       |      U|
|U  \          |      U|
|U   |———(^o^)—|      U|
|U      (active)      U|
|U____________________U|""",
    """________________________
|U                    U|
|U  .______________.  U|
|U  |norooz mobarak|  U|
|U  \——————————————/  U|
|U      |       |     U|
|U       \(v.v)/      U|
|U     short break    U|
|U____________________U|""",
    """________________________
|U                    U|
|U  .______________.  U|
|U  |norooz mobarak|  U|
|U  \——————————————/  U|
|U      |       |     U|
|U       \(^o^)/      U|
|U(see you next year!)U|
|U____________________U|""",
]

def auto_next_frame(message: Message):
    finish = datetime.datetime.now()+datetime.timedelta(days=1)
    time.sleep(5)
    while finish > datetime.datetime.now():
        try:
            for frame in frames[1:5]:
                try:
                    message.edit_text(
                        text = f"<code>{html.escape(frame)}</code>",
                        parse_mode = "HTML",
                    )
                except BadRequest:
                    pass
                time.sleep(1)
            time.sleep(3)
            for frame in frames[5:9]:
                try:
                    message.edit_text(
                        text = f"<code>{html.escape(frame)}</code>",
                        parse_mode = "HTML",
                    )
                except:
                    pass
                time.sleep(1)
            time.sleep(7)
        except TimedOut:
            time.sleep(2)
            continue
        except RetryAfter as err:
            print("/norooz: retry after", err.retry_after)
            time.sleep(err.retry_after)
    while 1:
        try:
            message.edit_text(
                text = f"<code>{html.escape(frames[9])}</code>",
                parse_mode = "HTML",
            )
            break
        except TimedOut:
            time.sleep(2)
        except RetryAfter:
            print("/norooz: retry after", err.retry_after)
            time.sleep(err.retry_after)

def norooz_command_handler(update: Update, context: CallbackContext, model):
    update.message.delete()
    ADMIN = int(os.getenv("ADMIN", "0"))
    if 0==ADMIN and context.bot.get_chat_member(
        chat_id=update.message.chat.id,
        user_id=update.message.from_user.id,
    ).status not in (ChatMember.ADMINISTRATOR, ChatMember.CREATOR):
        return
    elif ADMIN!=update.message.from_user.id:
        return
    message = context.bot.send_message(
        chat_id = update.message.chat.id,
        text = f"<code>{html.escape(frames[0])}</code>",
        parse_mode = "HTML",
    )
    context.chat_data["norooz_message"]=message
    context.job_queue.run_once(
        callback=lambda _: auto_next_frame(message),
        when=datetime.timedelta(milliseconds=1),
    )

def creator(model):
    handler = CommandHandler(
        "norooz",
        pass_model_to(norooz_command_handler, model)
    )
    return handler
