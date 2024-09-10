import sqlite3

# The main database for managing overall council operations, including member information, meetings, and administrative tasks.
COUNCIL_MANAGEMENT_DATABASE = "council_management.db"
# A database dedicated to tracking and managing council-related activities, including events, club activities, and participation records.
COUNCIL_ACTIVITIES_DATABASE = "council_activities.db"
# A database for managing the clubs
CLUBS_DATABASE = "clubs.db"
# A database to keep track of adding club things.
TEMP_CLUBS_DATABASE = "temp_clubs.db"
# A database to keep track of all things with permissions
PERMISSIONS_DATABASE = "permissions.db"

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


#Club Activites database code.
async def create_club_activities_table():
    """
    Create the necessary tables for council activities in the SQLite database.
    """
    with sqlite3.connect(COUNCIL_ACTIVITIES_DATABASE) as conn:
        cursor = conn.cursor()
        # Create a table to store activity information
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                club_id INTEGER,
                name TEXT NOT NULL,
                club_name TEXT,
                description TEXT,
                date DATE DEFAULT CURRENT_DATE,
                location TEXT,
                organizer TEXT,
                participants_count INTEGER
            )
        """)
        conn.commit()

async def upsert_activity(id=None, name=None, club_id=None, description=None, date=None, location=None, organizer=None, participants_count=None):
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
                    club_id = COALESCE(?, club_id)
                    description = COALESCE(?, description),
                    date = COALESCE(?, date),
                    location = COALESCE(?, location),
                    organizer = COALESCE(?, organizer),
                    participants_count = COALESCE(?, participants_count)
                WHERE id = ?
            """, (name, club_id, description, date, location, organizer, participants_count, id))

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
                president TEXT,
                vice_president TEXT
            )
        """)
        conn.commit()
        
async def store_club_info(club_id, name, description=None, founding_date=None, president=None, vice_president=None, members_count=None):
    """
    Store club information in the database. If the club already exists, update the information; otherwise, insert a new record.
    :param club_id: The ID of the club (for updating; use None for new records).
    :param name: The name of the club (required for both new and existing records).
    :param description: A description of the club.
    :param president: The name of the president.
    :param vice_president: The name of the vice president.
    """
    
    with sqlite3.connect(CLUBS_DATABASE) as conn:
        cursor = conn.cursor()
        if club_id is not None:
            # Update existing record
            cursor.execute('SELECT * FROM clubs WHERE id = ?', (club_id,))
            existing_data = cursor.fetchone()
            
            if existing_data:
                if name is not None:
                    cursor.execute('UPDATE clubs SET name = ? WHERE id = ?', (name, club_id))
                if description is not None:
                    cursor.execute('UPDATE clubs SET description = ? WHERE id = ?', (description, club_id))
                if president is not None:
                    cursor.execute('UPDATE clubs SET president = ? WHERE id = ?', (president, club_id))
                if vice_president is not None:
                    cursor.execute('UPDATE clubs SET vice_president = ? WHERE id = ?', (vice_president, club_id))
            else:
                raise ValueError("Club ID does not exist for update.")
        else:
            # Insert new record
            cursor.execute('INSERT INTO clubs (name, description, president, vice_president) VALUES (?, ?, ?, ?)',
                           (name, description, president, vice_president))
        conn.commit()

async def get_club_names_and_indexes():
    """
    Asynchronously fetch all club names and their indexes from the SQLite database.
    Returns a list of tuples with (id, name).
    """
    with sqlite3.connect(CLUBS_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM clubs")
        clubs = cursor.fetchall()
        return clubs




# Temp Clubs code

async def create_temp_clubs_table():
    """
    Create the necessary table for storing club information temporarily in the SQLite database.
    """
    with sqlite3.connect(TEMP_CLUBS_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clubs (
                chat_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                president TEXT,
                vice_president TEXT,
            )
        """)
        conn.commit()

