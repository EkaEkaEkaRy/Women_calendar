import sqlite3 as sq
import os.path


async def db_start():  # Создание таблицы с Id пользователя, длиной цикла и периода
    db = sq.connect('bot.db')
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'users'("
                "user_id TEXT PRIMARY KEY, "
                "period_length INTEGER, "
                "cycle_length INTEGER)")
    db.commit()
    db.close()


async def create_user(user_id):  # добавление в таблицу нового пользователя (только Id)
    db = sq.connect('bot.db')
    cur = db.cursor()
    user = cur.execute("SELECT 1 "
                       "FROM 'users' "
                       "WHERE 'user_id' = '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO 'users' VALUES (?, ?, ?)", (user_id, '', ''))
        db.commit()
        db.close()


async def add_info_period(user_id, period_length):  # добавление в таблицу длины периода
    db = sq.connect('bot.db')
    cur = db.cursor()
    add = cur.execute("UPDATE 'users' "
                      "SET period_length = {} "
                      "WHERE user_id = {}".format(period_length, user_id))
    db.commit()
    db.close()


async def add_info_cycle(user_id, cycle_length):  # добавление в таблицу длины цикла
    db = sq.connect('bot.db')
    cur = db.cursor()
    add = cur.execute("UPDATE users WHERE user_id == '{}' SET cycle_length = {}".format(user_id, cycle_length))
    db.commit()
    db.close()
