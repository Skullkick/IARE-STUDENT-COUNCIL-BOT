import sqlite3

async def create_clubs_table():
    """
    Create the necessary table for storing club information in the SQLite database.
    """
    with sqlite3.connect(CLUBS_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clubs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT,
                president TEXT,
                pres_chat_id INTEGER,
                vice_president TEXT,
                vice_pres_chat_id INTEGER,
                event_ids TEXT
            )
        """)
        conn.commit()

"""
in Club event keyboards add a condition such that if chat_id is present in the normal club presidents then it should not give that option.
And for now i need to give them an interface first

"""
"""CLUB Interface"""
""" 
The interface for the clubs will be There should be text displaying the info of club if there are no events then it should display club infor.. else it should be displaying the events info 

Buttons:
Add Events
View Events
"""