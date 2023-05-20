import sqlite3

# utils common for several scripts

db_location = "/root/pyserver/db.db"
# db_location = "C:\\workspace\\po-s-2023-hakaton\\db.db"

def execute_command(comm, params=()):
    with sqlite3.connect(db_location) as conn:
        cur = conn.cursor()
        cur.execute(comm, params)
        conn.commit()

def execute_query(comm, params=()):
    with sqlite3.connect(db_location) as conn:
        cur = conn.cursor()
        cur.execute(comm, params)
        result = cur.fetchall()
        conn.commit()
    return result
