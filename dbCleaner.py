import sqlite3
from datetime import datetime

def remove_duplicates_on_date(database_path, table_name, column_name, date_column):
    # Connect to the SQLite database
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        # Select and print information about each duplicated row before removal
        cursor.execute(f"SELECT {column_name}, date({date_column}), COUNT(*) FROM {table_name} GROUP BY {column_name}, date({date_column}) HAVING COUNT(*) > 1")
        duplicates = cursor.fetchall()

        for duplicate in duplicates:
            href_value, date_value, count = duplicate
            print(f"Removing duplicates for {column_name}: {href_value} on {date_value}, {count} rows removed.")

        # Create a temporary table with distinct values based on the href column and date
        cursor.execute(f"CREATE TABLE temp_table AS SELECT * FROM {table_name} GROUP BY {column_name}, date({date_column})")

        # Drop the original table
        cursor.execute(f"DROP TABLE {table_name}")

        # Rename the temporary table to the original table name
        cursor.execute(f"ALTER TABLE temp_table RENAME TO {table_name}")

        # Commit the changes
        connection.commit()

        print(f"Duplicates removed successfully from {column_name} column in {table_name} table on the same date.")
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        # Close the connection
        connection.close()


def create_last_checked_table(connection):
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS LastCheckedEntry (
            id INTEGER PRIMARY KEY,
            table_name TEXT,
            last_entry_id INTEGER,
            last_checked_timestamp DATETIME
        )
    ''')
    connection.commit()

def insert_initial_record(connection, table_name):
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO LastCheckedEntry (table_name, last_entry_id, last_checked_timestamp)
        VALUES (?, 0, ?)
    ''', (table_name, datetime.now()))
    connection.commit()

# def update_last_checked_record(connection, table_name, last_entry_id):
#     cursor = connection.cursor()
#     cursor.execute('''
#         UPDATE LastCheckedEntry
#         SET last_entry_id = ?, last_checked_timestamp = ?
#         WHERE table_name = ?
#     ''', (last_entry_id, datetime.now(), table_name))
#     connection.commit()

def update_last_checked_record(connection, table_name, last_entry_id):
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE LastCheckedEntry
        SET last_entry_id = ?, last_checked_timestamp = ?
        WHERE id = (SELECT id FROM LastCheckedEntry WHERE table_name = ? ORDER BY last_checked_timestamp DESC LIMIT 1)
    ''', (last_entry_id, datetime.now(), table_name))
    connection.commit()

def get_highest_id(database_path, table_name='WordAndUrl'):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        # Execute a query to get the highest value in the id column
        cursor.execute(f"SELECT MAX(id) FROM {table_name}")
        result = cursor.fetchone()

        # If there are records in the table, return the highest id; otherwise, return None
        return result[0] if result[0] is not None else None

    except sqlite3.Error as e:
        print(f"Error: {e}")
        return None

    finally:
        connection.close()


def clean_last_update():
    database_path = 'your_database.db'
    table_name = 'WordAndUrl'

    connection = sqlite3.connect(database_path)

    # Create the LastCheckedEntry table if it doesn't exist
    create_last_checked_table(connection)

    # Insert an initial record for WordAndUrl
    insert_initial_record(connection, table_name)

    # Simulate checking for duplicates in WordAndUrl
    # Replace this with your actual logic to check for duplicates
    last_entry_id_checked = get_highest_id(database_path)

    # Update the LastCheckedEntry record after checking for duplicates
    update_last_checked_record(connection, table_name, last_entry_id_checked)

    # Close the connection
    connection.close()

    if last_entry_id_checked is not None:
        print(f"The highest id in the WordAndUrl table is: {last_entry_id_checked}")
    else:
        print("Failed to retrieve the highest id.")

# import sqlite3

def reorganize_ids(database_path, table_name='WordAndUrl'):
    # Replace 'your_database.db' with the actual path to your SQLite database file
    database_path = 'your_database.db'
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        # Create a temporary table with the desired order
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS temp_table AS
            SELECT *, ROW_NUMBER() OVER (ORDER BY id) AS new_id
            FROM {table_name}
        ''')

        # Clear the original table
        cursor.execute(f'DELETE FROM {table_name}')

        # Update the original table with the new order
        cursor.execute(f'''
            INSERT INTO {table_name} (id, pagename, tag_name, search_word, href, timestamp)
            SELECT new_id, pagename, tag_name, search_word, href, timestamp
            FROM temp_table
        ''')

        # Drop the temporary table
        cursor.execute('DROP TABLE temp_table')

        # Commit the changes
        connection.commit()

        print(f"IDs in {table_name} table have been reorganized.")
    
    except sqlite3.Error as e:
        print(f"Error: {e}")
        connection.rollback()

    finally:
        connection.close()


# Call the function to reorganize the IDs in the WordAndUrl table
# reorganize_ids(database_path)
