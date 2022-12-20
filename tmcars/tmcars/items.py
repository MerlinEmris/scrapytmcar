# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TmcarsItem(scrapy.Item):
    link = scrapy.Field()
    post_date = scrapy.Field()
    views = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    details = scrapy.Field()
    images = scrapy.Field()



