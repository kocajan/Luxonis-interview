# ------------------- Scrapy pipelines -------------------

import psycopg2


class PostgresPipeline:
    def __init__(self):
        # Connection details
        self.connection = None
        self.cursor = None
        self.table_name = None

    # Original methods
    def open_spider(self, spider):
        # Extract the database information from the spider (database_info is a dictionary)
        dbname = spider.database_info["dbname"]
        self.table_name = spider.database_info["table_name"]
        user = spider.database_info["user"]
        password = spider.database_info["password"]
        host = spider.database_info["host"]
        port = spider.database_info["port"]

        # Prepare the database for storing the scraped data
        self.process_database(dbname=dbname, user=user, password=password, host=host, port=port)

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

        print("- Spider closed.")


    # Helper methods
    def process_database(self, dbname: str, user: str, password: str, host: str, port: str) -> None:
        """
        Prepare the PostgreSQL database for storing the scraped data.

        Note: Using psycopg2 library [psycopg2.connect()] to connect to the database.
              More info: https://www.psycopg.org/

        :param dbname: name of the database
        :param user: username used to authenticate
        :param password: password used to authenticate
        :param host: database host address
        :param port: connection port number

        :return: None
        """
        # Create the database or connect to the existing one
        self.connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

        # Create the cursor
        self.cursor = self.connection.cursor()

        # Create the table if it does not exist
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} (name TEXT, image_url TEXT);")

        # Delete all the data from the table
        self.cursor.execute(f"DELETE FROM {self.table_name};")
