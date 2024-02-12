# write by khanh
import scrapy
from ..items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawling.pipelines.QuotesPipeline': 300,
        }
    }
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response, **kwargs):
        item = QuoteItem()
        for quote in response.css("div.quote"):
            item["quote"] = quote.css("span.text::text").get()
            item["author"] = quote.css("small.author::text").get()
            item["tags"] = quote.css("div.tags a.tag::text").getall()
            yield item

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
