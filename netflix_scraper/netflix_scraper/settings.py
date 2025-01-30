# Scrapy settings for netflix_scraper project

BOT_NAME = "netflix_scraper"

SPIDER_MODULES = ["netflix_scraper.spiders"]
NEWSPIDER_MODULE = "netflix_scraper.spiders"
ITEM_PIPELINES = {
    'netflix_scraper.pipelines.NetflixTop10Pipeline': 1,
}

MONGO_URI = "mongodb://root:example@mongodb:27017/"
MONGO_DATABASE = "netflix_db"

ROBOTSTXT_OBEY = False

# Default configurations
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
