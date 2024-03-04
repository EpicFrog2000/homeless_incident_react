import psycopg2
import datetime

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname="oto_dom_db",
    user="postgres",
    password="haslo123",
    host="127.0.0.1",
    port="5432"
)

# Create a cursor object
cur = conn.cursor()

# Query to retrieve column names from information schema
cur.execute("""SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE';""")

# Fetch all column names
column_names = [row[0] for row in cur.fetchall()]

# Print column names
print("Column names:")
for name in column_names:
    print(name)

# Close the cursor and the connection
cur.close()
conn.close()