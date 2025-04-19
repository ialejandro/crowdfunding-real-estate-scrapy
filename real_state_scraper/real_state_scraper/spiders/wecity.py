import scrapy
import json
import logging
from real_state_scraper.items import RealEstateItem

class WecityOpenProjectsSpider(scrapy.Spider):
    """
    Spider for scraping open real estate projects from Wecity.

    This spider fetches data from Wecity's API and extracts information
    about open real estate crowdfunding projects.
    """
    name = "wecity"
    allowed_domains = ["wecity.com"]
    start_urls = ["https://www.wecity.com/ajax/ajax.php?option=opportunities"]

    # States that indicate a project is not available
    EXCLUDED_STATES = {"finalizada", "reserva", "financiada"}

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
            projects = data.get("data", [])

            for project in projects:
                if self._is_valid_project(project):
                    yield self._extract_project_data(project)
        except json.JSONDecodeError:
            self.logger.error(f"Failed to parse JSON from response: {response.url}")
        except Exception as e:
            self.logger.error(f"Error parsing response from {response.url}: {str(e)}")

    def _is_valid_project(self, project):
        """
        Verifies if the project meets validation criteria.

        Args:
            project: A dictionary containing project data

        Returns:
            bool: True if the project is valid, False otherwise
        """
        state = (project.get("estado_txt") or "").strip().lower()
        url_path = project.get("url", "")
        title = project.get("titulo", "").strip()
        city = project.get("nombre_ciudad", "").strip()

        return (
            url_path and
            not any(excluded in state for excluded in self.EXCLUDED_STATES) and
            (title or city)
        )

    def _extract_project_data(self, project):
        """
        Extracts and formats project data from the API response.

        Args:
            project: A dictionary containing project data

        Returns:
            RealEstateItem: An item containing the formatted project data
        """
        url_path = project.get("url", "")

        item = RealEstateItem()
        item["platform"] = "Wecity"
        item["title"] = project.get("titulo", "").strip()
        item["city"] = project.get("nombre_ciudad", "").strip()
        item["region"] = project.get("provincia", "").strip()
        item["address"] = project.get("direccion", "").strip()
        item["status"] = project.get("estado_txt", "")
        item["total_return"] = project.get("rentabilidad_total")
        item["term_months"] = project.get("plazo_estimado")
        item["business_model"] = project.get("tipo_inversion_txt", "")
        item["url"] = f"https://www.wecity.com{url_path}"
        return item
