import sqlite3
database_name='db/db.db'
def create_table_drawn_list():
    db=sqlite3.connect(database_name)
    cursor=db.cursor()
    cursor.execute("""CREATE  TABLE IF NOT EXISTS "drawn_list" (
	"id" INTEGER NOT NULL UNIQUE  ,
	"customer_id"	INTEGER,
	"equb_type_id"	INTEGER,
	"drawn_date"	TEXT,
	"amount_of_money"	INTEGER,
	"warrant_id"	INTEGER,
	"drawn_round"	INTEGER,
	"drawn_tax"	INTEGER,
    PRIMARY KEY ("id" AUTOINCREMENT),
	FOREIGN KEY ("warrant_id") REFERENCES customer(id),
	FOREIGN KEY ("equb_type_id") REFERENCES equb_type(id) ,
	FOREIGN KEY ("customer_id") REFERENCES customer(id) 
    );  """)
    cursor.close()
    db.commit()
    db.close()
create_table_drawn_list()