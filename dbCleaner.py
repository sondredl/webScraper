import sqlite3

def remove_duplicates(database_path, table_name, column_name):
    # Connect to the SQLite database
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        # Select and print information about each duplicated row before removal
        cursor.execute(f"SELECT {column_name}, COUNT(*) FROM {table_name} GROUP BY {column_name} HAVING COUNT(*) > 1")
        duplicates = cursor.fetchall()

        for duplicate in duplicates:
            href_value, count = duplicate
            print(f"Removing duplicates for {column_name}: {href_value}, {count} rows removed.")

        # Create a temporary table with distinct values based on the href column
        cursor.execute(f"CREATE TABLE temp_table AS SELECT * FROM {table_name} GROUP BY {column_name}")

        # Drop the original table
        cursor.execute(f"DROP TABLE {table_name}")

        # Rename the temporary table to the original table name
        cursor.execute(f"ALTER TABLE temp_table RENAME TO {table_name}")

        # Commit the changes
        connection.commit()

        print(f"Duplicates removed successfully from {column_name} column in {table_name} table.")
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        # Close the connection
        connection.close()
