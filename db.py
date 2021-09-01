import os
import psycopg2

DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a susumoney').read()[:-1]

conn = psycopg2.connect(DATABASE_URL, sslmode = "require")
cursor = conn.cursor()

message = "chat"
sql = 'INSERT INTO chat(chat) VALUES(' + message + ')'

print(sql, message)

"""
create_chat_table_query = '''CREATE TABLE chat(id SERIAL PRIMARY KEY NOT NULL,
                                                chat TEXT NOT NULL);'''

create_idToAccount_table_query = '''CREATE TABLE idToAccount(userID TEXT NOT NULL,
                                                        account INT PRIMARY KEY NOT NULL);'''
create_balance_table_query = '''CREATE TABLE balance(account SERIAL PRIMARY KEY NOT NULL,
                                                     amount INT NOT NULL);'''
create_income_table_query = '''CREATE TABLE income(id SERIAL PRIMARY KEY NOT NULL, 
                                                    userID TEXT NOT NULL, 
                                                    date DATE NOT NULL,
                                                    time TIME NOT NULL,
                                                    usage TEXT NOT NULL,
                                                    amount INT NOT NULL);'''
create_outcome_table_query = '''CREATE TABLE outcome(id SERIAL PRIMARY KEY NOT NULL, 
                                                    userID TEXT NOT NULL, 
                                                    date DATE NOT NULL, 
                                                    time TIME NOT NULL, 
                                                    usage TEXT NOT NULL, 
                                                    amount INT NOT NULL);'''
""""""
cursor.execute("DROP TABLE chat;")
cursor.execute("DROP TABLE idToAccount;")
cursor.execute("DROP TABLE balance;")
cursor.execute("DROP TABLE income;")
cursor.execute("DROP TABLE outcome;")
"""

"""
cursor.execute(create_chat_table_query)
cursor.execute(create_idToAccount_table_query)
cursor.execute(create_balance_table_query)
cursor.execute(create_income_table_query)
cursor.execute(create_outcome_table_query)
"""

conn.commit()

cursor.close()
conn.close()