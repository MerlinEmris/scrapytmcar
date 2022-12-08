# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TmcarsItem(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    house_type = scrapy.Field()
    floor_count = scrapy.Field()
    building_floor_count = scrapy.Field()
    room_count = scrapy.Field()
    interior_type = scrapy.Field()
    description = scrapy.Field()
    location = scrapy.Field()
    phone = scrapy.Field()
    post_date = scrapy.Field()
    views = scrapy.Field()

