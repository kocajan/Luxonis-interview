# ------------------- Scrapy items -------------------

import scrapy


class RealityItem(scrapy.Item):
    # Define the fields for your item here:
    name = scrapy.Field()
    image_url = scrapy.Field()
