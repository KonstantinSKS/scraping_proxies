import scrapy
import base64

from proxies.items import ProxiesItem
from proxies.settings import PROXY_NAME, PROXY_ALLOWED_DOMAINS, PROXY_START_URLS


class ProxySpider(scrapy.Spider):
    name = PROXY_NAME
    allowed_domains = PROXY_ALLOWED_DOMAINS
    start_urls = [f'{PROXY_START_URLS}?page={page}' for page in range(1, 3)]
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "sec-fetch-mode": "navigate"
        }
    }
    total_count = 0
    max_items = 150

    def parse(self, response):
        rows = response.css('tbody tr')

        for row in rows:

            if self.total_count >= self.max_items:
                break

            ip_encoded = ip_encoded = row.css('td[data-ip]::attr(data-ip)').get()
            port_encoded = row.css('td[data-port]::attr(data-port)').get()
            proto_list = row.css('td:nth-child(4) a::text').getall()

            if ip_encoded and port_encoded:
                try:
                    ip = base64.b64decode(ip_encoded).decode('utf-8')
                    port = int(base64.b64decode(port_encoded).decode('utf-8'))
                    protocols = [proto.strip() for proto in proto_list if proto.strip()]

                    item = ProxiesItem(
                        ip=ip,
                        port=port,
                        protocols=protocols
                        )
                    self.total_count += 1
                    yield item

                except Exception as e:
                    self.logger.warning(f"String decoding error: {e}")
