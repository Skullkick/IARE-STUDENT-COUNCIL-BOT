import sqlite3
import json
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
# A database for managng events
EVENTS_DATABASE = "events.db"

async def initialize_sqlite_database():
    try:
        await create_student_council_table()
        await create_clubs_table()
        await create_permissions_table()
        await create_temp_clubs_table()
        await create_event_table()
        await create_temp_event_table()
        await create_core_team_table()
        await create_temp_core_team_table()
        await create_enforcement_team_table()
        await create_temp_enforcement_team_table()
        await create_table_event_data()


    except Exception as e:
        print(f"There is an error while initializing the sqlite database : {e}")

# async def create_council_management_table():
#     """
#     Create the necessary tables for the council management in the SQLite database.
#     """
#     with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
#         cursor = conn.cursor()
#         # Create a table to store member information
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS members (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 name TEXT NOT NULL,
#                 role TEXT NOT NULL,
#                 email TEXT UNIQUE NOT NULL,
#                 phone TEXT UNIQUE NOT NULL,
#                 tenure_start DATE NOT NULL,
#                 tenure_end DATE
#             )
#         """)
#         conn.commit()


# #Club Activites database code.
# async def create_club_activities_table():
#     """
#     Create the necessary tables for council activities in the SQLite database.
#     """
#     with sqlite3.connect(COUNCIL_ACTIVITIES_DATABASE) as conn:
#         cursor = conn.cursor()
#         # Create a table to store activity information
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS activities (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 club_id INTEGER,
#                 name TEXT,
#                 club_name TEXT,
#                 description TEXT,
#                 date DATE DEFAULT CURRENT_DATE,
#                 location TEXT,
#                 organizer TEXT,
#                 participants_count INTEGER
#             )
#         """)
#         conn.commit()

# async def upsert_activity(id=None, name=None, club_id=None, description=None, date=None, location=None, organizer=None, participants_count=None):
#     """
#     Insert a new activity into the database or update an existing activity if ID is provided.
#     """
#     with sqlite3.connect(COUNCIL_ACTIVITIES_DATABASE) as conn:
#         cursor = conn.cursor()

#         if id is None:
#             # Insert new activity
#             cursor.execute("""
#                 INSERT INTO activities (name, description, date, location, organizer, participants_count)
#                 VALUES (?, ?, ?, ?, ?, ?)
#             """, (name, description, date, location, organizer, participants_count))
#         else:
#             # Update existing activity
#             cursor.execute("""
#                 UPDATE activities
#                 SET name = COALESCE(?, name),
#                     club_id = COALESCE(?, club_id)
#                     description = COALESCE(?, description),
#                     date = COALESCE(?, date),
#                     location = COALESCE(?, location),
#                     organizer = COALESCE(?, organizer),
#                     participants_count = COALESCE(?, participants_count)
#                 WHERE id = ?
#             """, (name, club_id, description, date, location, organizer, participants_count, id))

#         conn.commit()

# async def get_id_by_name(name):
#     """
#     Retrieve the ID of an activity based on its name.
#     """
#     with sqlite3.connect(COUNCIL_ACTIVITIES_DATABASE) as conn:
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT id FROM activities
#             WHERE name = ?
#         """, (name,))
#         row = cursor.fetchone()
#         if row:
#             return row[0]
#         else:
#             return None

# async def get_activity_details(activity_id, include_name=True, include_description=False, include_date=False, include_location=False, include_organizer=False, include_participants_count=False):
#     """
#     Retrieve values of specified attributes for an activity based on boolean flags.
    
#     Parameters:
#     - activity_id: The ID of the activity to retrieve.
#     - include_name: Boolean flag to include the 'name' attribute in the result.
#     - include_description: Boolean flag to include the 'description' attribute in the result.
#     - include_date: Boolean flag to include the 'date' attribute in the result.
#     - include_location: Boolean flag to include the 'location' attribute in the result.
#     - include_organizer: Boolean flag to include the 'organizer' attribute in the result.
#     - include_participants_count: Boolean flag to include the 'participants_count' attribute in the result.
    
#     Returns:
#     - A dictionary with the attribute names and their values if included.
#     """
#     with sqlite3.connect(COUNCIL_ACTIVITIES_DATABASE) as conn:
#         cursor = conn.cursor()
        
#         # Build the SELECT statement based on the included attributes
#         columns = []
#         if include_name:
#             columns.append("name")
#         if include_description:
#             columns.append("description")
#         if include_date:
#             columns.append("date")
#         if include_location:
#             columns.append("location")
#         if include_organizer:
#             columns.append("organizer")
#         if include_participants_count:
#             columns.append("participants_count")
        
#         # Join columns to form the SELECT query
#         select_columns = ", ".join(columns)
        
#         # Execute the query
#         cursor.execute(f"""
#             SELECT {select_columns}
#             FROM activities
#             WHERE id = ?
#         """, (activity_id,))
        
#         row = cursor.fetchone()
#         if row:
#             # Create a dictionary with the column names and their values
#             result = {column: value for column, value in zip(columns, row)}
#             return result
#         else:
#             return None




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
                name TEXT,
                description TEXT,
                president TEXT,
                pres_chat_id INTEGER,
                vice_president TEXT,
                vice_pres_chat_id INTEGER
            )
        """)
        conn.commit()
        
async def store_club_info(club_id = None, name=None, description=None, president=None, pres_chat_id=None, vice_president=None,  vice_pres_chat_id=None):
    """
    Store club information in the database. If the club already exists, update the information; otherwise, insert a new record.
    :param club_id: The ID of the club (for updating; use None for new records).
    :param name: The name of the club (required for both new and existing records).
    :param description: A description of the club.
    :param president: The name of the president.
    :param pres_chat_id: The chat_id of the president.
    :param vice_president: The name of the vice president.
    :param vice_pres_chat_id: The chat_id of the vice president.
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
                if pres_chat_id is not None:
                    cursor.execute('UPDATE clubs SET pres_chat_id = ? WHERE id = ?', (pres_chat_id, club_id))
                if vice_president is not None:
                    cursor.execute('UPDATE clubs SET vice_president = ? WHERE id = ?', (vice_president, club_id))
                if vice_pres_chat_id is not None:
                    cursor.execute('UPDATE clubs SET vice_pres_chat_id = ? WHERE id = ?', (vice_pres_chat_id, club_id))
            else:
                raise ValueError("Club ID does not exist for update.")
        else:
            # Insert new record
            cursor.execute('INSERT INTO clubs (name, description, president, pres_chat_id, vice_president, vice_pres_chat_id) VALUES (?, ?, ?, ?, ?, ?)',
                           (name, description, president, pres_chat_id, vice_president, vice_pres_chat_id))
        conn.commit()
    return True

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

async def get_club_info_by_id(club_id):
    """
    Retrieve a row from the clubs table based on the id.
    """
    try:
        conn = sqlite3.connect(CLUBS_DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clubs WHERE id = ?", (club_id,))
        row = cursor.fetchone()
        return row
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

async def get_club_info_by_chat_id(chat_id: int):
    """
    Get club information based on the chat ID of the president or vice president.
    Args:
        chat_id (int): The chat ID of the president or vice president.

    Returns:
        dict: Club information if found, None otherwise.
    """
    query = """
        SELECT id, name, description, president, pres_chat_id, vice_president, vice_pres_chat_id 
        FROM clubs 
        WHERE pres_chat_id = ? OR vice_pres_chat_id = ?
    """
    with sqlite3.connect(CLUBS_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (chat_id, chat_id))
        result = cursor.fetchone()
        if result:
            return {
                "id": result[0],
                "name": result[1],
                "description": result[2],
                "president": result[3],
                "pres_chat_id": result[4],
                "vice_president": result[5],
                "vice_pres_chat_id": result[6]
            }
        return None

async def get_club_id_by_chat_id(chat_id: int):
    """
    Retrieve the club_id based on the president's or vice president's chat_id.
    """
    with sqlite3.connect(CLUBS_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM clubs
            WHERE pres_chat_id = ? OR vice_pres_chat_id = ?
        """, (chat_id, chat_id))
        result = cursor.fetchone()
        
    if result:
        return result[0]  # Return the club_id
    return None

async def get_club_name_by_club_id(club_id: int) -> str:
    """
    Retrieves the club name based on the club_id from the clubs table.

    :param club_id: The ID of the club.
    :return: The name of the club, or None if the club is not found.
    """

    # Connect to the SQLite database
    with sqlite3.connect(CLUBS_DATABASE) as conn:
        cursor = conn.cursor()

        # Fetch the club name based on club_id
        cursor.execute('SELECT name FROM clubs WHERE id = ?', (club_id,))
        result = cursor.fetchone()

        if result:
            return result[0]  # Return the club name
        else:
            print(f"No club found with ID {club_id}.")
            return None

async def delete_club_by_id(club_id: int):
    """
    Delete a club from the clubs table based on the club_id.

    :param club_id: The ID of the club to be deleted.
    """
    try:
        # Connect to the SQLite database
        with sqlite3.connect(CLUBS_DATABASE) as conn:
            cursor = conn.cursor()
            
            # Execute the DELETE statement
            cursor.execute("DELETE FROM clubs WHERE id = ?", (club_id,))
            
            # Commit the transaction
            conn.commit()
            
            # Check if any row was deleted
            if cursor.rowcount == 0:
                print(f"No club found with id {club_id}.")
            else:
                print(f"Club with id {club_id} deleted successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

async def get_club_id_by_name(club_name: str):
    """
    Retrieve the club ID from the database based on the club name.

    :param club_name: The name of the club to retrieve the ID for.
    :returns: The club ID if found, or None if the club is not found.
    """
    try:
        # Connect to the SQLite database
        with sqlite3.connect(CLUBS_DATABASE) as conn:
            cursor = conn.cursor()
            
            # Execute the SELECT statement to fetch the club ID
            cursor.execute("SELECT id FROM clubs WHERE name = ?", (club_name,))
            
            # Fetch the result
            result = cursor.fetchone()
            
            # Return the club ID or None if not found
            return result[0] if result else None
            
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

async def get_pres_and_vice_pres_chat_ids():
    with sqlite3.connect(CLUBS_DATABASE) as conn:
        cursor = conn.cursor()

        # Fetch pres_chat_id and vice_pres_chat_id from each row
        cursor.execute('SELECT pres_chat_id, vice_pres_chat_id FROM clubs')
        chat_ids = cursor.fetchall()  # Fetch all results

    # Flatten the list of tuples into a single list
    return [chat_id for pair in chat_ids for chat_id in pair]


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
                club_id TEXT,
                name TEXT,
                description TEXT,
                president TEXT,
                pres_chat_id INTEGER,
                vice_president TEXT,
                vice_pres_chat_id INTEGER
            )
        """)
        conn.commit()

async def store_temp_club_info(chat_id, name=None, club_id = None, description=None, president=None, pres_chat_id=None, vice_president=None,  vice_pres_chat_id=None):
    """
    Asynchronously store or update club information in the temporary database.
    
    :param chat_id: The unique identifier for the club.
    :param name: The name of the club (required).
    :param description: A description of the club.
    :param president: The name of the president.
    :param pres_chat_id: The chat_id of the president.
    :param vice_president: The name of the vice president.
    :param vice_pres_chat_id: The chat_id of the vice president.
    """
    try:
        with sqlite3.connect(TEMP_CLUBS_DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM clubs WHERE chat_id = ?', (chat_id,))
            existing_data = cursor.fetchone()
            if existing_data:
                # Update existing record
                if name is not None:
                    cursor.execute('UPDATE clubs SET name = ? WHERE chat_id = ?', (name, chat_id))
                if club_id is not None:
                    cursor.execute('UPDATE clubs SET club_id = ? WHERE chat_id = ?', (club_id, chat_id))
                if description is not None:
                    cursor.execute('UPDATE clubs SET description = ? WHERE chat_id = ?', (description, chat_id))
                if president is not None:
                    cursor.execute('UPDATE clubs SET president = ? WHERE chat_id = ?', (president, chat_id))
                if pres_chat_id is not None:
                    cursor.execute('UPDATE clubs SET pres_chat_id = ? WHERE chat_id = ?', (pres_chat_id, chat_id))
                if vice_president is not None:
                    cursor.execute('UPDATE clubs SET vice_president = ? WHERE chat_id = ?', (vice_president, chat_id))
                if vice_pres_chat_id is not None:
                    cursor.execute('UPDATE clubs SET vice_pres_chat_id = ? WHERE chat_id = ?', (vice_pres_chat_id, chat_id))
            else:
                # Insert new record
                cursor.execute('INSERT INTO clubs (chat_id, club_id, name, description, president, pres_chat_id, vice_president, vice_pres_chat_id) VALUES (?, ?, ?, ?, ?, ?,?,?)',
                               (chat_id, club_id, name, description, president, pres_chat_id, vice_president, vice_pres_chat_id))
            conn.commit()
    except Exception as e:
        print(f"Error while storing temp values to the database : {e}")

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
            _, _club_id, name, description, president,pres_chat_id, vice_president,vice_pres_chat_id = result
            
            # Create the dictionary based on the presence of each field
            return {
                'name': name is not None,
                'description': description is not None,
                'president': president is not None,
                'pres_chat_id' : pres_chat_id is not None,
                'vice_president': vice_president is not None,
                'vice_pres_chat_id' : vice_pres_chat_id is not None
            }
        else:
            # Handle the case where the chat_id is not found
            return {
                'name': False,
                'description': False,
                'president': False,
                'pres_chat_id' : False,
                'vice_president': False,
                'vice_pres_chat_id' : False
            }
        
async def retrieve_temp_club_info_by_chat_id(chat_id):
    """
    Retrieve club information from the clubs table based on the chat_id.
    """
    # try:
    # Connect to the SQLite database
    conn = sqlite3.connect(TEMP_CLUBS_DATABASE)
    cursor = conn.cursor()
    # Execute the query with parameterized input to prevent SQL injection
    cursor.execute("SELECT * FROM clubs WHERE chat_id = ?", (chat_id,))
    # Fetch the result
    row = cursor.fetchone()
    return row

    # except sqlite3.Error as e:
    #     print(f"An error occurred: {e}")
    #     return None

async def delete_temp_club_by_chat_id(chat_id):
    """
    Delete a row from the clubs table based on the chat_id.
    """
    try:
        conn = sqlite3.connect(TEMP_CLUBS_DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clubs WHERE chat_id = ?", (chat_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False

#Events Code
async def create_event_table():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(EVENTS_DATABASE)
    cursor = conn.cursor()

    # Create the events table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT ,
        number_of_days INTEGER ,
        date_time TEXT ,
        venue TEXT ,
        audience_size INTEGER ,
        type TEXT CHECK(type IN ('Tech', 'Non-Tech')),
        club_id INTEGER 
    )
    ''')

    # Commit changes and close the connection
    conn.commit()

async def store_event_info(id=None, name=None, number_of_days=None, date_time=None, venue=None, audience_size=None, type=None,club_id = None):
    """
    Insert a new event into the database, or update an existing one if the ID is provided.
    
    Parameters:
        id (int, optional): The ID of the event to update. If None, a new event will be inserted.
        name (str, optional): The name of the event.
        number_of_days (int, optional): The number of days for the event.
        date_time (str, optional): The date and time of the event in 'DD/MM/YYY-HH:MM:SS' format.
        venue (str, optional): The venue of the event.
        audience_size (int, optional): The estimated audience size for the event.
        type (str, optional): The type of the event ('Tech' or 'Non-Tech').
    """
    try:
        with sqlite3.connect(EVENTS_DATABASE) as conn:
            cursor = conn.cursor()
            
            if id is not None:
                # Check if the event exists
                cursor.execute('SELECT * FROM events WHERE id = ?', (id,))
                existing_data = cursor.fetchone()
                
                if existing_data:
                    # Update existing record
                    if name is not None:
                        cursor.execute('UPDATE events SET name = ? WHERE id = ?', (name, id))
                    if number_of_days is not None:
                        cursor.execute('UPDATE events SET number_of_days = ? WHERE id = ?', (number_of_days, id))
                    if date_time is not None:
                        cursor.execute('UPDATE events SET date_time = ? WHERE id = ?', (date_time, id))
                    if venue is not None:
                        cursor.execute('UPDATE events SET venue = ? WHERE id = ?', (venue, id))
                    if audience_size is not None:
                        cursor.execute('UPDATE events SET audience_size = ? WHERE id = ?', (audience_size, id))
                    if type is not None:
                        cursor.execute('UPDATE events SET type = ? WHERE id = ?', (type, id))
                    if club_id is not None:
                        cursor.execute('UPDATE events SET club_id = ? WHERE id = ?', (club_id, id))
                else:
                    print(f"Event with ID {id} does not exist.")
                    return False
            else:
                # Insert new record
                cursor.execute('''
                INSERT INTO events (name, number_of_days, date_time, venue, audience_size, type, club_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (name, number_of_days, date_time, venue, audience_size, type, club_id))
                print("Successfully stored")
            
            conn.commit()
            return True  # Return True if insertion or update was successful
    
    except Exception as e:
        print(f"Error while storing event values to the database: {e}")
        return False  # Return False if an error occurred

async def get_event_ids_and_names():
    """
    Asynchronously fetch all event IDs and their names from the SQLite database.
    Returns a list of tuples with (id, name).
    """
    with sqlite3.connect(EVENTS_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM events")
        events = cursor.fetchall()
        return events


async def get_club_id_by_event_id(event_id: int) -> int:
    """
    Retrieves the club_id based on the event_id from the events table.

    :param event_id: The ID of the event.
    :return: The club_id associated with the event, or None if the event is not found.
    """
    # Connect to the SQLite database
    with sqlite3.connect(EVENTS_DATABASE) as conn:
        cursor = conn.cursor()

        # Fetch the club_id based on event_id
        cursor.execute('SELECT club_id FROM events WHERE id = ?', (event_id,))
        result = cursor.fetchone()

        if result:
            return result[0]  # Return the club_id
        else:
            print(f"No event found with ID {event_id}.")
            return None

async def get_all_event_ids():
    """
    Asynchronously fetch all event IDs and their names from the SQLite database.
    Returns a list of tuples with (id, name).
    """
    with sqlite3.connect(EVENTS_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM events")
        event_ids = cursor.fetchall()
        return event_ids

async def get_event_info_by_id(event_id):
    """
    Retrieve a row from the events table based on the id.
    :return : returns a tuple :(id, name, number_of_days, date_time, venue, audience_size, type,club_id)  
    """
    try:
        conn = sqlite3.connect(EVENTS_DATABASE)
        cursor = conn.cursor()
        # Prepare the SQL query to get event details by ID
        cursor.execute('SELECT * FROM events WHERE id = ?', (event_id,))
        row = cursor.fetchone()
        return row
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

# async def get_event_ids_by_club_id(club_id: int):
#     """
#     Retrieve all event IDs for a given club_id.
#     """
#     with sqlite3.connect(EVENTS_DATABASE) as conn:
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT id FROM events
#             WHERE club_id = ?
#         """, (club_id,))
#         result = cursor.fetchall()  # Fetch all matching records
    
#     event_ids = [row[0] for row in result]  # Extract event IDs from the result
#     return event_ids

async def get_event_ids_and_names_by_club_id(club_id: int):
    """
    Retrieve all event IDs and names for a given club_id.
    """
    with sqlite3.connect(EVENTS_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name FROM events
            WHERE club_id = ?
        """, (club_id,))
        result = cursor.fetchall()  # Fetch all matching records
    
    event_data = [(row[0], row[1]) for row in result]  # Extract event IDs and names from the result
    return event_data

async def get_event_id_by_name(event_name):
    """
    Retrieves the event_id based on the name of the event.

    :param event_name: The name of the event to search for.
    :return: The event_id if found, otherwise None.
    """
    if event_name is None:
        raise ValueError("Event name must be provided to retrieve the event ID.")

    with sqlite3.connect(EVENTS_DATABASE) as conn:
        cursor = conn.cursor()

        # Fetch the event_id based on the event name
        cursor.execute('SELECT id FROM events WHERE name = ?', (event_name,))
        event_id = cursor.fetchone()

        if event_id:
            return event_id[0]  # Return the event_id from the fetched result
        else:
            print(f"No event found with the name '{event_name}'.")
            return None


async def delete_event_by_id(event_id: int):
    """
    Delete an event from the events table based on the event_id.

    :param event_id: The ID of the event to be deleted.
    """
    try:
        # Connect to the SQLite database
        with sqlite3.connect(EVENTS_DATABASE) as conn:
            cursor = conn.cursor()
            
            # Execute the DELETE statement
            cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
            
            # Commit the transaction
            conn.commit()
            
            # Check if any row was deleted
            if cursor.rowcount == 0:
                print(f"No event found with id {event_id}.")
            else:
                print(f"Event with id {event_id} deleted successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


# Temp_events code
async def create_temp_event_table():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(EVENTS_DATABASE)
    cursor = conn.cursor()

    # Create the events table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS temp_events (
        chat_id INTEGER PRIMARY KEY,
        id INTEGER,
        name TEXT ,
        number_of_days INTEGER,
        date_time TEXT,
        venue TEXT,
        audience_size INTEGER ,
        type TEXT CHECK(type IN ('Tech', 'Non-Tech')),
        club_id INTEGER
    )
    ''')

    # Commit changes and close the connection
    conn.commit()

async def store_temp_event_info(chat_id=None,event_id=None, name=None, number_of_days=None, date_time=None, venue=None, audience_size=None, type=None,club_id = None):
    """
    Insert a new event into the database, or update an existing one if the ID is provided.
    
    Parameters:
        event_id (int, optional): The ID of the event to update. If None, a new event will be inserted.
        name (str, optional): The name of the event.
        number_of_days (int, optional): The number of days for the event.
        date_time (str, optional): The date and time of the event in 'DD:MM:YYY/HH:MM:SS' format.
        venue (str, optional): The venue of the event.
        audience_size (int, optional): The estimated audience size for the event.
        type (str, optional): The type of the event ('Tech' or 'Non-Tech').
    """
    # try:
    with sqlite3.connect(EVENTS_DATABASE) as conn:
        cursor = conn.cursor()
        
        # Check if an event with the provided chat_id already exists
        cursor.execute('SELECT * FROM temp_events WHERE chat_id = ?', (chat_id,))
        existing_data = cursor.fetchone()
        
        if existing_data:
            # Update existing event record
            if event_id is not None:
                cursor.execute('UPDATE temp_events SET id = ? WHERE chat_id = ?', (event_id, chat_id))
            if name is not None:
                cursor.execute('UPDATE temp_events SET name = ? WHERE chat_id = ?', (name, chat_id))
            if number_of_days is not None:
                cursor.execute('UPDATE temp_events SET number_of_days = ? WHERE chat_id = ?', (int(number_of_days), chat_id))
            if date_time is not None:
                cursor.execute('UPDATE temp_events SET date_time = ? WHERE chat_id = ?', (date_time, chat_id))
            if venue is not None:
                cursor.execute('UPDATE temp_events SET venue = ? WHERE chat_id = ?', (venue, chat_id))
            if audience_size is not None:
                cursor.execute('UPDATE temp_events SET audience_size = ? WHERE chat_id = ?', (audience_size, chat_id))
            if type is not None:
                cursor.execute('UPDATE temp_events SET type = ? WHERE chat_id = ?', (type, chat_id))
            if club_id is not None:
                cursor.execute('UPDATE temp_events SET club_id = ? WHERE chat_id = ?',(club_id,chat_id))
        else:
            # Insert new event record
            cursor.execute('''
            INSERT INTO temp_events (chat_id, id, name, number_of_days, date_time, venue, audience_size, type, club_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                chat_id,
                event_id,
                name,
                number_of_days,
                date_time,
                venue,
                audience_size,
                type,
                club_id
            ))
            print(await retrieve_temp_event_info_by_chat_id(chat_id))
        # Commit the transaction
        conn.commit()

    # except Exception as e:
    #     print(f"Error while storing event values to the database: {e}")

async def retrieve_temp_event_info_by_chat_id(chat_id):
    """
    Retrieve event information from the temp_events table based on the chat_id.
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(EVENTS_DATABASE)
        cursor = conn.cursor()

        # Execute the query with parameterized input to prevent SQL injection
        cursor.execute("SELECT * FROM temp_events WHERE chat_id = ?", (chat_id,))

        # Fetch the result
        row = cursor.fetchone()

        # Close the connection after fetching the data
        conn.close()

        return row

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

async def check_temp_event_field_presence(chat_id):
    """
    Check the presence of each field for the given event ID and return a dictionary with True/False for each field.
    
    :param id: The unique identifier for the event.
    :return: A dictionary indicating the presence of each field.
    """
    try:
        with sqlite3.connect(EVENTS_DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM temp_events WHERE chat_id = ?', (chat_id,))
            result = cursor.fetchone()
            if result:
                # Unpack the result tuple
                _,temp_id, name, number_of_days, date_time, venue, audience_size, type_, club_id = result
                
                # Create the dictionary based on the presence of each field
                return {
                    'name': name is not None,
                    'number_of_days': number_of_days is not None,
                    'date_time': date_time is not None,
                    'venue': venue is not None,
                    'audience_size': audience_size is not None,
                    'type': type_ is not None,
                }
            else:
                # Handle the case where the ID is not found
                return {
                    'name': False,
                    'number_of_days': False,
                    'date_time': False,
                    'venue': False,
                    'audience_size': False,
                    'type': False,
                }
    except Exception as e:
        print(f"Error while checking event field presence: {e}")
        return {
            'name': False,
            'number_of_days': False,
            'date_time': False,
            'venue': False,
            'audience_size': False,
            'type': False,
        }

async def get_club_id_by_chat_id_from_temp_events(chat_id):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(EVENTS_DATABASE)
        cursor = conn.cursor()

        # Query to get club_id by chat_id
        cursor.execute('SELECT club_id FROM temp_events WHERE chat_id = ?', (chat_id,))
        result = cursor.fetchone()

        # Close the connection
        conn.close()

        # Check if result was found
        if result:
            return result[0]  # Return the club_id
        else:
            print(f"No club_id found for chat_id {chat_id}")
            return None
    except Exception as e:
        print(f"Error retrieving club_id by chat_id: {e}")
        return None

async def delete_temp_event_by_chat_id(chat_id):
    """
    Delete an event from the temp_events table based on the given chat_id.
    
    :param chat_id: The unique identifier for the event to be deleted.
    """
    
    try:
        with sqlite3.connect(EVENTS_DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM temp_events WHERE chat_id = ?', (chat_id,))
            
            # Check if any row was deleted
            if cursor.rowcount == 0:
                print(f"No event found with chat_id {chat_id}.")
            else:
                print(f"Event with chat_id {chat_id} has been deleted.")
            
            conn.commit()
    except Exception as e:
        print(f"Error while deleting event with chat_id {chat_id}: {e}")

# Event Data

async def create_table_event_data():
    """
    Creates a table in the EVENTS_DATABASE with the following columns:
    - event_id: INTEGER (manually assigned ID for each event)
    - reporter_name: TEXT (name of the person reporting the event)
    - reporter_number: TEXT (contact number of the reporter)
    - photos_link: TEXT (link to the event's photos)
    - event_report: TEXT (date stored, status updated as "submitted" or "not_submitted")
    - proposal_form: TEXT (date stored, status updated as "submitted" or "not_submitted")
    - flyer_and_schedule: TEXT (date stored, status updated as "submitted" or "not_submitted")
    - list_of_participants: TEXT (date stored, status updated as "submitted" or "not_submitted")
    """
    with sqlite3.connect(EVENTS_DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS event_data (
                event_id INTEGER PRIMARY KEY,
                reporter_name TEXT,
                reporter_number TEXT,
                photos_link TEXT,
                event_report TEXT,         -- Stores date and submission status
                proposal_form TEXT,        -- Stores date and submission status
                flyer_and_schedule TEXT,   -- Stores date and submission status
                list_of_participants TEXT  -- Stores date and submission status
            )
        ''')
        conn.commit()

async def store_or_update_event_data(event_id, reporter_name=None, reporter_number=None, photos_link=None, 
                                     event_report=None, proposal_form=None, flyer_and_schedule=None, list_of_participants=None):
    """
    Adds a new event record or updates an existing one in the event_data table.

    :param event_id: The manually assigned ID of the event.
    :param reporter_name: The name of the individual reporting the event.
    :param reporter_number: The contact number for the reporter.
    :param photos_link: A link to the event's photos, formatted as "dd/mm/yy-status-link.
    :param event_report: The status and date of the event report (e.g., 'submitted' or 'not_submitted'), formatted as "dd/mm/yyyy-status".
    :param proposal_form: The status and date of the proposal form (e.g., 'submitted' or 'not_submitted'), formatted as "dd/mm/yyyy-status".
    :param flyer_and_schedule: The status and date of the flyer and schedule (e.g., 'submitted' or 'not_submitted'), formatted as "dd/mm/yyyy-status".
    :param list_of_participants: The status and date of the participants' list (e.g., 'submitted' or 'not_submitted'), formatted as "dd/mm/yyyy-status".
    """


    with sqlite3.connect(EVENTS_DATABASE) as conn:
        cursor = conn.cursor()

        # Check if the event with the given event_id already exists
        cursor.execute('SELECT * FROM event_data WHERE event_id = ?', (event_id,))
        existing_data = cursor.fetchone()

        if existing_data:
            # Update the existing event details
            if reporter_name is not None:
                cursor.execute('UPDATE event_data SET reporter_name = ? WHERE event_id = ?', (reporter_name, event_id))
            if reporter_number is not None:
                cursor.execute('UPDATE event_data SET reporter_number = ? WHERE event_id = ?', (reporter_number, event_id))
            if photos_link is not None:
                cursor.execute('UPDATE event_data SET photos_link = ? WHERE event_id = ?', (photos_link, event_id))
            if event_report is not None:
                cursor.execute('UPDATE event_data SET event_report = ? WHERE event_id = ?', (event_report, event_id))
            if proposal_form is not None:
                cursor.execute('UPDATE event_data SET proposal_form = ? WHERE event_id = ?', (proposal_form, event_id))
            if flyer_and_schedule is not None:
                cursor.execute('UPDATE event_data SET flyer_and_schedule = ? WHERE event_id = ?', (flyer_and_schedule, event_id))
            if list_of_participants is not None:
                cursor.execute('UPDATE event_data SET list_of_participants = ? WHERE event_id = ?', (list_of_participants, event_id))
        else:
            # Insert a new event record
            cursor.execute('''
                INSERT INTO event_data (event_id, reporter_name, reporter_number, photos_link, 
                                        event_report, proposal_form, flyer_and_schedule, list_of_participants)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (event_id, reporter_name, reporter_number, photos_link, event_report, proposal_form, flyer_and_schedule, list_of_participants))

        conn.commit()  # Commit the changes

async def delete_event_data(event_id):
    """
    Deletes an event record from the event_data table based on the event_id.

    :param event_id: The ID of the event to be deleted.
    """
    if event_id is None:
        raise ValueError("event_id must be provided to delete an event record.")
    
    with sqlite3.connect(EVENTS_DATABASE) as conn:
        cursor = conn.cursor()

        # Check if the event with the given ID exists
        cursor.execute('SELECT * FROM event_data WHERE event_id = ?', (event_id,))
        existing_data = cursor.fetchone()

        if existing_data:
            # Delete the event record
            cursor.execute('DELETE FROM event_data WHERE event_id = ?', (event_id,))
            conn.commit()
            print(f"Event with ID {event_id} has been deleted.")
        else:
            raise ValueError(f"No event found with ID {event_id}.")

async def retrieve_event_data(event_id):
    """
    Retrieves an event record from the event_data table based on the event_id.

    :param event_id: The ID of the event to retrieve.
    :return: A dictionary with the event data if found, otherwise None.
    """
    if event_id is None:
        raise ValueError("event_id must be provided to retrieve an event record.")

    with sqlite3.connect(EVENTS_DATABASE) as conn:
        cursor = conn.cursor()

        # Fetch the event data based on event_id
        cursor.execute('SELECT * FROM event_data WHERE event_id = ?', (event_id,))
        event_data = cursor.fetchone()

        if event_data:
            # Assuming the order of columns is:
            # event_id, reporter_name, reporter_number, photos_link, event_report, proposal_form,
            # flyer_and_schedule, list_of_participants
            return {
                'event_id': event_data[0],
                'reporter_name': event_data[1],
                'reporter_number': event_data[2],
                'photos_link': event_data[3],
                'event_report': event_data[4],  # Could be 'submitted' or 'not_submitted'
                'proposal_form': event_data[5],  # Could be 'submitted' or 'not_submitted'
                'flyer_and_schedule': event_data[6],  # Could be 'submitted' or 'not_submitted'
                'list_of_participants': event_data[7]  # Could be 'submitted' or 'not_submitted'
            }
        else:
            print(f"No event found with ID {event_id}.")
            return None



# Permissions code

async def create_permissions_table():
    conn = sqlite3.connect(PERMISSIONS_DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS permissions (
            chat_id INTEGER PRIMARY KEY,
            events BOOLEAN NOT NULL,
            clubs BOOLEAN NOT NULL,
            edit_clubs TEXT,
            edit_events TEXT,
            proposal_form TEXT,
            flyer TEXT,
            core_team BOOLEAN NOT NULL,
            core_team_edit TEXT,
            council_admin BOOLEAN NOT NULL,
            enforcement_team BOOLEAN NOT NULL,
            photos_drive_link TEXT,
            reporter_details TEXT,
            report_upload TEXT,
            list_of_participants TEXT,
            core_team_tasks TEXT
        )
    ''')

    conn.commit()
    conn.close()

async def initialize_permissions(chat_id):
    conn = sqlite3.connect(PERMISSIONS_DATABASE)
    cursor = conn.cursor()

    # Insert default values (False or NULL) for the given chat_id
    cursor.execute('''
        INSERT INTO permissions (
            chat_id, events, clubs, edit_clubs, edit_events, 
            proposal_form, flyer, core_team, core_team_edit, 
            council_admin, enforcement_team, photos_drive_link, 
            reporter_details, report_upload, list_of_participants, core_team_tasks
        ) 
        VALUES (?, 0, 0, NULL, NULL, NULL, NULL, 0, NULL, 0, 0, NULL, NULL, NULL, NULL)
    ''', (chat_id,))

    conn.commit()
    conn.close()


async def set_permissions(
    chat_id,
    events=False,
    clubs=False,
    edit_clubs=None,
    edit_events=None,
    proposal_form=None,
    flyer=None,
    core_team=False,
    edit_core=None,
    council_admin=False,
    enforcement_team=False,
    photos_drive_link=None,
    reporter_details=None,
    report_upload=None,
    list_of_participants=None,
    core_team_tasks=None
):
    conn = sqlite3.connect(PERMISSIONS_DATABASE)
    cursor = conn.cursor()

    # Check if the chat_id already exists
    cursor.execute('''
        SELECT chat_id FROM permissions WHERE chat_id = ?
    ''', (chat_id,))
    
    result = cursor.fetchone()

    if result is None:
        # Insert a new record if chat_id doesn't exist
        cursor.execute('''
            INSERT INTO permissions (
                chat_id, events, clubs, edit_clubs, edit_events, 
                proposal_form, flyer, core_team, core_team_edit, 
                council_admin, enforcement_team, photos_drive_link, 
                reporter_details, report_upload, list_of_participants, core_team_tasks
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            chat_id, events, clubs, edit_clubs, edit_events, 
            proposal_form, flyer, core_team, edit_core, 
            council_admin, enforcement_team, photos_drive_link, 
            reporter_details, report_upload, list_of_participants, core_team_tasks
        ))
    else:
        # Update the existing record if chat_id exists
        cursor.execute('''
            UPDATE permissions
            SET events = ?, clubs = ?, edit_clubs = ?, edit_events = ?, 
                proposal_form = ?, flyer = ?, core_team = ?, core_team_edit = ?, 
                council_admin = ?, enforcement_team = ?, photos_drive_link = ?, 
                reporter_details = ?, report_upload = ?, list_of_participants = ?, core_team_tasks = ?
            WHERE chat_id = ?
        ''', (
            events, clubs, edit_clubs, edit_events, 
            proposal_form, flyer, core_team, edit_core, 
            council_admin, enforcement_team, photos_drive_link, 
            reporter_details, report_upload, list_of_participants, core_team_tasks, chat_id
        ))

    conn.commit()
    conn.close()


async def check_permission(
    chat_id,
    events=False,
    clubs=False,
    edit_clubs=False,
    edit_events=False,
    proposal_form=False,
    flyer=False,
    core_team=False,
    edit_core=False,
    council_admin=False,
    enforcement_team=False,
    photos_drive_link=False,
    reporter_details=False,
    report_upload=False,
    list_of_participants=False,
    core_team_tasks=False  # Added core_team_tasks as a parameter
):
    with sqlite3.connect(PERMISSIONS_DATABASE) as conn:
        cursor = conn.cursor()

        # Fetch the permissions for the given chat_id
        cursor.execute('''
            SELECT events, clubs, edit_clubs, edit_events, proposal_form, 
                   flyer, core_team, core_team_edit, council_admin, 
                   enforcement_team, photos_drive_link, 
                   reporter_details, report_upload, list_of_participants, core_team_tasks
            FROM permissions WHERE chat_id = ?
        ''', (chat_id,))
        
        result = cursor.fetchone()

        if result is None:
            return None  # Return None if the chat_id is not found

        # Unpack the result
        (db_events, db_clubs, db_edit_clubs, db_edit_events, db_proposal_form,
         db_flyer, db_core_team, db_core_team_edit, db_council_admin,
         db_enforcement_team, db_photos_drive_link, db_reporter_details,
         db_report_upload, db_list_of_participants, db_core_team_tasks) = result

        # Check based on which parameter is True and return the corresponding value
        if events:
            return bool(db_events)
        elif clubs:
            return bool(db_clubs)
        elif edit_clubs:
            return db_edit_clubs
        elif edit_events:
            return db_edit_events
        elif proposal_form:
            return db_proposal_form
        elif flyer:
            return db_flyer
        elif core_team:
            return bool(db_core_team)
        elif edit_core:
            return db_core_team_edit
        elif council_admin:
            return bool(db_council_admin)
        elif enforcement_team:
            return bool(db_enforcement_team)
        elif photos_drive_link:
            return db_photos_drive_link
        elif reporter_details:
            return db_reporter_details
        elif report_upload:
            return db_report_upload
        elif list_of_participants:
            return db_list_of_participants
        elif core_team_tasks:  # Check for core_team_tasks
            return db_core_team_tasks

    return None



# # Admins code

# async def create_admins_table():
#     """
#     Create the necessary table for storing admins information in the SQLite database.
#     """
#     with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
#         cursor = conn.cursor()
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS admins (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 name TEXT,
#                 description TEXT,
#                 dean TEXT,
#                 dean_chat_id INTEGER,
#                 president TEXT,
#                 prdnt_chat_id INTEGER,
#                 vice_president TEXT,
#                 vice_prdnt_chat_id INTEGER
#                 meeting_schedule TEXT,       -- To store meeting details
#                 tasks TEXT,                  -- To store assigned tasks in JSON or CSV format
#                 calendar_privileges TEXT      -- To store calendar permissions (read/write)
#             )
#         """)
#         conn.commit()

# async def store_club_info(admin_id, name, description=None, president=None, vice_president=None
#                            , meeting_schedule=None, tasks=None, calendar_privileges='read'):
#     """
#     Store club information in the database. If the club already exists, update the information; otherwise, insert a new record.
#     :param club_id: The ID of the club (for updating; use None for new records).
#     :param name: The name of the club (required for both new and existing records).
#     :param description: A description of the club.
#     :param president: The name of the president.
#     :param vice_president: The name of the vice president.
#     :param meeting_schedule: A list of meeting details (optional).
#     :param tasks: A list of tasks (optional).
#     :param calendar_privileges: Calendar privileges (default: 'read').
#     """
    
#     with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
#         cursor = conn.cursor()
#         if admin_id is not None:
#             # Update existing record
#             cursor.execute('SELECT * FROM admins WHERE id = ?', (admin_id,))
#             existing_data = cursor.fetchone()
            
#             if existing_data:
#                 if name is not None:
#                     cursor.execute('UPDATE admins SET name = ? WHERE id = ?', (name, admin_id))
#                 if description is not None:
#                     cursor.execute('UPDATE admins SET description = ? WHERE id = ?', (description, admin_id))
#                 if president is not None:
#                     cursor.execute('UPDATE admins SET president = ? WHERE id = ?', (president, admin_id))
#                 if vice_president is not None:
#                     cursor.execute('UPDATE admins SET vice_president = ? WHERE id = ?', (vice_president, admin_id))
#                 if meeting_schedule is not None:
#                     cursor.execute('UPDATE admins SET meeting_schedule = ? WHERE id = ?', (json.dumps(meeting_schedule), admin_id))
#                 if tasks is not None:
#                     cursor.execute('UPDATE admins SET tasks = ? WHERE id = ?', (json.dumps(tasks), admin_id))
#                 if calendar_privileges is not None:
#                     cursor.execute('UPDATE admins SET calendar_privileges = ? WHERE id = ?', (calendar_privileges, admin_id))
#             else:
#                 raise ValueError("Club ID does not exist for update.")
#         else:
#             # Insert new record
#             cursor.execute('INSERT INTO admins (name, description, president, vice_president, meeting_schedule, tasks, calendar_privileges) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
#                            (name, description, president, vice_president, json.dumps(meeting_schedule or []), json.dumps(tasks or []), calendar_privileges))
#         conn.commit()


# Core team code

async def create_core_team_table():
    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS core_team (
                core_member_index INTEGER PRIMARY KEY AUTOINCREMENT,
                core_name TEXT,
                core_member_name TEXT,
                core_member_chat_id INTEGER,
                tasks TEXT
            )
        ''')
        conn.commit()

async def store_core_team_info(core_team_index=None, core_name=None, core_member_name=None, core_member_chat_id=None,tasks = None):
    """
    Store or update core team information in the database. If the core team member already exists, update the information;
    otherwise, insert a new record.

    :param core_team_index: The index of the core team member (for updating; use None for new records).
    :param core_name: The name of the core (e.g., department, team).
    :param core_member_name: The name of the core team member.
    :param core_member_chat_id: The chat ID of the core team member.
    :param tasks: Tasks of the core member (dictionary).
    """
    
    # if core_member_name is None or core_member_chat_id is None or core_name is None:
    #     raise ValueError("core_name, core_member_name, and core_member_chat_id must all be provided.")

    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.cursor()

        if core_team_index is not None:
            # Update existing core team member
            cursor.execute('SELECT * FROM core_team WHERE core_member_index = ?', (core_team_index,))
            existing_data =cursor.fetchone()

            if existing_data:
                if core_name is not None:
                    cursor.execute('UPDATE core_team SET core_name = ? WHERE core_member_index = ?', (core_name, core_team_index))
                if core_member_name is not None:
                    cursor.execute('UPDATE core_team SET core_member_name = ? WHERE core_member_index = ?', (core_member_name, core_team_index))
                if core_member_chat_id is not None:
                    cursor.execute('UPDATE core_team SET core_member_chat_id = ? WHERE core_member_index = ?', (core_member_chat_id, core_team_index))
                if tasks is not None:
                    cursor.execute('UPDATE core_team SET tasks = ? WHERE core_member_index = ?', (tasks, core_team_index))
        else:
            # Insert new core team member
            cursor.execute('''
                INSERT INTO core_team (core_name, core_member_name, core_member_chat_id)
                VALUES (?, ?, ?)
            ''', (core_name, core_member_name, core_member_chat_id))


async def delete_core_team_member_by_chat_id(core_member_chat_id):
    """
    Delete a core team member from the database based on their chat ID.
    
    :param core_member_chat_id: The chat ID of the core team member to be deleted.
    """
    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.cursor()
        
        # Check if the member exists before attempting to delete
        cursor.execute('SELECT * FROM core_team WHERE core_member_chat_id = ?', (core_member_chat_id,))
        existing_data = cursor.fetchone()
        
        if existing_data:
            cursor.execute('DELETE FROM core_team WHERE core_member_chat_id = ?', (core_member_chat_id,))
            conn.commit()
            print(f"Core team member with chat ID {core_member_chat_id} has been deleted.")
        else:
            raise ValueError(f"No core team member found with chat ID {core_member_chat_id}.")
        
async def get_all_core_team_members():
    """
    Retrieve all core team members from the database.
    
    :return: A list of tuples, each representing a core team member's data.
    example_data : [
    (1,"Cultural Head", "John Doe", 123456789,"Tasks_assigned"),
    (2,"Logistics Head", "Jane Smith", 987654321,"Tasks_assigned")
]
    """
    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM core_team')
        core_team_members = cursor.fetchall()
        
        return core_team_members

async def get_core_member_details(core_member_id, core_name=False, core_member_name=False, core_member_chat_id=False, tasks=False):
    """
    Fetch specific details of a core team member by their core_member_id, based on the parameters set to True.
    
    :param core_member_id: The ID of the core team member to be retrieved.
    :param core_name: Whether to return the core name.
    :param core_member_name: Whether to return the core member name.
    :param core_member_chat_id: Whether to return the core member chat ID.
    :param tasks: Whether to return the tasks.
    :return: A dictionary containing the requested details.
    """
    try:
        # Connect to the database
        with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
            cursor = conn.cursor()

            # Retrieve the core member information based on the ID
            cursor.execute('SELECT core_name, core_member_name, core_member_chat_id, tasks FROM core_team WHERE core_member_index = ?', (core_member_id,))
            core_member = cursor.fetchone()

            if not core_member:
                print(f"No core member found with ID {core_member_id}.")
            
            # Unpack the result
            core_name_val, core_member_name_val, core_member_chat_id_val, tasks_val = core_member

            # Prepare the dictionary to hold the selected values
            selected_details = {}

            if core_name:
                selected_details['core_name'] = core_name_val
            if core_member_name:
                selected_details['core_member_name'] = core_member_name_val
            if core_member_chat_id:
                selected_details['core_member_chat_id'] = core_member_chat_id_val
            if tasks:
                selected_details['tasks'] = tasks_val

            # Return the selected details
            return selected_details if selected_details else "No parameters were selected to return."
    
    except Exception as e:
        print(f"An error occurred while fetching core member details: {e}")

async def get_core_member_chat_ids():
    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.cursor()

        # Fetch core_member_chat_id from the core_team table
        cursor.execute('SELECT core_member_chat_id FROM core_team')
        chat_ids = cursor.fetchall()  # Fetch all results

    # Flatten the list of tuples into a single list
    return [chat_id[0] for chat_id in chat_ids]


async def get_all_core_tasks_and_ids():
    """
    Retrieve all core member indexes and their tasks from the core_team table.

    Returns:
    - List[Tuple[int, str]]: A list of tuples containing core member chat IDs and tasks.
    """
    # Connect to the SQLite database
    connection = sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE)
    cursor = connection.cursor()
    
    try:
        # Execute the query to fetch core member chat IDs and tasks
        cursor.execute('''
            SELECT core_member_index, tasks 
            FROM core_team
        ''')
        
        # Fetch all rows from the result
        result = cursor.fetchall()
        
    finally:
        # Close the database connection
        connection.close()
    
    return result

async def get_core_info_by_id(core_member_id):
    """
    Retrieve core team member information by their ID.

    :param core_member_id: The ID of the core team member to retrieve.
    :returns: A tuple containing core_name, core_member_name, core_member_chat_id if found; otherwise None.
    """
    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT core_name, core_member_name, core_member_chat_id,tasks
            FROM core_team
            WHERE core_member_index = ?
        ''', (core_member_id,))
        
        # Fetch the result
        result = cursor.fetchone()

    # Return the result or None if no match is found
    return result

async def get_core_member_info_by_chat_id(core_member_chat_id):
    """
    Retrieves core team member information based on their chat ID.

    :param core_member_chat_id: The chat ID of the core team member.
    :return: A dictionary with the core team member's data if found, otherwise None.
    """
    if core_member_chat_id is None:
        raise ValueError("core_member_chat_id must be provided to retrieve core member information.")

    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.cursor()

        # Fetch the core team member data based on core_member_chat_id
        cursor.execute('SELECT * FROM core_team WHERE core_member_chat_id = ?', (core_member_chat_id,))
        core_member_data = cursor.fetchone()

        if core_member_data:
            # Assuming the order of columns is: core_member_index, core_name, core_member_name, core_member_chat_id, tasks
            return {
                'core_member_index': core_member_data[0],
                'core_name': core_member_data[1],
                'core_member_name': core_member_data[2],
                'core_member_chat_id': core_member_data[3],
                'tasks': core_member_data[4]
            }
        else:
            print(f"No core member found with chat ID {core_member_chat_id}.")
            return None


async def delete_core_member_by_index(core_member_index):
    """
    Deletes a core member from the core_team table using the core_member_index.
    
    :param core_member_index: The index of the core member to be deleted.
    :return: A message indicating whether the deletion was successful.
    """

    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.cursor()
        # Retrieve the core_name of the member to be deleted
        cursor.execute('SELECT core_name FROM core_team WHERE core_member_index = ?', (core_member_index,))
        core_details = cursor.fetchone()
        if core_details:
            # Delete the core member from the table
            cursor.execute('DELETE FROM core_team WHERE core_member_index = ?', (core_member_index,))
            conn.commit()
            return True


# Temporary Core team code

async def create_temp_core_team_table():
    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS temp_core_team (
                chat_id INTEGER PRRIMARY KEY,
                core_member_id INTEGER,
                core_name TEXT,
                core_member_name TEXT,
                core_member_chat_id INTEGER,
                tasks TEXT
            )
        ''')
        conn.commit()

async def store_temp_core_team_info(chat_id=None,core_member_id=None, core_name=None, core_member_name=None, core_member_chat_id=None,tasks = None):
    """
    Store or update core team information temporarily in the database. If the core team member already exists, update the information;
    otherwise, insert a new record.

    :param chat_id: The chat_id of the current person.
    :param core_member_id: The ID of the core team member.
    :param core_name: The name of the core (e.g., department, team).
    :param core_member_name: The name of the core team member.
    :param core_member_chat_id: The chat ID of the core team member.
    :param tasks: Tasks of the core member.
    """

    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.cursor()

        if chat_id is not None:
            # Check if the core team member exists
            cursor.execute('SELECT * FROM temp_core_team WHERE chat_id = ?', (chat_id,))
            existing_data = cursor.fetchone()

            if existing_data:
                # Update existing core team member data
                if core_member_id is not None:
                    cursor.execute('UPDATE temp_core_team SET core_member_id = ? WHERE chat_id = ?', (core_member_id, chat_id))
                if core_name is not None:
                    cursor.execute('UPDATE temp_core_team SET core_name = ? WHERE chat_id = ?', (core_name, chat_id))
                if core_member_name is not None:
                    cursor.execute('UPDATE temp_core_team SET core_member_name = ? WHERE chat_id = ?', (core_member_name, chat_id))
                if core_member_chat_id is not None:
                    cursor.execute('UPDATE temp_core_team SET core_member_chat_id = ? WHERE chat_id = ?', (core_member_chat_id, chat_id))
                if tasks is not None:
                    cursor.execute('UPDATE temp_core_team SET tasks = ? WHERE chat_id = ?', (tasks, chat_id))
            else:
                # Insert new core team member
                cursor.execute('''
                    INSERT INTO temp_core_team (chat_id, core_member_id, core_name, core_member_name, core_member_chat_id, tasks)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (chat_id, core_member_id, core_name, core_member_name, core_member_chat_id, tasks))

async def retrieve_temp_core_info_by_chat_id(chat_id):
    """
    Retrieve temporary core team information based on chat_id.

    :param chat_id: The chat ID to search for in the temporary core team table.
    :return: A tuple containing the temporary chat ID, core name, core member name, and core member chat ID.
    """
    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.cursor()
        
        # Query to retrieve temporary core information
        cursor.execute('''
            SELECT chat_id, core_name, core_member_name, core_member_chat_id
            FROM temp_core_team
            WHERE chat_id = ?
        ''', (chat_id,))
        
        # Fetch one record
        result = cursor.fetchone()
        
        # Return the result or None if no record is found
        return result if result is not None else None

async def delete_temp_core_team_member_by_user_chat_id(user_chat_id):
    """
    Delete a core team member from the database based on their chat ID.
    
    :param user_chat_id: The chat ID of the user to be deleted.
    """
    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.cursor()
        
        # Check if the member exists before attempting to delete
        cursor.execute('SELECT * FROM temp_core_team WHERE chat_id = ?', (user_chat_id,))
        existing_data = cursor.fetchone()
        
        if existing_data:
            cursor.execute('DELETE FROM temp_core_team WHERE chat_id = ?', (user_chat_id,))
            conn.commit()
            print(f"Core team member with chat ID {user_chat_id} has been deleted.")
        else:
            raise ValueError(f"No core team member found with chat ID {user_chat_id}.")

async def check_temp_core_team_field_presence(chat_id):
    """
    Check the presence of each field for the given chat_id and return a dictionary with True/False for each field.
    
    :param chat_id: The unique identifier for the core team member.
    :return: A dictionary indicating the presence of each field.
    """
    
    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM temp_core_team WHERE chat_id = ?', (chat_id,))
        result = cursor.fetchone()
        
        if result:
            # Unpack the result tuple
            _,_, core_name,core_member_name, core_member_chat_id,tasks = result
            
            # Create the dictionary based on the presence of each field
            return {
                'core_name' : core_name is not None,
                'core_member_name': core_member_name is not None,
                'core_member_chat_id': core_member_chat_id is not None,
            }
        else:
            # Handle the case where the chat_id is not found
            return {
                'core_name' : False,
                'core_member_name': False,
                'core_member_chat_id': False,
            }
        
# Student Council Team Code


async def create_student_council_table():
    """
    Creates a table for student council members with columns:
    - chat_id (INTEGER PRIMARY KEY)
    - Name (TEXT)
    - dean (BOOLEAN)
    - president (BOOLEAN)
    - vice_president (BOOLEAN)
    """
    conn = sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE)  # Connect to the SQLite database (or create it)
    cursor = conn.cursor()  # Create a cursor object to interact with the database

    # Create the student_council table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_council (
            chat_id INTEGER PRIMARY KEY,
            Name TEXT,
            dean BOOLEAN NOT NULL DEFAULT 0,
            president BOOLEAN NOT NULL DEFAULT 0,
            vice_president BOOLEAN NOT NULL DEFAULT 0
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()

async def store_student_council_info(chat_id=None, name=None, dean=None, president=None, vice_president=None):
    """
    Store or update student council member information in the database. 
    If the member already exists, update the information; otherwise, insert a new record.

    :param chat_id: The chat_id of the member.
    :param name: The name of the member.
    :param dean: Whether the member is a dean (BOOLEAN).
    :param president: Whether the member is a president (BOOLEAN).
    :param vice_president: Whether the member is a vice president (BOOLEAN).
    """

    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.cursor()

        if chat_id is not None:
            # Update existing student council member
            cursor.execute('SELECT * FROM student_council WHERE chat_id = ?', (chat_id,))
            existing_data = cursor.fetchone()

            if existing_data:
                if name is not None:
                    cursor.execute('UPDATE student_council SET Name = ? WHERE chat_id = ?', (name, chat_id))
                if dean is not None:
                    cursor.execute('UPDATE student_council SET dean = ? WHERE chat_id = ?', (dean, chat_id))
                if president is not None:
                    cursor.execute('UPDATE student_council SET president = ? WHERE chat_id = ?', (president, chat_id))
                if vice_president is not None:
                    cursor.execute('UPDATE student_council SET vice_president = ? WHERE chat_id = ?', (vice_president, chat_id))
            # else:
                # raise ValueError("Student council member does not exist for update.")
            else:
                # Insert new student council member
                # cursor.execute('''
                #     INSERT INTO student_council (chat_id, Name, dean, president, vice_president)
                #     VALUES (?, ?, ?, ?, ?)
                # ''', (chat_id, name, dean, president, vice_president))
                cursor.execute('''
                    INSERT INTO student_council (chat_id)
                    VALUES (?)
                ''', (chat_id,))

        conn.commit()
async def delete_student_council_member(chat_id):
    """
    Deletes a student council member from the database based on chat_id.

    :param chat_id: The chat_id of the member to be deleted.
    """
    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.cursor()

        # Delete the member with the specified chat_id
        cursor.execute('DELETE FROM student_council WHERE chat_id = ?', (chat_id,))
        
        # Commit the changes
        conn.commit()

async def check_student_council_field_presence(chat_id):
    """
    Check the presence of each field for the given chat_id in the student council table
    and return a dictionary indicating the presence of each role.

    :param chat_id: The unique identifier for the student council member.
    :return: A dictionary indicating the presence of each role.
    """
    
    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM student_council WHERE chat_id = ?', (chat_id,))
        result = cursor.fetchone()
        
        if result:
            # Unpack the result tuple
            _, name, dean, president, vice_president = result
            
            # Create the dictionary based on the roles' presence
            return {
                'name': name is not None,
                'dean': bool(dean),  # Returns True if dean is True
                'president': bool(president),  # Returns True if president is True
                'vice_president': bool(vice_president),  # Returns True if vice president is True
                'any_position': bool(dean) or bool(president) or bool(vice_president),  # Returns True if any position is True
                'all_values' : bool(name) and (bool(dean) or bool(president) or bool(vice_president)) # Returns True if all the required values are present.
            }
        else:
            # Handle the case where the chat_id is not found
            return {
                'name': False,
                'dean': False,
                'president': False,
                'vice_president': False,
                'any_position': False,  # No roles assigned if the chat_id is not found
                'all_values' : False
            }

async def get_all_student_council_chat_ids():
    """
    Retrieve all chat_ids from the student council table.

    :return: A list of chat_ids from the student council table.
    """
    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT chat_id FROM student_council')
        
        # Fetch all chat_ids
        chat_ids = cursor.fetchall()
        
        # Extract chat_id values from tuples and return as a list
        return [chat_id[0] for chat_id in chat_ids]
    
async def get_student_council_member_details(chat_id):
    """
    Retrieves a student's information from the student_council table based on chat_id.
    Returns a dictionary with the Name, dean, president, and vice_president fields.
    """
    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT Name, dean, president, vice_president FROM student_council WHERE chat_id = ?', (chat_id,))
        row = cursor.fetchone()
        if row:
            # Unpack the row and return it as a dictionary
            name, dean, president, vice_president = row
            # Determine the position based on the flags
            if dean:
                position = 'dean'
            elif president:
                position = 'president'
            elif vice_president:
                position = 'vice_president'  # Default if none are true
            else: 
                return None # Handle case where no position is true.
            # Return the name and position as a dictionary
            return {
                'Name': name,
                'position': position
            }
        else:
            return None # Handle case where the chat_id doesn't exist

async def get_all_chat_ids():
    with sqlite3.connect(PERMISSIONS_DATABASE) as conn:
        cursor = conn.cursor()

        # Fetch all chat_ids from the student_council table
        cursor.execute('SELECT chat_id FROM student_council')
        chat_ids = cursor.fetchall()  # Fetch all results

    # Extract chat_ids from the tuples
    return [chat_id[0] for chat_id in chat_ids]

# Enforcement Team and Violations Code:

async def create_enforcement_team_table():
    """
    Creates a table for enforcement team members with the following columns:
    - chat_id (INTEGER PRIMARY KEY)
    - name (TEXT)
    """
    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS enforcement_team (
                chat_id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')
        conn.commit()  # Commit the changes after executing the query

async def create_violations_table():
    """
    Creates a table for violations with the following columns:
    - violation_id: Primary key, autoincrementing.
    - violation: Description of what violation has been committed.
    - club_name: Name of the club associated with the violation.
    - status: Current status of the violation (e.g., 'open', 'resolved').
    - timestamp: Date and time when the violation was recorded (Automatically Stores)(YYYY-MM-DD HH:MM:SS).
    """
    conn = sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS violations (
            violation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            violation TEXT NOT NULL,
            club_name TEXT NOT NULL,
            status TEXT NOT NULL,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            time_remaining INTEGER
        )
    ''')

    conn.commit()


async def store_enforcement_team_details(chat_id=None, name=None):
    """
    Stores or updates enforcement team details. If the member exists, update their information,
    otherwise insert a new record.

    :param chat_id: The chat ID of the enforcement team member.
    :param name: The name of the enforcement team member.
    """
    
    try:
        with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
            cursor = conn.cursor()

            if chat_id is not None:
                # Check if the enforcement team member already exists
                cursor.execute('SELECT * FROM enforcement_team WHERE chat_id = ?', (chat_id,))
                existing_data = cursor.fetchone()

                if existing_data:
                    # Update the existing enforcement team member's name
                    if name is not None:
                        cursor.execute('UPDATE enforcement_team SET name = ? WHERE chat_id = ?', (name, chat_id))
                else:
                    # Insert a new enforcement team member
                    cursor.execute('''
                        INSERT INTO enforcement_team (chat_id, name)
                        VALUES (?, ?)
                    ''', (chat_id, name))

            conn.commit()
            return True  # Return True on successful operation

    except Exception as e:
        print(f"Error storing or updating enforcement team member: {e}")
        return False  # Return False if an error occurred


async def delete_enforcement_team_member(chat_id):
    """
    Deletes a member from the enforcement_team table based on the chat_id.

    :param chat_id: The ID of the member to be deleted.
    """
    conn = sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE)
    cursor = conn.cursor()

    # Check if the member with the given chat_id exists
    cursor.execute('SELECT * FROM enforcement_team WHERE chat_id = ?', (chat_id,))
    existing_data = cursor.fetchone()

    if existing_data:
        # Delete the member
        cursor.execute('DELETE FROM enforcement_team WHERE chat_id = ?', (chat_id,))
        conn.commit()
        print(f"Enforcement team member with chat_id {chat_id} has been deleted.")
    else:
        raise ValueError(f"Member with chat_id {chat_id} does not exist.")

    conn.close()

async def get_enforcement_team_chat_ids():
    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.cursor()

        # Fetch chat_id from the enforcement_team table
        cursor.execute('SELECT chat_id FROM enforcement_team')
        chat_ids = cursor.fetchall()  # Fetch all results

    # Flatten the list of tuples into a single list
    return [chat_id[0] for chat_id in chat_ids]

async def get_enforcement_team_chat_ids_and_names():
    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT chat_id,name FROM enforcement_team')
        result =cursor.fetchall()
    return result


async def store_violation_details(violation_id=None, violation=None, club_name=None, status=None, time_remaining=None):
    """
    Stores a new violation or updates an existing violation record in the violations table.

    :param violation_id: The ID of the violation (for updating).
    :param violation: Description of the violation.
    :param club_name: The name of the club associated with the violation.
    :param status: The current status of the violation (e.g., 'open', 'resolved').
    :param time_remaining: Time left for the violation to be resolved (in minutes or desired unit).
    """
    conn = sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE)
    cursor = conn.cursor()

    if violation_id is not None:
        # Check if the violation with the given ID exists
        cursor.execute('SELECT * FROM violations WHERE violation_id = ?', (violation_id,))
        existing_data = cursor.fetchone()

        if existing_data:
            # Update the existing violation
            if violation is not None:
                cursor.execute('UPDATE violations SET violation = ? WHERE violation_id = ?', (violation, violation_id))
            if club_name is not None:
                cursor.execute('UPDATE violations SET club_name = ? WHERE violation_id = ?', (club_name, violation_id))
            if status is not None:
                cursor.execute('UPDATE violations SET status = ? WHERE violation_id = ?', (status, violation_id))
            if time_remaining is not None:
                cursor.execute('UPDATE violations SET time_remaining = ? WHERE violation_id = ?', (time_remaining, violation_id))
        else:
            raise ValueError(f"Violation with ID {violation_id} does not exist for update.")
    else:
        # Insert a new violation record
        cursor.execute('''
            INSERT INTO violations (violation, club_name, status, time_remaining)
            VALUES (?, ?, ?, ?)
        ''', (violation, club_name, status, time_remaining))

    conn.commit()
    conn.close()

async def delete_violation(violation_id):
    """
    Deletes a violation record from the violations table based on the violation_id.

    :param violation_id: The ID of the violation to be deleted.
    """
    conn = sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE)
    cursor = conn.cursor()

    # Check if the violation with the given ID exists
    cursor.execute('SELECT * FROM violations WHERE violation_id = ?', (violation_id,))
    existing_data = cursor.fetchone()

    if existing_data:
        # Delete the violation
        cursor.execute('DELETE FROM violations WHERE violation_id = ?', (violation_id,))
        conn.commit()
        print(f"Violation with ID {violation_id} has been deleted.")
    else:
        raise ValueError(f"Violation with ID {violation_id} does not exist.")

    conn.close()

async def get_enforcement_team_member(chat_id: int):
    """
    Retrieves a team member's details from the enforcement_team table based on chat_id.

    Args:
        chat_id (int): The chat ID of the team member.

    Returns:
        dict: A dictionary with keys 'chat_id' and 'name' if the member is found, otherwise None.
    """
    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.execute('''
            SELECT chat_id, name
            FROM enforcement_team
            WHERE chat_id = ?
        ''', (chat_id,))
        row = cursor.fetchone()
        return {'chat_id': row[0], 'name': row[1]} if row else None

async def retrieve_violations(status_filter: str = None):
    """
    Retrieves all violations from the violations table, optionally filtering by status.

    :param status_filter: Optional. If provided, only violations with the given status will be returned.
    :return: A list of dictionaries containing the violation records.
    """
    conn = sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE)
    cursor = conn.cursor()

    # Define the query to retrieve all violations
    query = "SELECT violation_id, violation, club_name, status, timestamp, time_remaining FROM violations"
    
    # If a status filter is provided, modify the query
    if status_filter:
        query += " WHERE status = ?"
        cursor.execute(query, (status_filter,))
    else:
        cursor.execute(query)

    violations = cursor.fetchall()

    # Convert the results to a list of dictionaries
    violation_list = []
    for violation in violations:
        violation_data = {
            'violation_id': violation[0],
            'violation': violation[1],
            'club_name': violation[2],
            'status': violation[3],
            'timestamp': violation[4],
            'time_remaining': violation[5]
        }
        violation_list.append(violation_data)

    conn.close()
    return violation_list

# Temp Enforcement team table.
async def create_temp_enforcement_team_table():
    """
    Creates a table for enforcement team members with the following columns:
    - chat_id (INTEGER PRIMARY KEY)
    - name (TEXT)
    """
    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS temp_enforcement_team (
                temp_chat_id INTEGER PRIMARY KEY,
                chat_id INTEGER,
                name TEXT
            )
        ''')
        conn.commit()

async def store_temp_enforcement_team_details(temp_chat_id=None, chat_id=None, name=None):
    """
    Stores or updates enforcement team details in the temporary table. 
    If the member exists, update their information; otherwise, insert a new record.

    :param temp_chat_id: The temporary chat ID of the enforcement team member.
    :param chat_id: The chat ID of the enforcement team member.
    :param name: The name of the enforcement team member.
    """
    
    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.cursor()

        if temp_chat_id is not None:
            # Check if the enforcement team member already exists
            cursor.execute('SELECT * FROM temp_enforcement_team WHERE temp_chat_id = ?', (temp_chat_id,))
            existing_data = cursor.fetchone()

            if existing_data:
                # Update the existing enforcement team member's name
                if name is not None:
                    cursor.execute('UPDATE temp_enforcement_team SET name = ? WHERE temp_chat_id = ?', (name, temp_chat_id))
                if chat_id is not None:
                    cursor.execute('UPDATE temp_enforcement_team SET chat_id = ? WHERE temp_chat_id = ? ', (chat_id,temp_chat_id))
            else:
                # Insert a new enforcement team member
                cursor.execute('''
                    INSERT INTO temp_enforcement_team (temp_chat_id, chat_id, name)
                    VALUES (?, ?, ?)
                ''', (temp_chat_id, chat_id, name))

        conn.commit()  # Commit the changes after executing the query

async def delete_temp_enforcement_team_member(temp_chat_id):
    """
    Deletes a row from the temp_enforcement_team table based on the given temp_chat_id.

    :param temp_chat_id: The temporary chat ID of the enforcement team member to delete.
    """
    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.cursor()
        
        # Execute the delete command
        cursor.execute('DELETE FROM temp_enforcement_team WHERE temp_chat_id = ?', (temp_chat_id,))
        conn.commit()  # Commit the changes after executing the query

async def check_temp_enforcement_team_field_presence(temp_chat_id):
    """
    Check the presence of each field for the given temp_chat_id in the enforcement_team table
    and return a dictionary indicating the presence of each field.

    :param temp_chat_id: The unique identifier for the enforcement team member.
    :return: A dictionary indicating the presence of each field (chat_id, name, admin_chat_id).
    """
    
    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM temp_enforcement_team WHERE temp_chat_id = ?', (temp_chat_id,))
        result = cursor.fetchone()
        
        if result:
            # Unpack the result tuple
            db_temp_chat_id, db_chat_id, db_name= result
            
            # Create the dictionary based on the fields' presence
            return {
                'name': db_name is not None,
                'temp_chat_id': db_temp_chat_id is not None, 
                'chat_id': bool(db_chat_id)
            }
        else:
            # Handle the case where the chat_id is not found
            return {
                'name': False,
                'temp_chat_id': False,
                'chat_id' : False
            }
        
async def retrieve_temp_enforcement_team_member(temp_chat_id):
    """
    Retrieves a row from the temp_enforcement_team table based on the given temp_chat_id.

    :param temp_chat_id: The temporary chat ID of the enforcement team member to retrieve.
    :return: A dictionary containing the enforcement team member details, or None if no member is found.
    """
    with sqlite3.connect(COUNCIL_MANAGEMENT_DATABASE) as conn:
        cursor = conn.cursor()
        
        # Execute the SELECT query to retrieve the row
        cursor.execute('SELECT * FROM temp_enforcement_team WHERE temp_chat_id = ?', (temp_chat_id,))
        result = cursor.fetchone()

        # If a result is found, return it.
        if result:
            return result
        else:
            # Return None if no row is found
            return None
