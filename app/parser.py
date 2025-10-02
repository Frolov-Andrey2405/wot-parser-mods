"""
This script parses mod information from the Russian website https://wotspeak.org.
It loads a list of mod page links from a JSON file, visits each link, extracts the mod title,
update date, patch version, download link, and EU/NA/ASIA server variant link (if available),
and saves the collected data to a results JSON file.
"""

import json
from typing import Dict, List, Optional
from urllib.parse import parse_qs, urlparse

import requests
from bs4 import BeautifulSoup


class LinkProcessor:
    """
    Class for processing links and extracting information from web pages.
    """

    def __init__(self, links_file: str, results_file: str):
        """
        Initialize the LinkProcessor object.
        """
        self.links_file = links_file
        self.results_file = results_file
        self.results: List[Dict[str, Optional[str]]] = []

    def load_links(self) -> List[str]:
        """
        Load a list of links from a file.
        """

        with open(self.links_file, "r", encoding="utf-8") as file:
            links_data = json.load(file)

        # Combine all links from categories
        links = []
        for category_links in links_data.values():
            links.extend(category_links)

        return links

    def process_link(self, link: str) -> None:
        """
        Process a single link: load the page and extract information.
        """
        print(f"Processing: {link}")
        response = requests.get(link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            title = self.extract_title(soup)
            update_date, patch_version = self.extract_info(soup)
            download_link = self.extract_download_link(soup)
            eu_na_asia_link = self.extract_eu_na_asia_link(soup)

            self.results.append(
                {
                    "Title": title,
                    "Update date": update_date,
                    "Patch version": patch_version,
                    "Download link": download_link,
                    "EU/NA/ASIA server variant": eu_na_asia_link,
                }
            )

    def extract_title(self, soup: BeautifulSoup) -> str:
        """
        Extract the page title.
        """
        return soup.find("header", class_="full-title").find("h1").get_text(strip=True)

    def extract_info(self, soup: BeautifulSoup) -> tuple[Optional[str], Optional[str]]:
        """
        Extract update date and patch version information.
        """
        update_date = None
        patch_version = None
        info_divs = soup.find_all("div", class_="full-info")
        for info_div in info_divs:
            if "Дата обновления:" in info_div.get_text():
                update_date = (
                    info_div.get_text(strip=True)
                    .replace("Дата обновления:", "")
                    .strip()
                )
            if "Актуально для патча:" in info_div.get_text():
                patch_version = info_div.find("label", class_="patch").get_text(
                    strip=True
                )
        return update_date, patch_version

    def extract_download_link(self, soup: BeautifulSoup) -> str:
        """
        Extract the download link.
        """
        download_link_element = soup.find(
            "a", class_="down_new", string="Перейти к скачиванию >>>"
        )
        download_link = download_link_element["href"]
        parsed_url = urlparse(download_link)
        return parse_qs(parsed_url.query)["xf"][0]

    def extract_eu_na_asia_link(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extract the link for EU/NA/ASIA servers or None if such a link is not found.
        """
        eu_na_asia_div = soup.find(
            "a", class_="down_new", string="Вариант для серверов EU/NA/ASIA >>>"
        )
        if eu_na_asia_div:
            eu_na_asia_link = eu_na_asia_div["href"]
            parsed_url = urlparse(eu_na_asia_link)
            return parse_qs(parsed_url.query)["xf"][0]
        return None

    def save_results(self) -> None:
        """
        Save the results to a JSON file.
        """
        with open(self.results_file, "w", encoding="utf-8") as file:
            json.dump(self.results, file, ensure_ascii=False, indent=4)

    def run(self) -> None:
        """
        Main method to start processing links and saving results.
        """
        links = self.load_links()
        for link in links:
            self.process_link(link)
        self.save_results()
        print("Parsing completed. Results saved to results.json.")


if __name__ == "__main__":
    processor = LinkProcessor("./json/links.json", "./json/results.json")
    processor.run()
