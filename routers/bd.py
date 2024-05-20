import sqlite3 as sq
import os.path
from datetime import date
from datetime import datetime, timedelta


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
        cur.execute("INSERT INTO users (user_id, period_length, cycle_length) VALUES (?, ?, ?)", (user_id, 6, 30))
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
        start_date TEXT, 
        end_date TEXT)""")
    db.commit()
    db.close()


'''async def create_user_cycles(user_id):  # добавление в таблицу cycles нового пользователя (только Id)
    db = sq.connect('bot.db')
    cur = db.cursor()
    user = user_id
    cur.execute("""CREATE TABLE IF NOT EXISTS cycles(
        user_id TEXT PRIMARY KEY, 
        start_date TEXT, 
        end_date TEXT)""")
    user = cur.execute("SELECT 1 "
                       "FROM cycles "
                       "WHERE user_id = {key}".format(key=user_id)).fetchone()
    if not user:
        cur.execute(f"INSERT INTO cycles (user_id, start_date, end_date) VALUES (?, ?, ?)", (user_id, ' ', ' '))
        db.commit()
        db.close()'''


async def start_date(user_id, start):  # добавление даты начала цикла
    db = sq.connect('bot.db')
    cur = db.cursor()
    cur.execute(f"""CREATE TABLE IF NOT EXISTS cycles(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            user_id TEXT, 
            start_date TEXT, 
            end_date TEXT)""")
    days_period_long = cur.execute("""SELECT period_length FROM users WHERE user_id = ?""", (user_id, )).fetchone()[0]
    end = str(start + timedelta(days=days_period_long))
    #ending = datetime.strptime(end, "%Y.%m.%d")
    cur.execute("INSERT INTO cycles (user_id, start_date, end_date) VALUES (?, ?, ?)",
                (user_id, f"{start}", f"{end}"))
    db.commit()
    db.close()


async def end_date(user_id, end):  # добвление даты конца цикла
    db = sq.connect('bot.db')
    cur = db.cursor()
    cur.execute(f"""CREATE TABLE IF NOT EXISTS cycles(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        user_id TEXT, 
        start_date TEXT, 
        end_date TEXT)""")
    latest_start = cur.execute(f"""SELECT start_date FROM cycles WHERE start_date <= '{end}' AND user_id = {user_id} ORDER BY start_date DESC""").fetchone()[0]
    print(latest_start, end.strftime("%Y-%m-%d"))
    if latest_start == end.strftime("%Y-%m-%d"):
        print("Yes")
        cur.execute(f"""DELETE FROM cycles WHERE start_date = '{latest_start}' AND user_id = {user_id};""")
    else:
        cur.execute("UPDATE cycles SET end_date = ? WHERE user_id = ? AND start_date = ?", (f"{end}", user_id, f"{latest_start}"))
    db.commit()
    db.close()


async def sel1():  # добвление даты конца цикла
    db = sq.connect('bot.db')
    cur = db.cursor()
    cur.execute(f"""SELECT * FROM cycles""")
    users = cur.fetchall()
    for user in users:
        print(user)
    db.commit()
    db.close()


async def sel2():  # добвление даты конца цикла
    db = sq.connect('bot.db')
    cur = db.cursor()
    cur.execute(f"""SELECT * FROM users""")
    users = cur.fetchall()
    for user in users:
        print(user)
    db.commit()
    db.close()


async def delet(user_id):  # добвление даты конца цикла
    db = sq.connect('bot.db')
    cur = db.cursor()
    cur.execute(f"DELETE FROM cycles WHERE user_id = {user_id}")
    db.commit()
    db.close()

async def select_periops_info(user_id):
    db = sq.connect('bot.db')
    cur = db.cursor()
    periods = cur.execute(f"""SELECT start_date, end_date FROM cycles WHERE user_id = {user_id}""").fetchall()
    return periods

async def cycle_info(user_id):
    db = sq.connect('bot.db')
    cur = db.cursor()
    curr_date = date.today()
    cycle_length = int(cur.execute("SELECT cycle_length "
                           "FROM users "
                           "WHERE user_id = ?", (user_id,)).fetchone()[0])
    cycles = cur.execute("SELECT start_date "
                                   "FROM cycles "
                                   "WHERE user_id = ?", (user_id,)).fetchone()
    last_cycle = datetime.strptime(cycles[len(cycles)-1], "%Y-%m-%d")
    next_cycle = (last_cycle + timedelta(days=cycle_length)).date()
    count_days = (next_cycle - curr_date).days
    return next_cycle.strftime("%d.%m.%Y"), count_days
    db.close()


async def fertile_days(user_id):
    db = sq.connect('bot.db')
    cur = db.cursor()
    curr_date = date.today()
    cycle_length = int(cur.execute("SELECT cycle_length "
                           "FROM users "
                           "WHERE user_id = ?", (user_id,)).fetchone()[0])
    cycles = cur.execute("SELECT start_date "
                                   "FROM cycles "
                                   "WHERE user_id = ?", (user_id,)).fetchone()
    number_day_start = cycle_length - 16
    number_day_end = cycle_length - 12
    start_days = datetime.strptime(cycles[len(cycles)-1], "%Y-%m-%d")
    next_days_start = (start_days + timedelta(days=number_day_start)).date()
    next_days_end = (start_days + timedelta(days=number_day_end)).date()
    count_days = (next_days_start - curr_date).days
    return next_days_start.strftime("%d.%m.%Y"), next_days_end.strftime("%d.%m.%Y"), count_days
    db.close()