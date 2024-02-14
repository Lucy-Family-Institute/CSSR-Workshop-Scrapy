# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GoodReads(scrapy.Item):
    # define the fields for your item here like:

    # Item key for post title
    quote = scrapy.Field()

    # Item key for top layer comment
    AuthorTitle = scrapy.Field()

    # Item key for child layer comment(s)
    Likes = scrapy.Field()

    # pass
