# write by khanh
import scrapy
from scrapy import FormRequest
from scrapy.utils.response import open_in_browser


class LogquotesSpider(scrapy.Spider):
    name = "LogQuotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/login"]

    def parse(self, response, **kwargs):
        token = response.css('form input::attr(value)').extract_first()
        # noinspection PyTypeChecker
        return FormRequest.from_response(
            response,
            formdata={
                'csrf_token': token,
                'username': 'khanh.tq2802@outlook.com',
                'password': 'password
                
                '},
            callback=self.start_crawling)

    def start_crawling(self, response):
        open_in_browser(response)
        for quote in response.css("div.quote"):
            yield {
                "quote": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.start_crawling)
