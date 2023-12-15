import psycopg2


def load_data_from_database(dbname: str, table_name:str, user: str, password: str, host: str, port: str) -> dict:
    """
    Load data from the given PostgreSQL database.

    NOTE:   This function extracts only a specific format of data for a specific use case. Therefore, it is not
            a general function that can be used for any database.

    :param dbname: name of the database
    :param table_name: name of the table in the database
    :param user: username used to authenticate
    :param password: password used to authenticate
    :param host: database host address
    :param port: connection port number

    :return: dictionary with the data (format: {"names": ["book_name1", ...], "images": ["image_url1", ..]})
    """
    # Create the connection
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    # Create the cursor
    cur = conn.cursor()

    # Read the data
    cur.execute(f"SELECT * FROM {table_name};")

    # Extract data
    names = []
    image_urls = []
    for book in cur.fetchall():
        names.append(book[0])
        image_urls.append(book[1])

    # Close the cursor
    cur.close()

    # Close the connection
    conn.close()

    return {"names": names, "image_urls": image_urls}


if __name__ == "__main__":
    dbname = "books_db"
    user = "jan"
    password = "123456"
    host = "localhost"
    port = "5432"
    table_name = "books"

    data = load_data_from_database(dbname, table_name, user, password, host, port)

    print(data)
