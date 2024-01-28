# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksItem(scrapy.Item):
    author = scrapy.Field()
    title = scrapy.Field()
    rating = scrapy.Field()
    ratings = scrapy.Field()
    genres = scrapy.Field()
    link = scrapy.Field()
