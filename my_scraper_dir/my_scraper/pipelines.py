# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2


class BooksPipeline:
    def process_item(self, item, spider):
        return item


class PostgresPipeline:
    def __init__(self):
        # Connection details
        hostname = "localhost"
        username = "jan"
        password = "123456"
        database = "books_db"

        # Create the database or connect to the existing one
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

        # Create the cursor
        self.cursor = self.connection.cursor()

        # Create the table if it does not exist
        self.cursor.execute("CREATE TABLE IF NOT EXISTS books (name TEXT, image TEXT)")

        # Delete all the data from the table
        self.cursor.execute("DELETE FROM books")

    def process_item(self, item, spider):
        # Define insert statement
        self.cursor.execute(f"INSERT INTO books (name, image) VALUES (%s, %s)", (item["name"], item["image"]))

        # Execute the statement
        self.connection.commit()

        return item

    def close_spider(self, spider):
        # Close the cursor
        self.cursor.close()

        # Close the connection
        self.connection.close()
