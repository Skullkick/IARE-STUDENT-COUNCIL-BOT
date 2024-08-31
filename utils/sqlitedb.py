import sqlite3

# The main database for managing overall council operations, including member information, meetings, and administrative tasks.
COUNCIL_MANAGEMENT_DATABASE = "council_management.db"
# A database dedicated to tracking and managing council-related activities, including events, club activities, and participation records.
COUNCIL_ACTIVITIES_DATABASE = "council_activities.db"
# A database for managing the clubs
CLUBS_DATABASE = "clubs.db"


async def create_council_management_table():
    """
    Create the necessary tables for the council management in the SQLite database.
    """
    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.cursor()
        # Create a table to store member information
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT UNIQUE NOT NULL,
                tenure_start DATE NOT NULL,
                tenure_end DATE
            )
        """)
        conn.commit()


#Council Activites database code.
async def create_council_activities_table():
    """
    Create the necessary tables for council activities in the SQLite database.
    """
    with sqlite3.connect(COUNCIL_ACTIVITIES_DATABASE) as conn:
        cursor = conn.cursor()
        # Create a table to store activity information
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                date DATE DEFAULT CURRENT_DATE,
                location TEXT,
                organizer TEXT,
                participants_count INTEGER
            )
        """)
        conn.commit()

async def upsert_activity(id=None, name=None, description=None, date=None, location=None, organizer=None, participants_count=None):
    """
    Insert a new activity into the database or update an existing activity if ID is provided.
    """
    with sqlite3.connect(COUNCIL_ACTIVITIES_DATABASE) as conn:
        cursor = conn.cursor()

        if id is None:
            # Insert new activity
            cursor.execute("""
                INSERT INTO activities (name, description, date, location, organizer, participants_count)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, description, date, location, organizer, participants_count))
        else:
            # Update existing activity
            cursor.execute("""
                UPDATE activities
                SET name = COALESCE(?, name),
                    description = COALESCE(?, description),
                    date = COALESCE(?, date),
                    location = COALESCE(?, location),
                    organizer = COALESCE(?, organizer),
                    participants_count = COALESCE(?, participants_count)
                WHERE id = ?
            """, (name, description, date, location, organizer, participants_count, id))

        conn.commit()

async def get_id_by_name(name):
    """
    Retrieve the ID of an activity based on its name.
    """
    with sqlite3.connect(COUNCIL_ACTIVITIES_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM activities
            WHERE name = ?
        """, (name,))
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            return None

async def get_activity_details(activity_id, include_name=True, include_description=False, include_date=False, include_location=False, include_organizer=False, include_participants_count=False):
    """
    Retrieve values of specified attributes for an activity based on boolean flags.
    
    Parameters:
    - activity_id: The ID of the activity to retrieve.
    - include_name: Boolean flag to include the 'name' attribute in the result.
    - include_description: Boolean flag to include the 'description' attribute in the result.
    - include_date: Boolean flag to include the 'date' attribute in the result.
    - include_location: Boolean flag to include the 'location' attribute in the result.
    - include_organizer: Boolean flag to include the 'organizer' attribute in the result.
    - include_participants_count: Boolean flag to include the 'participants_count' attribute in the result.
    
    Returns:
    - A dictionary with the attribute names and their values if included.
    """
    with sqlite3.connect(COUNCIL_ACTIVITIES_DATABASE) as conn:
        cursor = conn.cursor()
        
        # Build the SELECT statement based on the included attributes
        columns = []
        if include_name:
            columns.append("name")
        if include_description:
            columns.append("description")
        if include_date:
            columns.append("date")
        if include_location:
            columns.append("location")
        if include_organizer:
            columns.append("organizer")
        if include_participants_count:
            columns.append("participants_count")
        
        # Join columns to form the SELECT query
        select_columns = ", ".join(columns)
        
        # Execute the query
        cursor.execute(f"""
            SELECT {select_columns}
            FROM activities
            WHERE id = ?
        """, (activity_id,))
        
        row = cursor.fetchone()
        if row:
            # Create a dictionary with the column names and their values
            result = {column: value for column, value in zip(columns, row)}
            return result
        else:
            return None

# Clubs code.
async def create_clubs_table():
    """
    Create the necessary table for storing club information in the SQLite database.
    """
    with sqlite3.connect(CLUBS_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clubs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                founding_date DATE,
                president TEXT,
                members_count INTEGER
            )
        """)
        conn.commit()

