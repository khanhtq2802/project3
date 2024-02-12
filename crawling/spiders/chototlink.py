import scrapy
from ..items import ChoTotLinkItem


class ChototlinkSpider(scrapy.Spider):
    name = "chototlink"
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawling.pipelines.ChoTotLinkPipeline': 300,
        }
    }
    allowed_domains = ["xe.chotot.com"]

    start_urls = []
    url = "https://xe.chotot.com/mua-ban-xe-may?page="
    for i in range(1, 1001):
        start_urls.append(url + str(i))

    def parse(self, response, **kwargs):
        item = ChoTotLinkItem()
        links = response.css(".AdItem_big__70CJq a::attr(href)").extract()
        for link in links:
            item["link"] = 'xe.chotot.com' + link
            yield item
