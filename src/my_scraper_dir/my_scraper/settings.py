# ------------------- Scrapy settings -------------------
# Note: These settings are overwritten by the settings in the main.py file when the crawler is run
#       -> might not be up-to-date

# The name of the scrapy project
BOT_NAME = 'my_scraper'

# The path to the spider modules
SPIDER_MODULES = ['my_scraper.spiders']
NEWSPIDER_MODULE = 'my_scraper.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Use the item pipeline to store the data in the postgres database
ITEM_PIPELINES = {
    "my_scraper.pipelines.PostgresPipeline": 300,
}

# Suppress the logging messages
LOG_ENABLED = False
