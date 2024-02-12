# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlingItem(scrapy.Item):
  # define the fields for your item here like:
  # name = scrapy.Field()
    pass


class QuoteItem(scrapy.Item):  # write by khanh
    quote = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()

class GPUItem(scrapy.Item):
    name = scrapy.Field()

class ChoTotLinkItem(scrapy.Item):
    link = scrapy.Field()

class ChoTotXeItem(scrapy.Item):
    link = scrapy.Field()

    date = scrapy.Field()  # thời gian đăng bài
    subject = scrapy.Field()  # tiêu đề
    body = scrapy.Field()  # mô tả chi tiết
    company_ad = scrapy.Field()  # khong biet
    price = scrapy.Field()  # gia
    images = scrapy.Field()  # links anh
    longitude = scrapy.Field()  # kinh do
    latitude = scrapy.Field()  # vi do
    protection_entitlement = scrapy.Field()  # khong biet
    detail_address = scrapy.Field()  # dia chi

    ward = scrapy.Field()  # phuong, thi xa, thi tran
    motorbikebrand = scrapy.Field()  # hang xe
    motorbikemodel = scrapy.Field()  # dong xe
    regdate = scrapy.Field()  # nam dang ky
    mileage_v2 = scrapy.Field()  # so km da di
    motorbiketype = scrapy.Field()  # loai xe
    motorbikecapacity = scrapy.Field()  # dung tinh xe
    area = scrapy.Field()  # quan, huyen
    region = scrapy.Field()  # tinh, thanh pho
    motorbikeorigin = scrapy.Field()  # xuat xu
