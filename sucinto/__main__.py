from telegram.ext import Application
from telegram.error import InvalidToken

from sucinto.commands import HANDLERS
from sucinto.config import TELEGRAM_API_KEY

def main():
    try:
        app = Application.builder().token(TELEGRAM_API_KEY).build()
    except InvalidToken as error:
        print('Você deve colocar o token do seu bot no arquivo ".env".')
        print('Caso não possua um token solicite em https://t.me/Botfather!')
        exit()

    for handler in HANDLERS:
        app.add_handler(handler)
    
    app.run_polling()

if __name__ == "__main__":
    main()