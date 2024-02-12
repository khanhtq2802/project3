import scrapy
from ..items import ChoTotXeItem
import mysql.connector
import json


class ChototxeSpider(scrapy.Spider):
    name = "ChoTotXe"
    allowed_domains = ["xe.chotot.com"]
    custom_settings = {
        'ITEM_PIPELINES': {'crawling.pipelines.ChoTotXePipeline': 300},
        # 'SPIDER_MIDDLEWARES': {'crawling.middlewares.CrawlingSpiderMiddleware': 100},
        'DOWNLOADER_MIDDLEWARES': {"crawling.middlewares.ChoTotXeDownloaderMiddleware": 200}
    }
    # Establishing a connection to the database
    connection = mysql.connector.connect(
        host="localhost",
        user="khanh",
        password="tqk14131211",
        database="motorbike")
    # Creating a cursor object to execute SQL queries
    cursor = connection.cursor()
    # SELECT query to fetch links from 'chototlink' where 'crawled' is false
    select_query = "SELECT link FROM chototlink WHERE crawled = false and available = true"
    # Executing the SELECT query
    cursor.execute(select_query)
    # Fetching all the rows (links) returned by the query
    rows = cursor.fetchall()
    # Storing the links in the start_urls list
    start_urls = ['https://' + row[0] for row in rows]
    cursor.close()
    connection.close()

    def parse(self, response, **kwargs):
        item = ChoTotXeItem()
        item['link'] = response.url.replace('https://', '')
        
        data = response.css('script#__NEXT_DATA__').extract()[0]
        start_str = '"ad":{"ad_id":'
        start_index = data.find(start_str)
        end_str = ',"ad_params":'
        end_index = data.find(end_str)
        data = data[start_index:end_index]
        data = '{' + data + '}'

        DEFAULT_VALUE = None
        parsed_data = json.loads(data)
        # Trích xuất các giá trị từ 'ad'
        ad = parsed_data.get('ad', {})
        item['date'] = ad.get('date', DEFAULT_VALUE)
        item['subject'] = ad.get('subject', DEFAULT_VALUE)
        item['body'] = ad.get('body', DEFAULT_VALUE)
        item['company_ad'] = ad.get('company_ad', DEFAULT_VALUE)
        item['price'] = ad.get('price', DEFAULT_VALUE)
        item['images'] = ad.get('images', DEFAULT_VALUE)
        item['longitude'] = ad.get('longitude', DEFAULT_VALUE)
        item['latitude'] = ad.get('latitude', DEFAULT_VALUE)
        item['protection_entitlement'] = ad.get('protection_entitlement', DEFAULT_VALUE)
        item['detail_address'] = ad.get('shop', {}).get('address', DEFAULT_VALUE)

        # Trích xuất các giá trị từ 'parameters'
        parameters = parsed_data.get('parameters', {})
        item['ward'] = next((param['value'] for param in parameters if param['id'] == 'ward'), DEFAULT_VALUE)
        item['motorbikebrand'] = next((param['value'] for param in parameters if param['id'] == 'motorbikebrand'), DEFAULT_VALUE)
        item['motorbikemodel'] = next((param['value'] for param in parameters if param['id'] == 'motorbikemodel'), DEFAULT_VALUE)
        item['regdate'] = next((param['value'] for param in parameters if param['id'] == 'regdate'), DEFAULT_VALUE)
        item['mileage_v2'] = next((param['value'] for param in parameters if param['id'] == 'mileage_v2'), DEFAULT_VALUE)
        item['motorbiketype'] = next((param['value'] for param in parameters if param['id'] == 'motorbiketype'), DEFAULT_VALUE)
        item['motorbikecapacity'] = next((param['value'] for param in parameters if param['id'] == 'motorbikecapacity'), DEFAULT_VALUE)
        item['area'] = next((param['value'] for param in parameters if param['id'] == 'area'), DEFAULT_VALUE)
        item['region'] = next((param['value'] for param in parameters if param['id'] == 'region'), DEFAULT_VALUE)
        item['motorbikeorigin'] = next((param['value'] for param in parameters if param['id'] == 'motorbikeorigin'), DEFAULT_VALUE)

        yield item

        # filename = f"2.html"
        # from pathlib import Path
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")
