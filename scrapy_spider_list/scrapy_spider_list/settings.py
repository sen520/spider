# -*- coding: utf-8 -*-

# Scrapy settings for scrapy_spider_list project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'scrapy_spider_list'

SPIDER_MODULES = ['scrapy_spider_list.spiders']
NEWSPIDER_MODULE = 'scrapy_spider_list.spiders'

# ================= Dividing line =================
# MongoDB config
mongo = {
    # MONGODB HOST
    "MONGODB_HOST": "",
    # MONGODB PORT
    # "MONGODB_PORT": 27017,
    # DB NAME
    "MONGODB_DBNAME": "spider"
}

# ================= Dividing line =================
# SPLASH config
# SPLASH_URL = 'http://127.0.0.1:8050'
#
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy_splash.SplashCookiesMiddleware': 723,
#     'scrapy_splash.SplashMiddleware': 725,
#     'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
# }
#
# SPIDER_MIDDLEWARES = {
#     'scrapy_splash.SplashDeduplicateArgsMiddleware': 100
# }
#
# # Configure the filtering class used by message queuing
# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
#
# # Configure the classes that message queuing needs to use
# HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# ================= Dividing line =================
# Distributed spider
# REDIS_HOST = '192.168.1.44'
#
# REDIS_PORT = 6379
#
# # De-repeat filter
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
#
# # Using scrapy_redis 's scheduler instead of Scrapy's original scheduler
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
#
# # After the crawler stops, retain or clean up the request queue in the Redis and reassemble it
# # True: retention, False: cleanup, default is False
# SCHEDULER_PERSIST = True
#
# ITEM_PIPELINES = {
#     'scrapy_redis.pipelines.RedisPipeline': 400,
# }

# ================= Dividing line =================


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'scrapy_spider_list (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 5

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'scrapy_spider_list.middlewares.ScrapySpiderListSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'scrapy_spider_list.middlewares.ScrapySpiderListDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'scrapy_spider_list.pipelines.SpiderPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
