# coding=utf-8

import telebot
import os
import logging_utils
import logging
import helpers

config = helpers.read_config()

logger = logging_utils.create_default_logger(__name__)

bot = telebot.TeleBot(config['TelegramBot']['token'])
telebot.logger.handlers = []
telebot.logger.setLevel(logging.INFO)
telebot.logger.addHandler(logging_utils.logtail_handler)

root = os.path.abspath(os.path.dirname(__file__))
logger.info(f"Starting telegram bot on {root}")

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def handle_start_help(message):
    try:
        bot.reply_to(message, """\
Alertas de alterações de preços ou novos produtos lançados a cada 30min
Comandos:
/pricewatches - lista os urls da watchlist
/addpricewatch {url} - adiciona um novo url à watchlist
/removepricewatch {url} - remove um url da watchlist\
""")    
    except Exception as e:
        logger.error(e)

@bot.message_handler(commands=['pricewatches'])
def handle_get_price_watches(message):

    try:
        file_path = os.path.abspath(os.path.dirname(__file__)) + "/urls.txt"
        a_file = open(file_path)
        file_content = a_file.read()
        bot.reply_to(message, file_content)         
    except Exception as e:
        logger.error(e)

@bot.message_handler(commands=['addpricewatch'])
def handle_add_price_watche(message):
    try:
        url = message.text.replace('/addpricewatch', '').strip()

        if url == "":
            bot.reply_to(message, "Url inválido. Escreve o url após o comando: /addpricewatch {url}")
        else:
            file_path = os.path.abspath(os.path.dirname(__file__)) + "/urls.txt"
            a_file = open(file_path, "a")
            a_file.write(url + "\n")
            bot.reply_to(message, "Url adicionado: {}".format(url))           
    except Exception as e:
        logger.error(e)

@bot.message_handler(commands=['removepricewatch'])
def handle_remove_price_watche(message):
    try:
        url = message.text.replace('/removepricewatch', '').strip()
        found = False
        
        if url == "":
            bot.reply_to(message, "Url inválido. Escreve o url após o comando: /removewatch {url}")
        else:
            file_path = os.path.abspath(os.path.dirname(__file__)) + "/urls.txt"
            with open(file_path, "r") as f:
                lines = f.readlines()
            with open(file_path, "w") as f:
                for line in lines:
                    if line.strip("\n") != url:
                        f.write(line)
                    else:
                        found = True
        
        if found:
            bot.reply_to(message, f"Url removido: {url}")
        else:
            bot.reply_to(message, "Url não encontrado. Sem alterações")      
    except Exception as e:
        logger.error(e)


try:
    bot.infinity_polling()
except Exception as e:
    logger.error(e)
finally:
    logger.info("Shutting down telegram bot...")