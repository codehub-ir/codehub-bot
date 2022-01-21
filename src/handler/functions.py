from telegram import Update
from telegram.ext import CallbackContext
import random, string, requests

def pass_model_to(function, model):
    def wrapper(update: Update, context: CallbackContext):
        return function(update = update, context = context, model = model)
    return wrapper

CHARS = string.ascii_letters + string.digits
def generate_random_code(not_in = None) -> str:
    if not_in is None:
        return random.sample(CHARS, len(CHARS))
    code = "".join(random.sample(CHARS, len(CHARS)))
    while code in not_in:
        code = random.sample(CHARS, len(CHARS))
    return code

class codehub:
    def snippet_create(title, description, body, lang):
        res = requests.post(
            "https://codehub.pythonanywhere.com/api/v1/snippet",
            data = {
                "title": title,
                "description": description,
                "body": body,
                "lang": lang
            }
        )
        return res.json()
