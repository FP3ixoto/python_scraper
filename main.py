# coding=utf-8

import logging
from bs4 import BeautifulSoup
import cloudscraper
import telebot
import schedule
import time
from fcache.cache import FileCache
import os
import logging_utils
import json
import helpers

class Product:
    def __init__(self, name, price, url, availability):
        self.name = name
        self.price = price
        self.url = url
        self.availability = availability

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

def check_products():
    try:
        file_path = os.path.abspath(os.path.dirname(__file__)) + "/urls.txt"
        logger.info(f"Reading products urls from {file_path}.")

        a_file = open(file_path)
        file_content = a_file.read()
        urls = file_content.splitlines()

        for url in urls:
            try:
                check_product(url)
            except Exception as e:
                logger.error("Error while checking product: " + str(e))
    except Exception as e:
        logger.error("check_products: " + str(e))

def check_product(url):

    product = get_product_from_server(url)
    product_cache_name = url[-15:] if len(url) >= 15 else url

    if product_cache_name not in cache:
        logger.info("New product found.", extra={'product': product.toJSON()})
        notify(product, None)
    else:
        old_product = cache[product_cache_name]

        if product.price != old_product.price or product.availability != old_product.availability:
            logger.info(f"Product was updated.", extra={'product': product.toJSON(), 'old_product': old_product.toJSON()})
            notify(product, old_product)
        else:
            logger.info("Product didn't change. Not raising notification.'.", extra={'product': product.toJSON()})

    cache[product_cache_name] = product


def notify(product, old_product):
    logger.info("Sending notification to telegram.", extra={'product': product.toJSON()})

    if old_product is None:
        telegramBot.send_message(config['TelegramBot']['chat_id'], f"""\
[Novo] <b>{product.name}</b>
€ {product.price}
{product.availability}
&#128279; <a href="{product.url}">link</a>\
""")
    else:
        telegramBot.send_message(config['TelegramBot']['chat_id'], f"""\
[Atualização] <b>{product.name}</b>
{f"<s>€ {old_product.price}</s> &#10145; € {product.price}" if product.price != old_product.price else f"€ {product.price}" }
{f"<s>{old_product.availability}</s> &#10145; {product.availability}" if product.availability != old_product.availability else f"{product.availability}" }
&#128279; <a href="{product.url}">link</a>\
""")

    logger.info("Notification sent.", extra={'product': product.toJSON()})


def get_product_from_server(url):
    logger.info("Getting product from {}.".format(url))

    scraper = cloudscraper.create_scraper(browser='chrome')
    content = scraper.get(url).text 
    
    soup = BeautifulSoup(content, features="html.parser")
    prod_name = soup.find('h1', class_='iss-product-name').text.strip()
    prod_price = soup.find('span', class_='iss-product-current-price')['content']
    prod_unavailability = soup.find('div', class_='w-product__unavailability-title')
    
    return Product(prod_name, float(prod_price.replace(",", ".")), url, "Disponível" if prod_unavailability is None else "Indisponível")
    
config = helpers.read_config()
logger = logging_utils.create_default_logger(__name__)

root = os.path.abspath(os.path.dirname(__file__))
logger.info(f"Starting application on {root}")
logger.info(f"Telegram notifications will be sent to chat group {config['TelegramBot']['chat_id']}")

telegramBot = telebot.TeleBot(config['TelegramBot']['token'], parse_mode='HTML')
telebot.logger.handlers = []
telebot.logger.setLevel(logging.INFO)
telebot.logger.addHandler(logging_utils.logtail_handler)

cache = FileCache('worten_products', flag='cs', app_cache_dir=root)

schedule.every(30).minutes.do(check_products)
schedule.run_all(delay_seconds=5)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)  
except Exception as e:
    logger.error(str(e))
finally:
    logger.info("Shutting down ...")