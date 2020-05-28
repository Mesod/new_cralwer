# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class DigiatoSpider(scrapy.Spider):
    name = 'digiato'
    allowed_domains = ['digiato.com']
    start_urls = ['https://digiato.com/topic/mobile/']

    def parse(self, response):
        links = response.css('article a::attr(href)').getall()
        unique_links = set(links)
        # crawl each link here
    
        next_page = response.css('.next-page > a::attr(href)').get()
        if next_page:
            print(f'found next page. crawling {next_page}')
            yield Request(
                url=next_page,
                callback=self.parse,
            )

        yield list(unique_links)
