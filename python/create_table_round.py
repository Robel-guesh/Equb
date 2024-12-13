import sqlite3
database_name='db/db.db'
def create_table_round():
    db = sqlite3.connect(database_name)
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE "round" (
	"id"	INTEGER NOT NULL UNIQUE,
	"equb_type_id"	INTEGER,
	"current_round"	INTEGER,
	FOREIGN KEY("equb_type_id") REFERENCES equb_type(id) ,
	PRIMARY KEY("id" AUTOINCREMENT)
    )""")
    cursor.close()
    db.commit()
    db.close()
create_table_round()