<p align="center">
    <img width="140" src="https://raw.githubusercontent.com/codehub-ir/codehub-graphics/0dd43fd4d2f145f511332f09cc415acffe9e6637/github-org/SVGs/logotype-170.svg" />
</p>

<p align="center">
    <h1 align="center">
        <a href="https://codehub.pythonanywhere.com/">Codehub Telegram Bot (V2.0)</a>
    </h1>
</p>

English | [فارسی](./README-FA.md)

An interface using telegram API, via "python-telegram-bot" library to add, find and share pastes.

## Requirements

here are required libraries listed in `requirements.txt`:

1. python-telegram-bot
2. python-dotenv
3. peewee

## Usage

1. install the requirements:

    ```bash
    pip install -r requirements.txt
    ```

2. create a `.env` file (alongside the `main.py` file), with this content:

    ```text
    TOKEN="..."
    WEBHOOK="..."
    ```

    set `TOKEN` to your bot token. you can get the token from `@botfather` in telegram.

    if you need to use webhook, set `WEBHOOK` to the url. otherwise, don't change it (`WEBHOOK=""`).

3. fire!

    ```bash
    python3 main.py
    ```

    you may use something like `tmux` if you're not using webhook.

    note: this program uses `sqlite3` to save users, chats and pastes. you can change it from `src/model/__init__.py`. check [peewee doc](http://docs.peewee-orm.com/en/latest/peewee/database.html).

## Contributing

there are many files here; however, you just need to check 2 parts:

1. `src/handler`

    this folder contains any handler that you need. each handler has a folder in this form: `src/handler/<NAME>`. the handler will be written in `src/handler/<NAME>/__init__.py`. in this file, you should make a function named `creator(model)`. `model` is the imported object of `src/model`. this function receives this parameter, then only returns the handler. you can make a lot of this folders to write your handlers in them.

    for example, we imagine a handler to handle `/start` command. you will make a folder and a file like `src/handler/my_start_handler/__init__.py`. then, you'll open this file, and write something like this:

    ```python
    from telegram.ext import CommandHandler, CallbackContext
    from telegram import Update

    def your_function(update: Update, context: CallbackContext):
        update.message.reply_text("hello!")

    def creator(model):
        return CommandHandler("start", your_function)
    ```

    however, you may want to use an attribute from `src/model`, like `HELLO_TEXT`. I suggest you to make a function to pass model. this function is written at `src/handler/functions.py`. so, you can use it like this:

    ```python
    from telegram.ext import CommandHandler, CallbackContext
    from telegram import Update
    from ..function import pass_model_to

    def your_function(update: Update, context: CallbackContext, model):
        update.message.reply_text(model.HELLO_TEXT)

    def creator(model):
        return CommandHandler("start", pass_model_to(your_function, model))
    ```

    if you have some functions/classes that you want to use them in many handlers, you can put them in `src/handler/functions.py`, then, import them.

    when your handler is completed, you should import its `creator` in `src/handler/__init__.py`, and add it to `CREATORS` tuple. for example, if you want to add that `my_start_handler`, OK? so, add this line to `src/handler/__init__.py`:

    ```python
    from my_start_handler import creator as my_start_handler_creator
    ```

    as you can see, when you add `<NAME>` handler, it's better to change its `creator` name to `<NAME>_creator` (`from <NAME> import creator as <NAME>_creator`).then, add it to the `CREATORS` tuple.

    imagine that you have 3 hanlders:

    1. `hanlder1` (`src/hanlder/hanlder1`)
    2. `hanlder2` (`src/hanlder/hanlder2`)
    3. `hanlder3` (`src/hanlder/hanlder3`)

    then, you should write `src/hanlder/__init__.py` like this:

    ```python
    from handler1 import creator as handler1_creator
    from handler2 import creator as handler2_creator
    from handler3 import creator as handler3_creator
    # from your_new_handler import creaotr as your_new_hanlder_creator

    CREATORS = (
        handler1_creator,
        handler2_creator,
        handler3_creator,
        # your_new_hanlder_creator,
    )

    # don't change it, don't remove it, don't see it, and don't think about it at all!
    def get_handlers(model):
        for creator in CREATORES:
            yield creator(model)
    ```

    *note: if you don't add it, then the handler won't be added to the `dispatcher`. if your handler is not executed, maybe that's because you didn't add it here!*

2. `src/model`

    this part provides any data about languages, database, etc. for now, it contains the database part, and language part. it is imported and passed to the handlers creator (`model` parameter at `creator(model)`, remember?). for example, if you define `EXAMPLE = 123` at `src/model/__init__.py`, you can use it in `model` parameter as `model.EXAMPLE`.
