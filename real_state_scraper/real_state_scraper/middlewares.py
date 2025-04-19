# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import logging
from scrapy import signals
from itemadapter import is_item, ItemAdapter

class LoggingMiddleware:
    """
    Middleware for logging requests and responses.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        return middleware

    def process_request(self, request, spider):
        self.logger.debug(f"Processing request: {request.url}")
        return None

    def process_response(self, request, response, spider):
        self.logger.debug(f"Received response: {response.url} (Status: {response.status})")
        return response

    def spider_opened(self, spider):
        self.logger.info(f"Spider started: {spider.name}")
