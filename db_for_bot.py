import sqlite3

class DateBase():
    def __init__(self):
        self.conn = sqlite3.connect('db_bot.db', check_same_thread=False)
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute('CREATE TABLE if not exists History (User_id, Request)')

    def execute(self, query, data_in=''):
        self.cur.execute(query, data_in)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def add_entry(self, data_in):
        query = """ INSERT INTO History(User_id, Request) VALUES(?,?) """
        self.execute(query, data_in)
        self.commit()

    def get_data(self):
        query = """ SELECT * FROM History """
        self.execute(query)
        rows = self.cur.fetchall()
        if len(rows) > 10:
            rows = rows[-10:]
        return rows

# cur.execute('CREATE TABLE requests (id INTEGER AUTOINCREMENT, user, request)')
#
# def sql_add():
#     if message.text == '/low':
#         cur.execute("INSERT INTO db_bot VALUES (message.from_user.id, 'Запрос маленьких животных')")
#     if message.text == '/high':
#         cur.execute("INSERT INTO db_bot VALUES (message.from_user.id, 'Запрос больших животных')")
#     if message.text == '/custom':
#         cur.execute("INSERT INTO db_bot VALUES (message.from_user.id, 'Запрос животных по Вашим параметрам')")

my_db = DateBase()