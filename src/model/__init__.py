import peewee as pw
from . import lang
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

afoot_pastes = dict()

programming_languages = (
    'arduino', 'bash', 'c', 'cpp', 'csharp', 'css', 'dart',
    'docker', 'docker-compose', 'go', 'html', 'java', 
    'js', 'json', 'lua', 'md', 'mysql', 'php', 'python', 'rb'
)
programming_languages_keyboard = [
    ['arduino', 'bash', 'c', 'cpp'],
    ['csharp', 'css', 'dart', 'docker'],
    ['docker-compose', 'go', 'html'],
    ['java', 'js', 'json', 'lua', 'md'],
    ['mysql', 'php', 'python', 'rb']
]
programming_languages_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton(y, callback_data=y) for y in x]
    for x in programming_languages_keyboard
])

languages_keyboard = [
    ['fa', 'en']
]
languages_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton(y, callback_data=y) for y in x]
    for x in languages_keyboard
])

db = pw.SqliteDatabase("database.db")

class Chat(pw.Model):
    id = pw.BigIntegerField(primary_key=True)
    lang = pw.TextField(default=lang.DEFAULT)
    class Meta:
        database = db

class User(pw.Model):
    id = pw.BigIntegerField(primary_key=True)
    lang = pw.TextField(default=lang.DEFAULT)
    class Meta:
        database = db

class Paste(pw.Model):
    title = pw.TextField()
    description = pw.TextField()
    created_on = pw.DateTimeField(formats="%Y-%m-%dT%H:%M:%S.%f%z")
    lang = pw.TextField()
    id = pw.TextField(primary_key=True)
    chat = pw.ForeignKeyField(Chat, backref="pastes")
    user = pw.ForeignKeyField(User, backref="pastes")
    class Meta:
        database = db

db.connect()
db.create_tables([Chat, User, Paste])
