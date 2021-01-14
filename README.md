# Visa appointments scraper
This scraper is made for checking the ais.usvisa-info.com site in time intervals. It logs you in, and scrape the payment site and when there's an available appointment (a change on the original site where there are not appointments), it will notify you through a Telegram bot.

## TODO
- [ ] Add a timestamp to each run.
- [ ] Add requiriments.
- [ ] Add tests.

## Installation
1. Install chromedriver
2. Install requirements

## Usage
Run via SSH on a Raspberry. The process will create a 
```
nohup python3 selenium_scraper.py &
```

