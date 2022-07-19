import sqlite3

# Connecting to sqlite
db_file = '../db.sqlite3'
connection = sqlite3.connect(db_file)

# Create a cursor object
cursor = connection.cursor()

# execute an sqlite INSERT query
cursor.execute('''INSERT INTO app_photographer(name, number, approx_loc)
VALUES ('Nadia', 18, 'Illinois')''')

# execute an sqlite DELETE query
cursor.execute('''DELETE from app_photographer where name="Jeff"''')

# Commit your changes in the database
connection.commit()
print("Completed")

# Closing the connection
connection.close()
