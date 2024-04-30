# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Pokemon(scrapy.Item):
    pokedex_no = scrapy.Field()
    name = scrapy.Field()
    type1 = scrapy.Field()
    type2 = scrapy.Field()
    hp = scrapy.Field()
    attack = scrapy.Field()
    defense = scrapy.Field()
    sp_attack = scrapy.Field()
    sp_defense = scrapy.Field()
    speed = scrapy.Field()
    total_bst = scrapy.Field()
