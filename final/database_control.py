import sqlite3
import pandas as pd
import datetime
from decimal import Decimal
from tkinter import messagebox
from hashlib import sha256

def create_tables():
    conn = sqlite3.connect('transactions.db')

    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        userid INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userid INTEGER NOT NULL,
        date TEXT NOT NULL,
        description TEXT NOT NULL,
        category TEXT NOT NULL DEFAULT "MISCELLANEOUS",
        type TEXT NOT NULL,
        amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
        FOREIGN KEY(userid) REFERENCES users(userid)
    )
    """)

    conn.commit()
    conn.close()

def format_balance(amount):
    """
    Formats the balance according to the Indian numbering system with paise in decimal.
    Example:
    - 1250.3 -> "1.25 K.30"
    - 1030.05 -> "1.03 K.05"
    - 1000.0 -> "1 K.00"
    """
    rupees = int(amount)
    paise = round((amount - rupees) * 100)

    if amount >= 1_00_00_00_000:  # 1000 Cr
        formatted_amount = f"{rupees / 1_00_00_00_000:.2f}K Cr.{paise:02d}"
    elif amount >= 1_00_00_000:  # 1 Cr to <1000 Cr
        formatted_amount = f"{rupees / 1_00_00_000:.2f} Cr.{paise:02d}"
    elif amount >= 1_00_000:  # 1 Lakh to <1 Cr
        formatted_amount = f"{rupees / 1_00_000:.2f} L.{paise:02d}"
    elif amount >= 1_000:  # 1 Thousand to <1 Lakh
        formatted_amount = f"{rupees / 1_000:.2f} K.{paise:02d}"
    else:  # Below Thousand, show the full amount with paise
        formatted_amount = f"₹{rupees}.{paise:02d}"

    return formatted_amount


def update_balance(app_instance):
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()

    userid = app_instance.user_id
    
    c.execute("SELECT SUM(amount) FROM transactions WHERE userid=? AND type='deposit'", (userid, ))
    total_credited = c.fetchone()[0] or 0

    c.execute("SELECT SUM(amount) FROM transactions WHERE userid=? AND type='withdraw'", (userid, ))
    total_debited = c.fetchone()[0] or 0

    balance = format_balance(total_credited - total_debited)

    app_instance.amount_label.configure(text=balance)

def add_transactions(userid, date, description, category, type_, amount):
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute('INSERT INTO transactions (userid, date, description, category, type, amount) VALUES (?, ?, ?, ?, ?, ?)', (userid, date, description, category, type_, str(amount), ))
    conn.commit()
    conn.close()

def add_user(username, email, password):
    """Adds a new user to the database with a hashed password."""
    hashed_password = hash_password(password)  # Hash the password before storing
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, hashed_password))
    conn.commit()
    conn.close()

def hash_password(password):
    """Hashes a password using SHA-256."""
    return sha256(password.encode()).hexdigest()

def verify_user(username, password):
    """
    Verifies a user's credentials by comparing the hashed input password with the stored hashed password.

    Args:
        username (str): The username of the user.
        password (str): The plaintext password input by the user.

    Returns:
        str: "Success" if credentials are correct,
             "IncorrectPassword" if the password is wrong,
             "UserNotFound" if the username does not exist.
    """
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    
    if result:
        stored_password_hash = result[0]
        input_password_hash = hash_password(password)
        if input_password_hash == stored_password_hash:
            return "Success"
        else:
            return "IncorrectPassword"
    else:
        return "UserNotFound"


def get_userid(username):
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute('SELECT userid FROM users WHERE username = ?', (username,))
    userid = c.fetchone()
    conn.close
    return userid[0] if userid else None

def main():
    verify_user('Demon', 'Dynamo@27')

def get_usernames():
    conn = sqlite3.connect("transactions.db")
    query = "SELECT username FROM users"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df['username'].tolist()

def get_transactions(user_id, start_date, end_date):
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    
    c.execute('''
        SELECT date, description, category, type, amount
        FROM transactions
        WHERE userid= ? AND date BETWEEN ? AND ?;
    ''', (user_id, start_date, end_date, ))

    results = c.fetchall()
    conn.close()

    return results

def get_sum_by_label(user_id, start_date, end_date, labels):
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    
    c.execute('''
        SELECT category, SUM(amount) AS total_amount
        FROM transactions WHERE userid = ? AND type = "withdraw" AND date BETWEEN ? AND ?
        GROUP BY category
    ''', (user_id, start_date, end_date, ))
    
    withdraw = c.fetchall()
    
    c.execute('''
        SELECT category, SUM(amount) AS total_amount
        FROM transactions WHERE userid = ? AND type = "deposit" AND date BETWEEN ? AND ?
        GROUP BY category
    ''', (user_id, start_date, end_date, ))

    deposit = c.fetchall()

    w_dict = {row[0]: row[1] for row in withdraw}
    d_dict = {row[0]: row[1] for row in deposit}
    
    w_sums = [w_dict.get(label, 0) for label in labels]
    d_sums = [d_dict.get(label, 0) for label in labels]
    
    return (w_sums, d_sums)
   
def reset_transactions(user_id):
    # Connect to the database
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()

    try:
        # Begin transaction
        conn.execute('BEGIN')

        # Step 1: Delete all transactions for the given user_id
        c.execute("DELETE FROM transactions WHERE userid = ?", (user_id,))
        conn.commit()

        # Step 2: Reassign IDs to remove gaps
        # Select remaining transactions ordered by the current 'id'
        c.execute("SELECT id FROM transactions ORDER BY id")
        transactions = c.fetchall()

        # If there are transactions left, renumber the ids
        if transactions:
            for new_id, (old_id,) in enumerate(transactions, start=1):
                # Update the transaction's id
                c.execute("UPDATE transactions SET id = ? WHERE id = ?", (new_id, old_id))

            conn.commit()

        # Step 3: Reset the autoincrement value in sqlite_sequence
        # Get the current highest id
        c.execute("SELECT MAX(id) FROM transactions")
        max_id = c.fetchone()[0]

        if max_id is None:
            max_id = 0  # If there are no remaining rows, reset the sequence to 0

        # Update sqlite_sequence to ensure the next id starts after the current max_id
        c.execute("UPDATE sqlite_sequence SET seq = ? WHERE name = 'transactions'", (max_id,))
        conn.commit()

        print(f"All transactions for user {user_id} deleted and IDs reset.")
    except sqlite3.Error as e:
        conn.rollback()  # Roll back the transaction in case of an error
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        conn.close()

def reset_transactions_within_dates(user_id, from_date, to_date):
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()

    try:
        conn.execute('BEGIN')

        c.execute("""
            DELETE FROM transactions 
            WHERE userid = ? AND date BETWEEN ? AND ?
        """, (user_id, from_date, to_date))
        conn.commit()

        c.execute("SELECT id FROM transactions ORDER BY id")
        transactions = c.fetchall()

        if transactions:
            for new_id, (old_id,) in enumerate(transactions, start=1):
                c.execute("UPDATE transactions SET id = ? WHERE id = ?", (new_id, old_id))

            conn.commit()

        c.execute("SELECT MAX(id) FROM transactions")
        max_id = c.fetchone()[0]

        if max_id is None:
            max_id = 0

        c.execute("UPDATE sqlite_sequence SET seq = ? WHERE name = 'transactions'", (max_id,))
        conn.commit()

        print(f"All transactions for user {user_id} between {from_date} and {to_date} deleted and IDs reset.")
    except sqlite3.Error as e:
        conn.rollback()
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def delete_user_and_reset(user_id):
    reset_transactions(user_id)
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()

    try:
        # Begin transaction for user deletion
        conn.execute('BEGIN')

        # Step 2: Delete the user from the users table
        c.execute("DELETE FROM users WHERE userid = ?", (user_id,))
        conn.commit()

        # Step 3: Reassign user IDs to remove gaps
        c.execute("SELECT userid FROM users ORDER BY userid")
        users = c.fetchall()

        if users:
            for new_id, (old_id,) in enumerate(users, start=1):
                c.execute("UPDATE users SET userid = ? WHERE userid = ?", (new_id, old_id))

            conn.commit()

        # Step 4: Reset the autoincrement value in sqlite_sequence
        c.execute("SELECT MAX(userid) FROM users")
        max_userid = c.fetchone()[0]

        if max_userid is None:
            max_userid = 0  # If there are no remaining rows, reset the sequence to 0

        c.execute("UPDATE sqlite_sequence SET seq = ? WHERE name = 'users'", (max_userid,))
        conn.commit()

        print(f"User {user_id} and their transactions deleted, and user IDs reset.")
    except sqlite3.Error as e:
        conn.rollback()  # Rollback the transaction in case of an error
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_transactions(1, '2024-01-01', 'Rent Payment', 'HOUSING', 'withdraw', 1200)
    add_transactions(1, '2024-01-03', 'Groceries', 'FOOD', 'withdraw', 150)
    add_transactions(1, '2024-01-05', 'Salary', 'PERSONAL', 'deposit', 2500)
    add_transactions(1, '2024-01-06', 'Gas Refill', 'TRANSPORT', 'withdraw', 40)
    add_transactions(1, '2024-01-08', 'Electricity Bill', 'UTILITIES', 'withdraw', 80)
