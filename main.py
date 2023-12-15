import yaml

from scrapy.crawler import CrawlerProcess

from http_server import send_data_to_http
from database import load_data_from_database, prepare_database
from my_scraper_dir.my_scraper.spiders.book_spider import BookSpider
from my_scraper_dir.my_scraper.spiders.reality_spider import RealitySpider


def main():
    # ----------- Extract the project configuration -----------
    # Load the configuration file
    config = yaml.safe_load(open("config.yaml"))

    # Extract the information from the configuration file
    hostname = config["database"]["hostname"]
    username = config["database"]["username"]
    password = config["database"]["password"]
    database = config["database"]["database_name"]
    table = config["database"]["table_name"]
    port = config["database"]["port"]
    max_items = config["scraper"]["max_items"]
    http_ip = config["http"]["ip"]
    http_port = config["http"]["port"]
    target_url = config["scraper"]["url"]

    # ----------- Prepare the database -----------
    prepare_database(dbname=database, table_name=table, user=username, password=password, host=hostname, port=port)

    # ----------- Scrape the data from the website and store it in the database -----------
    # Prepare the settings for the crawler
    settings = {
        "BOT_NAME": "my_scraper",
        "SPIDER_MODULES": ["my_scraper_dir.my_scraper.spiders"],
        "NEWSPIDER_MODULE": "my_scraper_dir.my_scraper.spiders",
        "ROBOTSTXT_OBEY": False,
        "ITEM_PIPELINES": {
            "my_scraper_dir.my_scraper.pipelines.PostgresPipeline": 300,
        }}

    # Create a crawler process
    process = CrawlerProcess(settings)

    # Tell the process which spider to use and pass the arguments
    database_info = {"hostname": hostname, "username": username, "password": password, "database": database,
                     "table_name": table}
    process.crawl(RealitySpider, max_flats=max_items, database_info=database_info)
    # process.crawl(BookSpider, max_books=max_items, database_info=database_info)

    # Start the crawling process
    process.start()

    # ----------- Load the data from the database -----------
    # Load the data from the database (format: {"names": ["item_name1", ...], "images": ["image_url1", ..]})
    data = load_data_from_database(dbname=database, table_name=table, user=username, password=password, host=hostname,
                                   port=port)
    print("LOADED: ", len(data["names"]))

    # Send the data to the website
    image_ext = data["image_urls"]
    # image_urls = [target_url + ext for ext in image_ext]
    image_urls = image_ext
    names = data["names"]
    send_data_to_http(http_ip, http_port, image_urls, names)


if __name__ == "__main__":
    main()
