import openai
from telegram.ext import CommandHandler, MessageHandler, filters

from sucinto.config import OPENAI_API_KEY
from sucinto.messages import Messages


openai.api_key = OPENAI_API_KEY
messages = Messages()

async def start(update, context):
    await update.message.reply_text("Hello!")

async def help(update, context):
    await update.message.reply_text("Help!")

async def resume(update, context):
    chat_id = update.effective_chat.id
    conversation = messages.retrieve(chat_id)

    if conversation == '':
        await update.message.reply_text("Não consegui ler nenhuma conversa ainda.")
        return 

    prompt = f"{conversation} \nOs usuários falaram sobre "

    request = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.6,
        max_tokens=500,
    )

    text = "Os usuários falaram sobre " + request['choices'][0]['text']
    await update.message.reply_text(text)

async def store_message(update, context):
    chat_id = update.effective_chat.id
    first_name = update.message.chat.first_name
    username = update.message.chat.username
    text = update.message.text
    messages.register(chat_id, first_name, username, text)


HANDLERS = [
    CommandHandler('start', start),
    CommandHandler('help', help),
    CommandHandler('resume', resume),
    MessageHandler(filters.TEXT & ~filters.COMMAND, store_message),
]