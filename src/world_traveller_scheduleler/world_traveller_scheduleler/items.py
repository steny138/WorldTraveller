# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
class WorldTravellerSchedulelerItem(scrapy.Item):
    """ 景點 Model """
    viewid = scrapy.Field()
    name = scrapy.Field()
    location = scrapy.Field()
    en_name = scrapy.Field()
    address = scrapy.Field()
    cover = scrapy.Field()
    rate = scrapy.Field()
    comments = scrapy.Field()
    outer_key = scrapy.Field() 
    contact = scrapy.Field()
    description = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    homepage = scrapy.Field()
    business_hours = scrapy.Field()
