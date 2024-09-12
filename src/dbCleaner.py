import sqlite3
from datetime import datetime


def remove_duplicates_on_date(database_path, table_name, column_name, date_column):
    last_entry_id = get_highest_id(database_path)
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        cursor.execute(
            f"SELECT {column_name}, date({date_column}), COUNT(*) FROM {table_name} WHERE id > ? GROUP BY {column_name}, date({date_column}) HAVING COUNT(*) > 1",
            (last_entry_id,),
        )
        duplicates = cursor.fetchall()

        for duplicate in duplicates:
            href_value, date_value, count = duplicate
            print(
                f"Removing duplicates for {column_name}: {href_value} on {date_value}, {count} rows removed."
            )

        cursor.execute(
            f"CREATE TABLE temp_table AS SELECT * FROM {table_name} WHERE id <= ? GROUP BY {column_name}, date({date_column})",
            (last_entry_id,),
        )
        cursor.execute(f"DROP TABLE {table_name}")
        cursor.execute(f"ALTER TABLE temp_table RENAME TO {table_name}")
        connection.commit()

        print(
            f"Duplicates removed successfully from {column_name} column in {table_name} table after id {last_entry_id}."
        )
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        connection.close()


def create_last_checked_table(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS LastCheckedEntry (
            id INTEGER PRIMARY KEY,
            table_name TEXT,
            last_entry_id INTEGER,
            last_checked_timestamp DATETIME
        )
    """
    )
    connection.commit()


def insert_initial_record(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO LastCheckedEntry (table_name, last_entry_id, last_checked_timestamp)
        VALUES (?, 0, ?)
    """,
        (table_name, datetime.now()),
    )
    connection.commit()


def update_last_checked_record(connection, table_name, last_entry_id):
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE LastCheckedEntry
        SET last_entry_id = ?, last_checked_timestamp = ?
        WHERE id = (SELECT id FROM LastCheckedEntry WHERE table_name = ? ORDER BY last_checked_timestamp DESC LIMIT 1)
    """,
        (last_entry_id, datetime.now(), table_name),
    )
    connection.commit()


def get_highest_id(database_path, table_name="WordAndUrl"):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        cursor.execute(f"SELECT MAX(id) FROM {table_name}")
        result = cursor.fetchone()

        return result[0] if result[0] is not None else None

    except sqlite3.Error as e:
        print(f"Error: {e}")
        return None

    finally:
        connection.close()


def clean_last_update():
    database_path = "your_database.db"
    table_name = "WordAndUrl"

    connection = sqlite3.connect(database_path)

    create_last_checked_table(connection)
    insert_initial_record(connection, table_name)

    last_entry_id_checked = get_highest_id(database_path)

    update_last_checked_record(connection, table_name, last_entry_id_checked)

    connection.close()

    if last_entry_id_checked is not None:
        print(f"The highest id in the WordAndUrl table is: {last_entry_id_checked}")
    else:
        print("Failed to retrieve the highest id.")


def reorganize_ids(database_path, table_name="WordAndUrl"):
    database_path = "your_database.db"
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS temp_table AS
            SELECT *, ROW_NUMBER() OVER (ORDER BY id) AS new_id
            FROM {table_name}
        """
        )

        cursor.execute(f"DELETE FROM {table_name}")
        cursor.execute(
            f"""
            INSERT INTO {table_name} (id, pagename, tag_name, search_word, href, timestamp)
            SELECT new_id, pagename, tag_name, search_word, href, timestamp
            FROM temp_table
        """
        )

        cursor.execute("DROP TABLE temp_table")
        connection.commit()

        print(f"IDs in {table_name} table have been reorganized.")

    except sqlite3.Error as e:
        print(f"Error: {e}")
        connection.rollback()

    finally:
        connection.close()

def evaluateArticlesTable():
# def insert_article(connection, title, subtitle, text):
    db_path = "your_database.db"
    connection = sqlite3.connect(db_path)

    cursor = connection.cursor()
    cursor.execute("PRAGMA table_info(articles)")
    columns = cursor.fetchall()

    # Extract column names
    column_names = [column[1] for column in columns]

    # If 'search_words' column doesn't exist, add it
    if 'search_words' not in column_names:
        cursor.execute("ALTER TABLE articles ADD COLUMN search_words TEXT")
        print("Column 'search_words' added.")
    else:
        print("Column 'search_words' already exists.")

    searchWords = []

    # get serarchWords.json
    # get companies.json

    # get articles text
    # search for search words
    # append hits to searchWords list
    cursor.execute(
        """
        INSERT INTO articles (
            search_words
            )
        VALUES (?, )
        """,
        ( searchWords),
    )
    connection.commit()
    connection.close()