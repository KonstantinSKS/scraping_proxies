import scrapy


class ProxiesItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    protocols = scrapy.Field()
