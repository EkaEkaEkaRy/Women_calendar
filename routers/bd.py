import sqlite3 as sq
import os.path


async def db_start():  # Создание таблицы с Id пользователя, длиной цикла и периода
    db = sq.connect('bot.db')
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id TEXT PRIMARY KEY, 
        period_length INTEGER, 
        cycle_length INTEGER)""")
    db.commit()
    db.close()


async def create_user_users(user_id):  # добавление в таблицу нового пользователя (только Id)
    db = sq.connect('bot.db')
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
            user_id TEXT PRIMARY KEY, 
            period_length INTEGER, 
            cycle_length INTEGER)""")
    user = cur.execute("SELECT 1 "
                       "FROM users "
                       "WHERE user_id = {key}".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO users (user_id, period_length, cycle_length) VALUES (?, ?, ?)", (user_id, '', ''))
        db.commit()
        db.close()


async def add_info_period(user_id, period_length):  # добавление в таблицу длины периода
    db = sq.connect('bot.db')
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                user_id TEXT PRIMARY KEY, 
                period_length INTEGER, 
                cycle_length INTEGER)""")
    cur.execute("UPDATE users "
                "SET period_length = {} "
                "WHERE user_id = {}".format(period_length, user_id))
    db.commit()
    db.close()


async def add_info_cycle(user_id, cycle_length):  # добавление в таблицу длины цикла
    db = sq.connect('bot.db')
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                user_id TEXT PRIMARY KEY, 
                period_length INTEGER, 
                cycle_length INTEGER)""")
    cur.execute("UPDATE users SET cycle_length = {} WHERE user_id = {}".format(cycle_length, user_id))
    db.commit()
    db.close()


''''''''''''''''''''''''''''''''''''


async def cycle_start():  # Создание таблицы с датами циклов
    db = sq.connect('bot.db')
    cur = db.cursor()
    cur.execute(f"""CREATE TABLE IF NOT EXISTS cycles(
        user_id TEXT PRIMARY KEY, 
        start_date STRING, 
        end_date STRING)""")
    db.commit()
    db.close()


async def create_user_cycles(user_id):  # добавление в таблицу cycles нового пользователя (только Id)
    db = sq.connect('bot.db')
    cur = db.cursor()
    user = user_id
    cur.execute("""CREATE TABLE IF NOT EXISTS cycles(
        user_id TEXT PRIMARY KEY, 
        start_date STRING, 
        end_date STRING)""")
    user = cur.execute("SELECT 1 "
                       "FROM cycles "
                       "WHERE user_id = {key}".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO cycles (user_id, start_date, end_date) VALUES (?, ?, ?)", (user_id, '', ''))
        db.commit()
        db.close()


async def start_date(user_id, start):  # добавление даты начала цикла
    db = sq.connect('bot.db')
    cur = db.cursor()
    cur.execute(f"""CREATE TABLE IF NOT EXISTS cycles(
        user_id TEXT PRIMARY KEY, 
        start_date STRING, 
        end_date STRING)""")
    cur.execute("UPDATE cycles SET start_date = {} WHERE user_id = {}".format(start, user_id))
    db.commit()
    db.close()


async def end_date(user_id, start, end):  # добвление даты конца цикла
    db = sq.connect('bot.db')
    cur = db.cursor()
    cur.execute(f"""CREATE TABLE IF NOT EXISTS cycles(
        user_id TEXT PRIMARY KEY, 
        start_date STRING, 
        end_date STRING)""")
    cur.execute("UPDATE cycles SET end_date = {} WHERE user_id = {} AND start_date = {}".format(end, user_id, start))
    db.commit()
    db.close()