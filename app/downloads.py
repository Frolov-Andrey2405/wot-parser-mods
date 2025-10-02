"""
This script downloads mod files based on the results of parsing the website https://wotspeak.org.
It loads parsed mod data from a JSON file, creates a download directory if needed, and downloads each mod file
using the provided download links (preferring the EU/NA/ASIA server variant if available).
"""

import json
import os
from typing import Dict, List, Optional
from urllib.parse import unquote, urlparse

import requests


class ModDownloader:
    """
    Class for downloading mods based on parsing results.
    """

    def __init__(self, results_file: str, download_dir: str):
        """
        Initialize the ModDownloader object.
        """
        self.results_file = results_file
        self.download_dir = download_dir
        self.results: List[Dict[str, Optional[str]]] = []

    def load_results(self) -> None:
        """
        Load parsing results from a JSON file.
        """
        with open(self.results_file, "r", encoding="utf-8") as file:
            self.results = json.load(file)

    def create_download_directory(self) -> None:
        """
        Create the directory for saving downloaded files if it does not exist.
        """
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def download_file(self, url: str, destination: str) -> None:
        """
        Download a file from the given URL and save it to the specified destination.
        """
        response = requests.get(url, stream=True)
        with open(destination, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded: {destination}")

    def process_results(self) -> None:
        """
        Process parsing results and download files.
        """
        for result in self.results:
            download_link = result["Download link"]
            eu_na_asia_link = result["EU/NA/ASIA server variant"]

            url = eu_na_asia_link if eu_na_asia_link else download_link

            parsed_url = urlparse(url)
            file_name = unquote(os.path.basename(parsed_url.path))

            destination = os.path.join(self.download_dir, file_name)
            self.download_file(url, destination)

    def run(self) -> None:
        """
        Main method to start downloading mods.
        """
        self.load_results()
        self.create_download_directory()
        self.process_results()
        print("Download completed.")


if __name__ == "__main__":
    downloader = ModDownloader("./json/results.json", "download_mods")
    downloader.run()
