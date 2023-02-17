import openai
import logging
from telegram.ext import CommandHandler, MessageHandler, filters
from telegram.constants import ParseMode

from sucinto.config import OPENAI_API_KEY
from sucinto.messages import Messages


openai.api_key = OPENAI_API_KEY
messages = Messages()

INFO_TEXT = """\
🕹 *INSTRUÇÕES*:
/resume - Faz um resumo das últimas mensagens.
/clear - O bot esquece o que foi lido.
/info - Mostra esta mensagem de ajuda.

🚨 *IMPORTANTE*:
O bot não armazena permanentemente suas mensagens e elas não estão expostas.

⁉️ *CÓDIGO FONTE*:
https://github.com/andrefpf/sucinto

"""


async def start(update, context):
    await update.message.reply_text("Hello!")


async def info(update, context):
    await update.message.reply_text(INFO_TEXT, parse_mode=ParseMode.MARKDOWN)


async def resume(update, context):
    logging.info("Resuming a conversation")

    chat_id = update.effective_chat.id
    conversation = messages.retrieve(chat_id)

    if conversation == "":
        await update.message.reply_text("Não consegui ler nenhuma conversa ainda.")
        return

    prompt = (
        f"{conversation} \n\nFaça um resumo sobre o que foi falado na conversa acima."
    )

    request = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.6,
        max_tokens=500,
    )

    messages.clear(chat_id)  # clear stored messages after resumed
    text = request["choices"][0]["text"]
    await update.message.reply_text(text)


async def store_message(update, context):
    logging.info("Saving message")

    if update.message.forward_date is None:
        first_name = update.message.chat.first_name
        username = update.message.chat.username
    else:
        forwarded = update.message.forward_from
        if forwarded is not None:
            first_name = forwarded.first_name
            username = forwarded.username
        else:
            first_name = "Sem nome"
            username = "desconhecido"

    chat_id = update.effective_chat.id
    text = update.message.text
    messages.register(chat_id, first_name, username, text)


async def clear(update, context):
    chat_id = update.effective_chat.id
    messages.clear(chat_id)
    await update.message.reply_text("As mensagens deste chat foram obliteradas.")


HANDLERS = [
    CommandHandler("start", start),
    CommandHandler("info", info),
    CommandHandler("clear", clear),
    CommandHandler("resume", resume),
    MessageHandler(filters.TEXT & ~filters.COMMAND, store_message),
]
