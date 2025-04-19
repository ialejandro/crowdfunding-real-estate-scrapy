import scrapy
import json
import logging
from real_state_scraper.items import RealEstateItem

class UrbanitaeOpenProjectsSpider(scrapy.Spider):
    """
    Spider for scraping open real estate projects from Urbanitae.

    This spider fetches data from Urbanitae's API and extracts information
    about open real estate crowdfunding projects.
    """
    name = "urbanitae"
    allowed_domains = ["urbanitae.com"]
    base_url = "https://urbanitae.com/api/projects/open"
    page_size = 20

    def start_requests(self):
        """
        Initiates the crawling process by generating the first request.
        """
        params = f"?page=0&size={self.page_size}&phases=POST_STUDY,FUNDING,IN_STUDY,PREFUNDING&sorts=priority:DESC,creationDate:DESC"
        yield scrapy.Request(
            url=self.base_url + params,
            callback=self.parse,
            meta={"page": 0},
            errback=self.handle_error
        )

    def parse(self, response):
        """
        Parses the JSON response from the API and extracts project data.

        Args:
            response: The response object containing the JSON data

        Yields:
            RealEstateItem: An item containing the extracted project data
        """
        try:
            data = json.loads(response.text)
            projects = data.get("elements", [])
            current_page = response.meta["page"]

            for project in projects:
                yield self._extract_project_data(project)

            # Check if there are more pages to scrape
            if len(projects) == self.page_size:
                next_page = current_page + 1
                next_url = (
                    f"{self.base_url}"
                    f"?page={next_page}&size={self.page_size}&phases=POST_STUDY,FUNDING,IN_STUDY,PREFUNDING"
                    f"&sorts=priority:DESC,creationDate:DESC"
                )
                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse,
                    meta={"page": next_page},
                    errback=self.handle_error
                )
        except json.JSONDecodeError:
            self.logger.error(f"Failed to parse JSON from response: {response.url}")
        except Exception as e:
            self.logger.error(f"Error parsing response from {response.url}: {str(e)}")

    def _extract_project_data(self, project):
        """
        Extracts and formats project data from the API response.

        Args:
            project: A dictionary containing project data

        Returns:
            RealEstateItem: An item containing the formatted project data
        """
        item = RealEstateItem()
        item["platform"] = "Urbanitae"
        item["title"] = project.get("name", "").strip()
        item["city"] = project.get("address", {}).get("city", "").strip()
        item["region"] = project.get("address", {}).get("state", "").strip()
        item["address"] = project.get("address", {}).get("streetName", "").strip()
        item["status"] = project.get("phase", "")
        item["total_return"] = project.get("fund", {}).get("totalNetProfitabilityToShow")
        item["term_months"] = project.get("details", {}).get("investmentPeriod")
        item["business_model"] = project.get("businessModel", "")
        item["url"] = f"https://urbanitae.com/es/proyectos/{project.get('id')}"
        return item

    def handle_error(self, failure):
        """
        Handles request errors.

        Args:
            failure: The failure object containing error information
        """
        self.logger.error(f"Request failed: {failure.request.url}")
