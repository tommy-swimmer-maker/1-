import sqlite3
from msg_handling import MsgHandling
import flet as ft

# connect to database
conn = sqlite3.connect("erfan.db", check_same_thread=False)


def create_table():
    # Create a table named 'paziresh'
    conn.execute("""
        CREATE TABLE IF NOT EXISTS paziresh (
            id INTEGER PRIMARY KEY,
            name TEXT,
            date Numeric,
            khadamat TEXT,
            price INT
        )
    """)


def save_data(page: ft.Page, name, date, khadamat, price):
    msg = MsgHandling(page)
    conn = sqlite3.connect("erfan.db", check_same_thread=False)
    try:
        # Insert data into the 'paziresh' table
        conn.execute("INSERT INTO paziresh VALUES (NULL, ?, ?, ?, ?)", (name, date, khadamat, price))
        conn.commit()
    except sqlite3.Error as err:
        msg.error_dialog(err.args)
    # Don't forget to close the connection when done
    conn.close()


def read_data(page: ft.Page, start_date=None, end_date=None):
    conn = sqlite3.connect("erfan.db", check_same_thread=False)
    cursor = conn.cursor()

    # define error handler
    msg = MsgHandling(page)

    try:
        if start_date and end_date:
            # Retrieve all rows from the 'paziresh' table
            cursor.execute("SELECT * FROM paziresh WHERE ? <= date and date <= ? ORDER BY DATE",
                           (start_date, end_date))
        else:
            cursor.execute("SELECT * FROM paziresh")

        rows = cursor.fetchall()
        length = len(rows)
        id, name, date, khadamat, price = zip(*rows)
        return length, id, name, date, khadamat, price

    except sqlite3.Error as err:
        msg.error_dialog(err.args)
        return 0, [], [], [], []

    # close cursor and connection
    finally:
        cursor.close()
        conn.close()


# Create the table (if not already created)
create_table()
