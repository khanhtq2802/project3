# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# import sqlite3
import mysql.connector


# Scraped data -> item containers -> json/csv files
# Scraped data -> item containers -> pipeline -> SQL/Mongo databases

# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter


# class CrawlingPipeline:
#     def process_item(self, item, spider):
#         return item

# class QuotesPipeline:   # write by khanh for sqlite3
#     def __init__(self):
#         self.connection = sqlite3.connect("motorbike.db")
#         self.cursor = self.connection.cursor()
#         self.create_table()
#
#     def create_table(self):
#         self.cursor.execute("""DROP TABLE IF EXISTS quotes""")
#         self.cursor.execute("""CREATE TABLE quotes(quote text, author text, tags text)""")
#
#     def store_quote(self, item):
#         self.cursor.execute("""INSERT INTO quotes VALUES (?,?,?)""", (
#         item["quote"],
#         item["author"],
#         str(item["tags"])))
#         self.connection.commit()
#
#     def process_item(self, item, spider):
#         if spider.name != 'quotes':
#             return
#         self.store_quote(item)

class QuotesPipeline:  # write by khanh for MySQL
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="khanh",
            password="tqk14131211",
            database="motorbike"
        )
        self.cursor = self.connection.cursor()
        # CREATE TABLE for quotes
        self.cursor.execute("""DROP TABLE IF EXISTS quotes""")
        self.cursor.execute("""CREATE TABLE quotes(quote text, author text, tags text)""")

    def store_quote(self, item):
        self.cursor.execute("""INSERT INTO quotes VALUES (%s,%s,%s)""", (
            item["quote"],
            item["author"],
            str(item["tags"])))
        self.connection.commit()

    def process_item(self, item, spider):
        self.store_quote(item)


class ChoTotLinkPipeline:  # write by khanh
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="khanh",
            password="tqk14131211",
            database="motorbike"
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS `chototlink` (
          `id` int NOT NULL AUTO_INCREMENT,
          `link` text,
          `available` tinyint(1) DEFAULT NULL,
          `crawled` tinyint(1) DEFAULT '0',
          PRIMARY KEY (`id`),
          UNIQUE KEY `link_unique` (`link`(255))
        ) ENGINE=InnoDB AUTO_INCREMENT=20011 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci''')
        self.connection.commit()

    def process_item(self, item, spider):
        self.cursor.execute("""INSERT INTO chototlink (link, available, crawled) VALUES (%s,%s,%s)""", (
            item["link"],
            True,
            False,))
        self.connection.commit()


class ChoTotXePipeline:  # write by khanh
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="khanh",
            password="tqk14131211",
            database="motorbike"
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS chototxe (
        id INT NOT NULL AUTO_INCREMENT,
        date TEXT,
        subject TEXT,
        body TEXT,
        company_ad BOOLEAN,
        price DECIMAL(11,0),
        longitude FLOAT,
        latitude FLOAT,
        protection_entitlement BOOLEAN,
        detail_address TEXT,
        ward TEXT,
        motorbikebrand TEXT,
        motorbikemodel TEXT,
        regdate YEAR,
        mileage_v2 DECIMAL(7,0),
        motorbiketype TEXT,
        motorbikecapacity TEXT,
        area TEXT,
        region TEXT,
        motorbikeorigin TEXT,
        PRIMARY KEY (id),
        FOREIGN KEY (id) REFERENCES chototlink(id));''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS chototimage (
        id INT,
        link TEXT,
        path TEXT DEFAULT NULL,
        UNIQUE KEY `link_unique` (`link`(255)),
        FOREIGN KEY (id) REFERENCES chototlink(id));''')
        self.connection.commit()

    def process_item(self, item, spider):
        try:
            # get id from chototlink
            self.cursor.execute("SELECT id FROM chototlink WHERE link = %s", (item['link'],))
            id = self.cursor.fetchone()[0]
            # add to chototxe
            chototxe_data = (
                id,
                item['date'],
                item['subject'],
                item['body'],
                item['company_ad'],
                item['price'],
                item['longitude'],
                item['latitude'],
                item['protection_entitlement'],
                item['detail_address'],
                item['ward'],
                item['motorbikebrand'],
                item['motorbikemodel'],
                item['regdate'],
                item['mileage_v2'],
                item['motorbiketype'],
                item['motorbikecapacity'],
                item['area'],
                item['region'],
                item['motorbikeorigin']
            )
            chototxe_query = ("INSERT INTO chototxe "
                              "(id, date, subject, body, company_ad, price, longitude, latitude, "
                              "protection_entitlement, detail_address, ward, motorbikebrand, motorbikemodel, "
                              "regdate, mileage_v2, motorbiketype, motorbikecapacity, area, region, motorbikeorigin) "
                              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            self.cursor.execute(chototxe_query, chototxe_data)
            # add to chototimage
            for linkImage in item['images']:
                chototimage_data = (
                    id,
                    linkImage)
                chototimage_query = "INSERT INTO chototimage (id, link) VALUES (%s, %s)"
                self.cursor.execute(chototimage_query, chototimage_data)
            # change value in chototlink
            chototlink_data = (
                True,
                id)
            chototlink_query = "UPDATE chototlink SET crawled = %s WHERE id = %s"
            self.cursor.execute(chototlink_query, chototlink_data)
            self.connection.commit()
        except mysql.connector.Error as e:
            print(f"Error inserting data into MySQL: {e}")
