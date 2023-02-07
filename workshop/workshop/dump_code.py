custom_settings = {
    'FEED_URI': name + datetime.datetime.today().strftime('%y%m%d') + '.jsonl',
    'FEED_FORMAT': 'jsonlines',
    'FEED_EXPORTERS': {'json': 'scrapy.exporters.JsonLinesItemExporter',},
    'FEED_EXPORT_ENCODING': 'utf-8',
}


class Reddit(Spider):
    name = "reddit"

    def start_requests(self):

        url_list = ['https://old.reddit.com/r/HarryPotterMemes/comments/108rj3j/anyone_else_pick_up_a_copy_of_cedrics_biography/']
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        # xpath selector
        title = response.xpath('//*[@class="title"]//*[@class="title may-blank outbound"]//text()').extract()
        # css selector
        title = response.css('.title .title.may-blank.outbound *::text').get()


        # method 1: Extract entire text of the page
        body = BeautifulSoup(response.text, features="html.parser")
        body = "".join(body.get_text()).strip()

        # method 2: Extract only the comments
        ## xpath selector
        comments = response.xpath('//*[@class="commentarea"]//*[@class="usertext-body may-blank-within md-container "]//text()').extract()

        ## css selector
        comments = response.css('.commentarea .usertext-body.may-blank-within.md-container  *::text').extract()


        # method 3: Build up comment trees

        # xpath selector
        root_node = response.xpath('//*[@class="sitetable nestedlisting"]//*[contains(@class, "noncollapsed   comment ")]')
        for node in root_node:
            comment_layer1 = node.xpath('//*[@class="usertext-body may-blank-within md-container "]//text()').get()
            comment_layer2 = node.xpath('.//*[@class="child"]//*[@class="usertext-body may-blank-within md-container "]//text()').extract()

        # css selector
        root_node = response.css('.sitetable.nestedlisting .noncollapsed.comment')
        for node in root_node:
            comment_layer1 = node.css('.usertext-body.may-blank-within.md-container *::text').get()
            comment_layer2 = node.css('.child .usertext-body.may-blank-within.md-container *::text').extract()

        with open('../../crawldata/'+self.name+'.jsonl', 'a', encoding='utf-8') as f:
            json.dump({"title":title,"layer1":comment_layer1, "layer2":comment_layer2,}, f)
            f.write('\n')
