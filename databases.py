import sqlite3
conn = sqlite3.connect('management.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (id INTEGER PRIMARY KEY, user TEXT, password TEXT, perm INTEGER)''')

c.execute('''CREATE TABLE IF NOT EXISTS user_info
             (id INTEGER PRIMARY KEY, customer_id TEXT, customer_name TEXT, customer_mobile TEXT, customer_email TEXT, customer_username TEXT, customer_password TEXT, customer_address TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS transaction_info
             (id INTEGER PRIMARY KEY, 
             transaction_id TEXT,
              transaction_customer_id TEXT, 
              transaction_amount TEXT, 
              transaction_bill TEXT, 
              transaction_number TEXT, 
              transaction_type TEXT, 
              transaction_history TEXT, 
              transaction_description TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS bill_info
             (id INTEGER PRIMARY KEY, 
              bill_id TEXT,
              bill_customer_id TEXT, 
              bill_number TEXT, 
              bill_type TEXT, 
              bill_receipt TEXT, 
              bill_description TEXT,
              bill_amount TEXT,
              unpaid_bill TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS payment_info
             (id INTEGER PRIMARY KEY, 
              payment_id TEXT, 
              payment_customer_id TEXT, 
              payment_des TEXT, 
              payment_status TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS transaction_history_info
             (id INTEGER PRIMARY KEY, 
              transaction_history_id TEXT, 
              transaction_history_customer_id TEXT, 
              transaction_history_amount TEXT, 
              transaction_history_bill TEXT,
              transaction_history_number TEXT,
              transaction_history_type TEXT,
              transaction_history_description TEXT,
              unpaid_bill TEXT)''')



conn.commit()


conn.close()
