import sqlite3
database_name='db/db.db'
def create_table_user():
    db = sqlite3.connect(database_name)
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS "user" (
        "full_name" TEXT,
        "user_name" TEXT,
        "password" TEXT,
        "role" TEXT,
        "photo" BLOB
    )""")
    cursor.close()
    db.commit()
    db.close()
create_table_user()