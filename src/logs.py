import os
import logging
import telebot
import configparser

os.makedirs("logs", exist_ok=True)

DIR = r"logs"
FILE = r"log.txt"
TELEGRAM_CONFIG = os.path.expanduser("~/.config/telegram.ini")
logfile = os.path.join(DIR, FILE)

# ---- SETUP LOGGING ----
logging.basicConfig(
    filename=logfile,
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger()

# ---- SETUP TELEGRAM CONFIG ----
config = configparser.ConfigParser()
try:
    config.read(TELEGRAM_CONFIG)
    TOKEN = config.get("Telegram", "token")
    CHAT_ID = config.get("Telegram", "chat_id")
except Exception as e:
    log.error(f"Error reading configuration file: {e}")

def ntfy(msg: str) -> None:
    """
    Sends `msg` string to Telegram bot defined with `TOKEN` and `CHAT_ID` global variables.
    """
    # starting bot
    bot = telebot.TeleBot(TOKEN)

    try:
        bot.send_message(CHAT_ID, msg)
    except Exception as e:
        log.error(f"Failed to send Telegram notification: {e}")