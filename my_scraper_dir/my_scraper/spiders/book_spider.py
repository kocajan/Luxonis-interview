import scrapy


# Print a current path
import os

current_path = os.getcwd()
print("Current Path:", current_path)

from my_scraper_dir.my_scraper.items import BooksItem


class BookSpider(scrapy.Spider):
    name = "book"
    start_urls = ["https://books.toscrape.com/"]

    def __init__(self, max_books: int, database_info: dict):
        """
        Initialize the spider.

        :param max_books:
        :param database_info:
        """
        super(BookSpider, self).__init__()
        # Set the counter of the collected books to 0 (TODO: use internal counter if possible)
        self.counter = 0

        # Save the info about the database
        self.database_info = database_info

        # Set the maximum number of books to collect
        self.max_books = max_books

    def parse(self, response):
        # Create the item to store the information
        item = BooksItem()

        # Get the information from the website
        for book in response.css("img"):

            # Check if the maximum number of books has been reached
            if self.counter >= self.max_books:
                break

            # Fill the item with the information
            item["name"] = book.attrib["alt"]
            item["image"] = book.attrib["src"]

            # Yield the information
            yield item

            # Increment the counter
            self.counter += 1

        # Get the next page
        next_page = response.css("li.next a::attr(href)").get()

        # Check if the next page is available and if so, go to the next page
        if next_page is not None and self.counter < self.max_books:
            yield response.follow(next_page, callback=self.parse)
