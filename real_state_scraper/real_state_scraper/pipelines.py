# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from itemadapter import ItemAdapter

class RealEstateScraperPipeline:
    """
    Pipeline for processing real estate items.

    This pipeline performs data cleaning and validation on the scraped items.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def process_item(self, item, spider):
        """
        Process each item before it is exported.

        Args:
            item: The scraped item
            spider: The spider that scraped the item

        Returns:
            The processed item
        """
        adapter = ItemAdapter(item)

        # Clean string fields
        for field in ['title', 'city', 'region', 'address', 'status', 'business_model']:
            if field in adapter:
                value = adapter.get(field)
                if isinstance(value, str):
                    adapter[field] = value.strip()

        # Clean numeric fields
        for field in ['total_return', 'term_months']:
            if field in adapter:
                value = adapter.get(field)
                if value is not None:
                    try:
                        # Convert to float for total_return, int for term_months
                        if field == 'total_return':
                            adapter[field] = float(value)
                        else:
                            adapter[field] = int(value)
                    except (ValueError, TypeError):
                        self.logger.warning(f"Invalid {field} value: {value} for item {adapter.get('url')}")
                        adapter[field] = None

        # Validate URL
        if 'url' in adapter and not adapter['url']:
            self.logger.warning(f"Missing URL for item: {adapter.get('title')}")

        return item
