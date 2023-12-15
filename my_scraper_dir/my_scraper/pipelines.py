# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2


class PostgresPipeline:
    def __init__(self):
        # Connection details
        self.connection = None
        self.cursor = None
        self.table_name = None

    def open_spider(self, spider):
        host_name = spider.database_info["hostname"]
        user_name = spider.database_info["username"]
        password = spider.database_info["password"]
        database_name = spider.database_info["database"]
        self.table_name = spider.database_info["table_name"]

        self.process_database(host_name, user_name, password, database_name)

    def process_database(self, hostname, username, password, database):
        # Create the database or connect to the existing one
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

        # Create the cursor
        self.cursor = self.connection.cursor()

        # Create the table if it does not exist
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} (name TEXT, image_url TEXT);")

        # Delete all the data from the table
        self.cursor.execute(f"DELETE FROM {self.table_name};")

    def process_item(self, item, spider):
        # Define insert statement
        self.cursor.execute(f"INSERT INTO {self.table_name} (name, image_url) VALUES (%s, %s)", (item["name"],
                                                                                                 item["image_url"]))

        # Execute the statement
        self.connection.commit()

        return item

    def close_spider(self, spider):
        # Close the cursor
        self.cursor.close()

        # Close the connection
        self.connection.close()
