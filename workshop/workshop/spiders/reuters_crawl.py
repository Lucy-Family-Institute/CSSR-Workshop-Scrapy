import scrapy
from scrapy.spiders import CrawlSpider, Rule
# from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import os, datetime
from scrapy.loader import ItemLoader
from workshop.items import Reuters
ROOT_DIR = os.getcwd()


class ReutersCrawl(CrawlSpider):
    name = 'reuterscrawl'
    allowed_domains = ['reuters.com']
    start_urls = ['https://www.reuters.com/lifestyle/sports/']


    rules = (
        Rule(LinkExtractor(allow=('lifestyle/sports/$',)), follow=True),
        Rule(LinkExtractor(allow=('lifestyle/sports/.+/')), callback='parse_item'),
    )

    def parse_item(self, response):
        # self.logger.info('item page log: %s', response.url)
        reuters_instance = ItemLoader(item=Reuters(), response=response)

        # xpath selector
        title = response.xpath('//h1[@data-testid="Heading"]//text()').extract()
        # css selector
        title = response.css('h1[data-testid="Heading"] *::text').extract()

        # method 1: Extract entire text of the page
        body = BeautifulSoup(response.text, features="html.parser")
        body = "".join(body.get_text()).strip()

        # method 2: Extract sections separately

        ## extract summary
        ## xpath selector
        summary = response.xpath('//*[contains(@class,"paywall-article")]//*[contains(@class,"summary__summary")]//text()').extract()
        ## css selector
        summary = response.css('[class*="paywall-article"] [class*="summary__summary"] *::text').extract()

        ## extract article
        ## xpath selector
        article = response.xpath('//*[contains(@class,"paywall-article")]//*[contains(@data-testid,"paragraph")]//text()').extract()
        ## css selector
        article = response.css('[class*="paywall-article"] [data-testid*="paragraph"] *::text').extract()

        # item['title'] = title
        # item['comment_layer1'] = comment_layer1
        # item['comment_layer2'] = comment_layer2
        # yield item
        # return response(item)
        reuters_instance.add_value('title',title)
        reuters_instance.add_value('summary',summary)
        reuters_instance.add_value('article',article)
        return reuters_instance.load_item()

# process = CrawlerProcess({
#     'CONCURRENT_REQUESTS_PER_IP': 2,
#     'DOWNLOAD_DELAY': 5,
#     'CLOSESPIDER_PAGECOUNT': 10,
# })

# process.crawl(RedditCrawl)
# process.start()