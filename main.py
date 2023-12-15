import yaml

from scrapy.crawler import CrawlerProcess

from http_server import send_data_to_http
from database import load_data_from_database, prepare_database
from my_scraper_dir.my_scraper.spiders.reality_spider import RealitySpider


def main():
    # ----------- Extract the project configuration -----------
    # Load the configuration file
    config = yaml.safe_load(open("config.yaml"))

    # Extract the information from the configuration file
    host = config["database"]["hostname"]
    user = config["database"]["username"]
    password = config["database"]["password"]
    dbname = config["database"]["database_name"]
    table_name = config["database"]["table_name"]
    port = config["database"]["port"]

    max_items = config["scraper"]["max_items"]
    obey_robots_txt = config["scraper"]["obey_robots_txt"]

    http_ip = config["http"]["ip"]
    http_port = config["http"]["port"]

    # ----------- Prepare the database -----------
    prepare_database(dbname=dbname, table_name=table_name, user=user, password=password, host=host, port=port)

    # ----------- Scrape the data from the website and store it in the database -----------
    # Prepare the settings for the crawler
    settings = {
        "BOT_NAME": "my_scraper",
        "SPIDER_MODULES": ["my_scraper_dir.my_scraper.spiders"],
        "NEWSPIDER_MODULE": "my_scraper_dir.my_scraper.spiders",
        "ROBOTSTXT_OBEY": obey_robots_txt,
        "ITEM_PIPELINES": {
            "my_scraper_dir.my_scraper.pipelines.PostgresPipeline": 300,
        }}

    # Create a crawler process
    process = CrawlerProcess(settings)

    # Tell the process which spider to use and pass the arguments
    database_info = {"dbname": dbname, "table_name": table_name, "user": user, "password": password, "host": host,
                     "port": port}
    process.crawl(RealitySpider, max_flats=max_items, database_info=database_info)

    # Start the crawling process
    process.start()

    # ----------- Load the data from the database -----------
    # Load the data from the database (format: {"names": ["item_name1", ...], "images": ["image_url1", ..]})
    data = load_data_from_database(dbname=dbname, table_name=table_name, user=user, password=password,
                                   host=host, port=port)

    # Send the data to the website
    image_urls = data["image_urls"]
    names = data["names"]
    send_data_to_http(http_ip, http_port, image_urls, names)


if __name__ == "__main__":
    main()
