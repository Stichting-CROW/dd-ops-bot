import os
import requests

def send_telegram_msg(text, chat_id):
   token = os.getenv("TELEGRAM_TOKEN")
   text = text.replace("-", "\-").replace(".", "\.").replace("_", "\_")
   # Info on parse_mode:
   # https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#message-formatting-bold-italic-code-
   # https://stackoverflow.com/a/66640534
   # https://docs.python-telegram-bot.org/en/stable/telegram.parsemode.html
   url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + str(chat_id) + "&parse_mode=MarkdownV2&text=" + text
   results = requests.get(url_req)
   print(results.json())