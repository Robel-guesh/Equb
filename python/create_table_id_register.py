import sqlite3
database_name='db/db.db'
def create_table_id_register():
    db = sqlite3.connect(database_name)
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS "id_register" (
        "id" INTEGER NOT NULL UNIQUE,
        "reached_id" INTEGER,
        PRIMARY KEY("id" AUTOINCREMENT)
    )""")
    cursor.close()
    db.commit()
    db.close()
    print('id created')
create_table_id_register()