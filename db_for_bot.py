import sqlite3

conn = sqlite3.connect('db_bot.db')
cur = conn.cursor()

cur.execute('CREATE TABLE requests (id INTEGER AUTOINCREMENT, user, request)')

def sql_add():
    if message.text == '/low':
        cur.execute("INSERT INTO db_bot VALUES (message.from_user.id, 'Запрос маленьких животных')")
    if message.text == '/high':
        cur.execute("INSERT INTO db_bot VALUES (message.from_user.id, 'Запрос больших животных')")
    if message.text == '/custom':
        cur.execute("INSERT INTO db_bot VALUES (message.from_user.id, 'Запрос животных по Вашим параметрам')")

