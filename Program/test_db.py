import sqlite3

def test_database(db_name):
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        print(f"Connected to database: {db_name}")

        # Check if the table 'file_table' exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='file_table';")
        table_exists = cursor.fetchone()

        if table_exists:
            print("The 'file_table' exists.")
        else:
            print("Error: 'file_table' does not exist.")
            return
        
        # Check the structure of the table
        print("Checking the table structure (columns and types):")
        cursor.execute("PRAGMA table_info(file_table);")
        columns = cursor.fetchall()
        if columns:
            for col in columns:
                print(f"Column Name: {col[1]}, Type: {col[2]}")
        else:
            print("Error: Unable to fetch table structure.")
            return

        # Query the table to find rows where delete_flag = 0
        cursor.execute("SELECT name FROM file_table WHERE delete_flag = 0;")
        rows = cursor.fetchall()

        if rows:
            print("Rows with delete_flag = 0:")
            for row in rows:
                print(f"File: {row[0]}")
        else:
            print("No rows found with delete_flag = 0.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        # Close the database connection
        connection.close()
        print("Connection closed.")

# Replace 'example.db' with the path to your SQLite database file
test_database("data/user.db")
