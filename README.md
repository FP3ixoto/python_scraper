# Worten Scraper
This project is a web scraper that can scrape Worten produts for price changes and notify using the telegram bot api (see https://core.telegram.org/bots/api).
Includes logging integrated with Logtail platform (see https://betterstack.com/logtail) 

## Running and experimenting locally
1 - Create/update the configurations.ini (or configuration.Development.ini) file with the needed config.

2 - Install dependencies 
```
pip3 install -r requirements.txt
```

3 - Run the scripts

To run the web scrapper
```
python main.py
```

To run the telegram bot listener
```
python telegrambot.py
```
