import sqlite3
database_name='../db/db.db'
def create_table_pay_list():
    db = sqlite3.connect(database_name)
    cursor = db.cursor()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS "pay_list_history" (
	"id"	INTEGER NOT NULL ,
	"customer_id"	INTEGER,
	"equb_type_id"	INTEGER,
	"amount"	INTEGER,
	"number_of_paid_lot"	INTEGER,
	"paid_round"	INTEGER,
	"punished_amount" INTEGER,
	"paid_date"	TEXT,
	FOREIGN KEY("equb_type_id") REFERENCES "equb_type"("id"),
	FOREIGN KEY("customer_id") REFERENCES "customer"("id"),
	
	
)""")
    
    
    
    
    
    cursor.close()
    db.commit()
    db.close()
create_table_pay_list()
