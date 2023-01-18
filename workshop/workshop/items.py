# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RedditItem(scrapy.Item):
    # define the fields for your item here like:

    # Item key for post title
    title = scrapy.Field()

    # Item key for top layer comment
    comment_layer1 = scrapy.Field()

    # Item key for child layer comment(s)
    comment_layer2 = scrapy.Field()

    # pass
