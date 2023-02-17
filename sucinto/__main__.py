import logging
from telegram.ext import Application
from telegram.error import InvalidToken, TimedOut

from sucinto.commands import HANDLERS
from sucinto.config import TELEGRAM_API_KEY


logging.basicConfig(filename="sucinto.log", encoding="utf-8", level=logging.INFO)


def main():
    logging.info("Starting the Server.")

    try:
        app = Application.builder().token(TELEGRAM_API_KEY).build()
    except InvalidToken as error:
        logging.critical("Invalid Telegram API KEY.")
        print('Você deve colocar o token do seu bot no arquivo ".env".')
        print("Caso não possua um token solicite em https://t.me/Botfather!")
        exit()

    for handler in HANDLERS:
        app.add_handler(handler)

    logging.info("Running.")
    try:
        app.run_polling()
    except TimedOut as error:
        logging.critical(error)

    logging.info("Exiting Server.")


if __name__ == "__main__":
    main()
