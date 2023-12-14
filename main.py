import yaml

from scrapy.crawler import CrawlerProcess

from http_server import send_data_to_http
from database import load_data_from_database
from my_scraper_dir.my_scraper.spiders.book_spider import BookSpider


def main():
    # ----------- Extract the project configuration -----------
    # Load the configuration file
    config = yaml.safe_load(open("config.yaml"))

    # Extract the information from the configuration file
    hostname = config["database"]["hostname"]
    username = config["database"]["username"]
    password = config["database"]["password"]
    database = config["database"]["database_name"]
    port = config["database"]["port"]
    max_books = config["scraper"]["max_items"]
    http_ip = config["http"]["ip"]
    http_port = config["http"]["port"]
    target_url = config["scraper"]["url"]

    # ----------- Scrape the data from the website and store it in the database -----------
    # Create a crawler process
    process = CrawlerProcess()

    # Tell the process which spider to use
    database_info = {"hostname": hostname, "username": username, "password": password, "database": database}
    process.crawl(BookSpider, max_books=max_books, database_info=database_info)

    # Start the crawling process
    process.start()

    # ----------- Load the data from the database -----------
    # Load the data from the database (format: {"names": ["book_name1", ...], "images": ["image_url1", ..]})
    data = load_data_from_database(dbname=database, user=username, password=password, host=hostname, port=port)

    # Send the data to the website
    image_ext = data["image_urls"]
    image_urls = [target_url + ext for ext in image_ext]
    names = data["names"]
    send_data_to_http(http_ip, http_port, image_urls, names)


if __name__ == "__main__":
    main()
