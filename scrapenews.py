import hashlib
import scrapy
import os
import csv
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
dump_location = os.path.expanduser ("~/g/news-scrape")
log_location = os.path.expanduser("~/g/news-scrape-index.log")

class MyNewsSpider(scrapy.Spider):
    name = "mynews"
    allowed_domains = ["news.yahoo.com"]
    start_urls = [
        "https://www.yahoo.com/news/us/",
    ]
    async def parse(self, response, **kwargs):
        file_name = hashlib.sha256(response.body).hexdigest()
        if not any((response.url.startswith(base_url) for base_url in self.start_urls)):
            self.log(f"Skipping {response.url}")
            return
        if not response.headers["Content-Type"].decode().startswith("text/html"):
            self.log(f"Skipped non-html document: {response.url}")
            return

        with open(os.path.join(dump_location, file_name), "wt") as f, open(log_location, "at", newline="") as f_log:
            csv_writer = csv.writer(f_log)
            csv_writer.writerow([response.url, file_name])
            f.write(response.text)
        self.log(f"Saved file{file_name}")

        for link in LinkExtractor().extract_links(response):
            yield response.follow(link, callback=self.parse)

process = CrawlerProcess()

process.crawl(MyNewsSpider)
process.start()



