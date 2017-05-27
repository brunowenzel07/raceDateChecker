# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags

class RecingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    racedate = scrapy.Field()
    racecourse = scrapy.Field()
    noraces = scrapy.Field()

