import sqlite3
database_name='../db/db.db'
def create_table_customer():
    db = sqlite3.connect(database_name)
    cursor = db.cursor()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS "customer" (
	"id"	INTEGER NOT NULL UNIQUE,
	"customer_name"	TEXT,
	"phone_number"	TEXT,
	"customer_adress" TEXT,
	"registration_date"	TEXT,
	"photo"	BLOB,
	PRIMARY KEY("id" AUTOINCREMENT)
    )""")
    cursor.close()
    db.commit()
    db.close()
create_table_customer()
