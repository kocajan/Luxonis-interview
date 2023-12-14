import psycopg2

conn = psycopg2.connect(dbname="books_db", user="jan", password="123456", host="localhost", port="5432")

cur = conn.cursor()

# Read the data
cur.execute("SELECT * FROM books")

# Print the data
counter = 0
for book in cur.fetchall():
    print(book)
    counter += 1

print(f"Number of books: {counter}")

# Close the cursor
cur.close()

# Close the connection
conn.close()
