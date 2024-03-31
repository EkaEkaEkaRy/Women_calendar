import sqlite3 as sq

async def db_start() : #Создание таблицы с Id пользователя, длиной цикла и периода
    global db, cur

    db = sq.connect('bot.db')
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(user_id TEXT PRIMARY KEY, period_length INTEGER, cycle_length INTEGER)")
    db.commit()

async def create_user(user_id): #добавление в таблицу нового пользователя (только Id)
    user = cur.execute("SELECT 1 FROM users WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO users VALUES (?, ?, ?)", (user_id, '', ''))
        db.commit

async def add_info_period(user_id, period_length): #добавление в таблицу длины периода
    add = cur.execute("UPDATE users WHERE user_id == '{}' SET period_length = {}".format(user_id, period_length))
    db.commit()
    
async def add_info_cycle(user_id, cycle_length): #добавление в таблицу длины цикла
    add = cur.execute("UPDATE users WHERE user_id == '{}' SET cycle_length = {}".format(user_id, cycle_length))
    db.commit()