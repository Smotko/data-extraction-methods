import scrapy

SPIDER_NAME = 'delo'

class DeloSpider(scrapy.Spider):
    name = SPIDER_NAME
    save_files=False

    def start_requests(self):
        save_files_attr = getattr(self, 'save-files', None)
        if save_files_attr == 'True':
            self.save_files = True
            
        # TODO import from ../../../constants.py - URLS_DELO
        urls = [
            'https://www.delo.si/novice/',
            'https://www.delo.si/gospodarstvo/',
            'https://www.delo.si/lokalno/',
            'https://www.delo.si/mnenja/',
            'https://www.delo.si/sport/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if self.save_files:
            article = response.url.split("/")[-2]
            filename = f'./scraped-content/{SPIDER_NAME}-{article}.html'
            with open(filename, 'wb') as f:
                f.write(response.body)

        
        article_titles = self.get_all_titles(response)
        yield {'titles' : article_titles}

        # NOT IN USE - use when urls are specific articles
        #article_data_list = self.get_article_data_list(response)

    def get_all_titles(self, response):
        article_titles = response.xpath('//span[has-class("article_teaser__title_text")]/text()').getall()
        return self.get_trimmed_list(article_titles)

    def get_trimmed_list(self, l):
        result = []
        for el in l:
            el = el.replace('\n', '')
            el = el.strip()
            if el != '':
                result.append(el)

        return result

    # NOT IN USE - needs to scrape from different urls (www.delo.si)
    def get_article_data_list(self, response):
        title = response.xpath('//h1[has-class("article__title")]/text()').get()
        subtitle = response.xpath('//div[has-class("article__subtitle")]/text()').get()
        content = self.get_article_content(response)
        image_captions_list = response.xpath('//div[has-class("article__image-caption")]/text()').getall()
        return {
            'title': title,
            'subtitle': subtitle,
            'content': content,
            'image_captions_list': image_captions_list,
        }

    def get_article_content(self, response):
        content_list = response.xpath('//div[has-class("article__content")]/text()').getall()
        content = ''
        for el in content_list:
            el = el.replace('\n', '')
            el = el.strip()
            if el != '':
                content += el

        return content
