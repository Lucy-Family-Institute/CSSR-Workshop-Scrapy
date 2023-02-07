import scrapy
from scrapy import Spider
from bs4 import BeautifulSoup
import os, datetime, json
ROOT_DIR = os.getcwd()

class Reuters(Spider):
    name = "reuters"

    def start_requests(self):

        url_list = ['https://www.reuters.com/world/europe/zelenskiy-vows-changes-will-bolster-ukraine-amid-defence-minister-uncertainty-2023-02-06/']
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

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

        with open('../../crawldata/'+self.name+'.jsonl', 'a', encoding='utf-8') as f:
            json.dump({"title":title,"summary": summary, "article":article,}, f)
            f.write('\n')
