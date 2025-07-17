import os

from dotenv import load_dotenv

load_dotenv()


BOT_NAME = "proxies"

SPIDER_MODULES = ["proxies.spiders"]
NEWSPIDER_MODULE = "proxies.spiders"

ADDONS = {}

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Spiders constants
PROXY_NAME = 'proxy'
PROXY_ALLOWED_DOMAINS = ['advanced.name']
PROXY_START_URLS = 'https://advanced.name/freeproxy'
PERSONAL_TOKEN = os.getenv("PERSONAL_TOKEN")

# Concurrency and throttling settings
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 1

# Configure item pipelines
ITEM_PIPELINES = {
   "proxies.pipelines.ProxiesPipeline": 300,
}

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"
