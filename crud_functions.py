import sqlite3


def initiate_db():
    connect = sqlite3.connect('teleBot.db')
    curs = connect.cursor()
    curs.execute(
        '''
        CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL
        )
        '''
    )
    connect.commit()
    curs.execute(
        '''
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
        )
        '''
    )
    connect.commit()
    connect.close()


def get_all_products():
    connect = sqlite3.connect('teleBot.db')
    curs = connect.cursor()
    curs.execute(
        '''
        SELECT * FROM Products
        '''
    )
    data = curs.fetchall()
    connect.commit()
    connect.close()
    return data


def add_user(username, email, age):
    con = sqlite3.connect('teleBot.db')
    curs = con.cursor()
    curs.execute(
        '''
        INSERT INTO Users (username, email, age, balance)
        VALUES (?, ?, ?, ?)
        ''', (username, email, age, 1000)
    )
    con.commit()
    con.close()


def is_included(username):
    con = sqlite3.connect('teleBot.db')
    curs = con.cursor()
    curs.execute(
        '''
        SELECT username FROM Users
        '''
    )
    username_list = curs.fetchall()
    con.commit()
    con.close()
    for i in username_list:
        if i[0] == username:
            return True
    return False


initiate_db()

# con = sqlite3.connect('teleBot.db')
# curs = con.cursor()
# for i in range(1, 5):
#     curs.execute(
#         '''
#         INSERT INTO Products (id, title, description, price)
#         VALUES (?, ?, ?, ?)
#         ''', (f'{i}', f'Продукт {i}', f'Описание {i}', f'{i * 100}',)
#     )
# con.commit()
# con.close()
