import sqlite3
database_name='../db/db.db'
def create_table_equb_enrollment():
    db = sqlite3.connect(database_name)
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS "equb_enrollment_history" (
	"id"	INTEGER NOT NULL UNIQUE,
	"customer_id"	INTEGER,
	"equb_type"	TEXT,
	"amount"	INTEGER,
	"number_of_paid_lot"	INTEGER,
	"paid_date"	TEXT,
	"reg_number_of_paid_lot"	INTEGER,
	FOREIGN KEY("customer_id") REFERENCES "customer"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);""")
    cursor.close()
    db.commit()
    db.close()
create_table_equb_enrollment()
