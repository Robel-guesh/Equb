import sqlite3
database_name='db/db.db'
def create_table_equb_type():
    db = sqlite3.connect(database_name)
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS "equb_type" (
	"id"	INTEGER NOT NULL UNIQUE,
	"equb_name" TEXT,
	"equb_type"	TEXT,
	"amount_of_money"	INTEGER,
	"total_member"	INTEGER,
    "tax" INTEGER , 
	PRIMARY KEY("id" AUTOINCREMENT)
    )""")
    cursor.close()
    db.commit()
    db.close()
create_table_equb_type()
