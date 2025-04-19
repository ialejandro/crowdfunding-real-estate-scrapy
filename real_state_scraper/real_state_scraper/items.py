# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RealEstateItem(scrapy.Item):
    """
    Item class for real estate crowdfunding projects.
    Standardizes the data structure across different platforms.
    """
    platform = scrapy.Field()  # Name of the platform (Urbanitae, Wecity, etc.)
    title = scrapy.Field()     # Project title
    city = scrapy.Field()      # City where the project is located
    region = scrapy.Field()    # Region/state/province
    address = scrapy.Field()   # Street address
    status = scrapy.Field()    # Current status of the project
    total_return = scrapy.Field()  # Expected return percentage
    term_months = scrapy.Field()   # Investment term in months
    business_model = scrapy.Field()  # Type of business model
    url = scrapy.Field()       # URL to the project page
