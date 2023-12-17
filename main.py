import yaml

from scrapy.crawler import CrawlerProcess

from src.http_server import send_data_to_http
from src.database import load_data_from_database, prepare_database
from src.my_scraper_dir.my_scraper.spiders.reality_spider import RealitySpider


def main():
    print(" ------------------- *INTERVIEW PROJECT* ------------------- ")
    print(" -> Jan Koca")
    print(" -> 2023-12\n")
    # ----------- Extract the project configuration -----------
    # Load the configuration file
    config = yaml.safe_load(open("cfg/config.yaml"))

    # Extract the information from the configuration file
    host = config["database"]["hostname"]
    user = config["database"]["username"]
    password = config["database"]["password"]
    dbname = config["database"]["database_name"]
    table_name = config["database"]["table_name"]
    port = config["database"]["port"]

    max_items = config["scraper"]["max_items"]
    obey_robots_txt = config["scraper"]["obey_robots_txt"]

    http_mapped_ip = config["http"]["local_ip"]
    http_ip = config["http"]["docker_ip"]
    http_port = config["http"]["port"]

    # ----------- Prepare the database -----------
    print("- Preparing the database...")
    prepare_database(dbname=dbname, table_name=table_name, user=user, password=password, host=host, port=port)

    # ----------- Scrape the data from the website and store it in the database -----------
    print("- Scraping the data from the website and storing it in the database...")
    # Prepare the settings for the crawler
    settings = {
        "BOT_NAME": "my_scraper",
        "SPIDER_MODULES": ["src.my_scraper_dir.my_scraper.spiders"],
        "NEWSPIDER_MODULE": "src.my_scraper_dir.my_scraper.spiders",
        "ROBOTSTXT_OBEY": obey_robots_txt,
        "ITEM_PIPELINES": {
            "src.my_scraper_dir.my_scraper.pipelines.PostgresPipeline": 300},
        "LOG_ENABLED": False
    }

    # Create a crawler process
    process = CrawlerProcess(settings)

    # Tell the process which spider to use and pass the arguments
    database_info = {"dbname": dbname, "table_name": table_name, "user": user, "password": password, "host": host,
                     "port": port}
    print(" -> Start scraping...")
    process.crawl(RealitySpider, max_flats=max_items, database_info=database_info)

    # Start the crawling process
    process.start()

    # ----------- Load the data from the database -----------
    print("- Loading the data from the database...")
    # Load the data from the database (format: {"names": ["item_name1", ...], "images": ["image_url1", ..]})
    data = load_data_from_database(dbname=dbname, table_name=table_name, user=user, password=password,
                                   host=host, port=port)

    # ----------- Send the data to the website -----------
    print("- Sending the data to the website...")
    image_urls = data["image_urls"]
    names = data["names"]
    send_data_to_http(http_ip, http_port, image_urls, names, mapped_ip=http_mapped_ip)


if __name__ == "__main__":
    main()
