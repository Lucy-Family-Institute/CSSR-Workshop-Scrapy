import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import os, datetime
from scrapy.loader import ItemLoader
from workshop.items import Reuters
ROOT_DIR = os.getcwd()


class ReutersCrawl(CrawlSpider):
    name = 'goodreads'
    allowed_domains = ['goodreads.com']
    start_urls = ['https://www.goodreads.com/quotes/tag/classic-literature']


    rules = (
        Rule(LinkExtractor(allow=('quotes/tag/.+$',)), follow=True),
        Rule(LinkExtractor(allow=('work/quotes/\d+$')), callback='parse_item'),
    )

    def parse_item(self, response):
        # self.logger.info('item page log: %s', response.url)
        goodreads_instance = ItemLoader(item=GoodReads(), response=response)

        # xpath selector
        title = response.xpath('//h1[@class="quoteText"]//text()').extract()
        # css selector
        title = response.css('h1[class="quoteText"] *::text').extract()

        # method 1: Extract entire text of the page
        body = BeautifulSoup(response.text, features="html.parser")
        body = "".join(body.get_text()).strip()

        # method 2: Extract sections separately

        ## extract summary
        ## xpath selector
        summary = response.xpath('//*[contains(@class,"article-body__content")]//*[contains(@class,"summary__summary")]//text()').extract()
        ## css selector
        summary = response.css('[class*="article-body__content"] [class*="summary__summary"] *::text').extract()

        ## extract article
        ## xpath selector
        article = response.xpath('//*[contains(@class,"article-body__content")]//*[contains(@data-testid,"paragraph")]//text()').extract()
        ## css selector
        article = response.css('[class*="article-body__content"] [data-testid*="paragraph"] *::text').extract()

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
# process.crawl(ReutersCrawl)
# process.start()