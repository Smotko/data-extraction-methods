import scrapy

spider_name = 'zurnal'

class ZurnalSpider(scrapy.Spider):
    name = spider_name
    save_files=False

    def start_requests(self):
        save_files_attr = getattr(self, 'save-files', None)
        if save_files_attr == 'True':
            self.save_files = True
            
        # TODO import from ../../../constants.py - URLS_ZURNAL
        urls = [
            'https://www.zurnal24.si/',
            'https://www.zurnal24.si/slovenija',
            'https://www.zurnal24.si/svet',
            'https://www.zurnal24.si/sport',
            'https://www.zurnal24.si/magazin',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if self.save_files:
            article = response.url.split("/")[-2]
            filename = f'./scraped-content/{spider_name}-{article}.html'
            with open(filename, 'wb') as f:
                f.write(response.body)

        
        article_titles = self.get_all_titles(response)
        yield {'titles' : article_titles}


    def get_all_titles(self, response):
        article_titles = response.xpath('//span[has-class("card__title_highlight")]/text()').getall()
        return self.get_trimmed_list(article_titles)

    def get_trimmed_list(self, l):
        result = []
        for el in l:
            el = el.replace('\n', '')
            el = el.strip()
            if el != '':
                result.append(el)

        return result