async def store_temp_club_info(chat_id, name=None, description=None, president=None, vice_president=None):
    """
    Asynchronously store or update club information in the temporary database.
    
    :param chat_id: The unique identifier for the club.
    :param name: The name of the club (required).
    :param description: A description of the club.
    :param president: The name of the president.
    :param vice_president: The name of the vice president.
    """
    with sqlite3.connect(TEMP_CLUBS_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clubs WHERE chat_id = ?', (chat_id,))
        existing_data = cursor.fetchone()
        if existing_data:
            # Update existing record
            if name is not None:
                cursor.execute('UPDATE clubs SET name = ? WHERE chat_id = ?', (name, chat_id))
            if description is not None:
                cursor.execute('UPDATE clubs SET description = ? WHERE chat_id = ?', (description, chat_id))
            if president is not None:
                cursor.execute('UPDATE clubs SET president = ? WHERE chat_id = ?', (president, chat_id))
            if vice_president is not None:
                cursor.execute('UPDATE clubs SET vice_president = ? WHERE chat_id = ?', (vice_president, chat_id))
        else:
            # Insert new record
            cursor.execute('INSERT INTO clubs (chat_id, name, description, founding_date, president, vice_president, members_count) VALUES (?, ?, ?, ?, ?)',
                           (chat_id, name, description, president, vice_president))
        conn.commit()

async def check_temp_club_field_presence(chat_id):
    """
    Check the presence of each field for the given chat_id and return a dictionary with True/False for each field.
    
    :param chat_id: The unique identifier for the club.
    :return: A dictionary indicating the presence of each field.
    """
    
    with sqlite3.connect(TEMP_CLUBS_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clubs WHERE chat_id = ?', (chat_id,))
        result = cursor.fetchone()
        if result:
            # Unpack the result tuple
            _, name, description, president, vice_president = result
            
            # Create the dictionary based on the presence of each field
            return {
                'name': name is not None,
                'description': description is not None,
                'president': president is not None,
                'vice_president': vice_president is not None,
            }
        else:
            # Handle the case where the chat_id is not found
            return {
                'name': False,
                'description': False,
                'president': False,
                'vice_president': False,
            }
        


# Permissions code

async def create_permissions_table():
    conn = sqlite3.connect(PERMISSIONS_DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS permissions (
            chat_id INTEGER PRIMARY KEY,
            events BOOLEAN NOT NULL,
            clubs BOOLEAN NOT NULL,
            proposal_form BOOLEAN NOT NULL,
            flyer BOOLEAN NOT NULL
        )
    ''')

    conn.commit()

async def initialize_permissions(chat_id):
    conn = sqlite3.connect(PERMISSIONS_DATABASE)
    cursor = conn.cursor()

    # Insert default values (False) for the given chat_id
    cursor.execute('''
        INSERT INTO permissions (chat_id, events, clubs, proposal_form, flyer)
        VALUES (?, 0, 0, 0, 0)
    ''', (chat_id,))

    conn.commit()

async def set_permissions(chat_id, events=False, clubs=False, proposal_form=False, flyer=False):
    conn = sqlite3.connect(PERMISSIONS_DATABASE)
    cursor = conn.cursor()

    # Check if the chat_id already exists
    cursor.execute('''
        SELECT chat_id FROM permissions WHERE chat_id = ?
    ''', (chat_id,))
    
    result = cursor.fetchone()

    if result is None:
        # If the chat_id doesn't exist, insert a new record with the provided values
        cursor.execute('''
            INSERT INTO permissions (chat_id, events, clubs, proposal_form, flyer)
            VALUES (?, ?, ?, ?, ?)
        ''', (chat_id, events, clubs, proposal_form, flyer))
    else:
        # If the chat_id exists, update the record with the new values
        cursor.execute('''
            UPDATE permissions
            SET events = ?, clubs = ?, proposal_form = ?, flyer = ?
            WHERE chat_id = ?
        ''', (events, clubs, proposal_form, flyer, chat_id))

    conn.commit()
    conn.close()