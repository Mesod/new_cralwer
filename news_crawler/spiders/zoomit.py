# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request



class ZoomitSpider(scrapy.Spider):
    name = 'zoomit'
    allowed_domains = ['zoomit.ir']
    start_urls = [
        'https://www.zoomit.ir/category/mobile/',
    ]
    labels = ['mobile', 'business', 'game', 'science']

    def parse(self, response):
        label = self.find_label(response.url)
        articles = response.css('.catlist__post-title')
        unique_links = []
        for article in articles:
            link = article.css('a::attr(href)').get()
            title = article.css('a::text').get()
            if title is not ' ' and link not in unique_links:
                unique_links.append(link)
                yield {
                    'title': title,
                    'url': link,
                    'label': label,
                    'source': self.name,
                }

        next_page = response.css(
            '.pagination > li:nth-child(7) > a:nth-child(1) > .icon-angle-left')\
            .get()
        if next_page:
            next_page_url = response.css(
                '.pagination > li:nth-child(7) > a:nth-child(1)::attr(href)')\
                .get()
            print(f'found next page. crawling {next_page_url}')
            yield Request(
                url=next_page_url,
                callback=self.parse,
            )

    def find_label(self, url):
        for label in self.labels:
            if label in url:
                return label
        return 'unknown'
