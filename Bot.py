from aiogram import executor
from dispatcher import han, cur, db
import settings
import handler


if __name__ == "__main__":
    cur.execute("""CREATE TABLE IF NOT EXISTS whitelist (
        link TEXT,
        chat_id BIGINT
    )""")

    db.commit()
    print("bot has been started")
    executor.start_polling(han, skip_updates=True)
