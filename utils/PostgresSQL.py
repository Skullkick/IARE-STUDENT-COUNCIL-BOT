# PostGrace database for Student Council 
import asyncpg
import asyncio
import os 
import json 

#Database Credentials 
USER= os.environ.get("POSTGRES_USER_ID") 
PASSWORD= os.environ.get("POSTGRES_PASSWORD") 
DATABASE = os.environ.get("POSTGRES_DATABASE") 
HOST= os.environ.get("POSTGRES_HOST") 
PORT = os.environ.get("POSTGRES_PORT") 
async def connect_pg_database(): 
    """connect_pg_database is used to make a connection to the postgres database""" 
    # connecting to the PSQL database 
    connection = await asyncpg.connect( 
        user=USER, 
        password=PASSWORD, 
        database=DATABASE, 
        host=HOST, 
        port=PORT 
    ) 
    return connection 
 
 
 
# Clubs 


async def create_all_pgdatabase_tables(): 
    try:
        await create_student_council_table() # done testing
        await create_clubs_table() # done testing
        await create_event_table() # done testing
        await create_table_event_data() # done testing
        await create_core_team_table() # done testing
        await create_enforcement_team_table() # done testin
        await create_permissions_table() # pending testing
        
                
     
    except Exception as e: 
        print(f"An error while creating PG_database:{e}") 
     




async def create_clubs_table(): 
    """ 
    Create the necessary table for storing club information in the PostgreSQL database. 
    SERIAL auto-increments in PostgreSQL.
    """ 
    connection = await connect_pg_database()   
    if not connection:
        print("Failed to establish a database connection.")
        return False

    try: 
        # Create the clubs table if it doesn't exist 
        await connection.execute(""" 
            CREATE TABLE IF NOT EXISTS clubs ( 
                id SERIAL PRIMARY KEY,   
                name TEXT NOT NULL, 
                description TEXT, 
                president TEXT, 
                pres_chat_id INTEGER, 
                vice_president TEXT, 
                vice_pres_chat_id INTEGER 
            )
        """) 
        print("Clubs table created successfully.")
        return True
     
    except Exception as e: 
        print(f"Error while creating clubs table: {e}")
        return False
     
    finally: 
        await connection.close() 
 


         
         
async def store_club_info(club_id=None, name=None, description=None, president=None, pres_chat_id=None, vice_president=None, vice_pres_chat_id=None):
    connection = await connect_pg_database()
    if not connection:
        print("Failed to establish a database connection.")
        return False

    try:
        if club_id:
            # Attempt to update, and insert if no row is affected (meaning club_id doesn't exist)
            result = await connection.execute(
                '''UPDATE clubs SET 
                       name = COALESCE($2, name),
                       description = COALESCE($3, description),
                       president = COALESCE($4, president),
                       pres_chat_id = COALESCE($5, pres_chat_id),
                       vice_president = COALESCE($6, vice_president),
                       vice_pres_chat_id = COALESCE($7, vice_pres_chat_id)
                   WHERE id = $1''', 
                club_id, name, description, president, pres_chat_id, vice_president, vice_pres_chat_id
            )

            # If no rows were updated, insert a new row with the specified club_id
            if result == 'UPDATE 0':
                await connection.execute(
                    '''INSERT INTO clubs (id, name, description, president, pres_chat_id, vice_president, vice_pres_chat_id)
                       VALUES ($1, $2, $3, $4, $5, $6, $7)''',
                    club_id, name, description, president, pres_chat_id, vice_president, vice_pres_chat_id
                )
                print("New club inserted with specified club_id.")
            else:
                print("Club info updated successfully.")
        else:
            # Insert with an auto-generated ID
            await connection.execute(
                '''INSERT INTO clubs (name, description, president, pres_chat_id, vice_president, vice_pres_chat_id)
                   VALUES ($1, $2, $3, $4, $5, $6)''',
                name, description, president, pres_chat_id, vice_president, vice_pres_chat_id
            )
            print("New club inserted with auto-generated ID.")
        return True

    except Exception as e:
        print(f"Error while storing club info: {e}")
        return False
    finally:
        await connection.close()
         

 
async def retrive_club_info():
    """ 
    Asynchronously fetch all club names and their indexes from the SQLite database. 
    Returns a list of tuples with (id, name). 
    """ 
    connection = await connect_pg_database()
    try: 
        Clubs = await connection.fetch("SELECT * FROM clubs") 
        return Clubs 
     
    except Exception as e: 
        print(f"error while fetching the data:{e}")
        return []
    finally: 
        await connection.close() 
 
 
 
async def delete_club_by_id(club_id: int): 
 
    connection = await connect_pg_database() 
    try: 
 
        result = await connection.execute("DELETE FROM clubs WHERE id = $1", club_id) 
 
        if result == "DELETE 0": 
            print(f"No club found with id {club_id}.") 
        else: 
            print(f"Club with id {club_id} deleted successfully.") 
     
    except Exception as e: 
        print(f"An error occurred: {e}") 
     
    finally: 
        await connection.close() 
         
 
 
async def retrieve_all_clubs_data(club_name: str): 
     
    connection = await connect_pg_database() 
    try: 
  
        result = await connection.fetchrow("SELECT * FROM clubs") 
        return result if result else None 
         
    except Exception as e: 
        print(f"An error occurred: {e}") 
        return None 
     
    finally: 
        await connection.close() 
 
 
async def create_event_table(): 
    connection = await connect_pg_database() 
    try: 
        await connection.execute(''' 
        CREATE TABLE IF NOT EXISTS events ( 
            id SERIAL PRIMARY KEY, 
            name TEXT, 
            number_of_days INTEGER, 
            date_time TEXT, 
            venue TEXT, 
            audience_size INTEGER, 
            type TEXT CHECK(type IN ('Tech', 'Non-Tech')) 
        ) 
        ''') 
        print("Events table created successfully.") 
         
    except Exception as e: 
        print(f"Error while creating events table: {e}") 
     
    finally: 
        await connection.close() 
 
 
 
async def store_event_info(id=None, name=None, number_of_days=None, date_time=None, venue=None, audience_size=None, type=None): # check in sql lite code
 
    connection = await connect_pg_database() 
    try: 
        if id is not None: 
           
            query = ''' 
            UPDATE events  
            SET name = COALESCE($1, name), 
                number_of_days = COALESCE($2, number_of_days), 
                date_time = COALESCE($3, date_time), 
                venue = COALESCE($4, venue), 
                audience_size = COALESCE($5, audience_size), 
                type = COALESCE($6, type) 
            WHERE id = $7 
            RETURNING id; 
            ''' 
            result = await connection.execute(query, name, number_of_days, date_time, venue, audience_size, type, id) 
            if result == "UPDATE 0": 
                print(f"Event with ID {id} does not exist.") 
            else: 
                print(f"Event with ID {id} updated successfully.") 
        else: 
            # Insert a new event 
            query = ''' 
            INSERT INTO events (name, number_of_days, date_time, venue, audience_size, type) 
            VALUES ($1, $2, $3, $4, $5, $6) 
            RETURNING id; 
            ''' 
            event_id = await connection.fetchval(query, name, number_of_days, date_time, venue, audience_size, type) 
            print(f"Successfully inserted event with ID {event_id}.") 
             
    except Exception as e: 
        print(f"Error while storing event values to the database: {e}") 
     
    finally: 
        await connection.close() 
 
 
async def retrive_events_info(): 
 
    connection = await connect_pg_database() 
    try: 
        query = "SELECT * FROM events" 
        events = await connection.fetch(query) 
        return events 
     
    except Exception as e: 
        print(f"Error while fetching event data: {e}") 
     
    finally: 
        await connection.close() 
 

async def delete_event_by_id(event_id: int): 
 
    connection = await connect_pg_database() 
    try: 
        query = "DELETE FROM events WHERE id = $1" 
        result = await connection.execute(query, event_id) 
         
        if result == "DELETE 0": 
            print(f"No event found with id {event_id}.") 
        else: 
            print(f"Event with id {event_id} deleted successfully.") 
     
    except Exception as e: 
        print(f"An error occurred while deleting event: {e}") 
     
    finally: 
        await connection.close() 
 
 
async def create_event_table():
    connection = await connect_pg_database()
    try:
        query = '''
            CREATE TABLE IF NOT EXISTS event_data (
                event_id SERIAL PRIMARY KEY,
                reporter_name TEXT,
                reporter_number TEXT,
                photos_link TEXT,
                event_report TEXT,
                proposal_form TEXT,
                flyer_and_schedule TEXT,
                list_of_participants TEXT
            )
        '''
        await connection.execute(query)
        print("Event_data table created successfully.")
        return True
    except Exception as e:
        print(f"An error occurred while creating the event_data table: {e}")
        return False
    finally:
        await connection.close()


async def store_or_update_event_data(event_id=None, reporter_name=None, reporter_number=None, photos_link=None,
                                     event_report=None, proposal_form=None, flyer_and_schedule=None, list_of_participants=None):
    connection = await connect_pg_database()
    try:
        # Check if the event with the given event_id already exists
        query = 'SELECT * FROM event_data WHERE event_id = $1'
        existing_data = await connection.fetchrow(query, event_id)

        if existing_data:
            # Update the existing event details
            if reporter_name is not None:
                await connection.execute('UPDATE event_data SET reporter_name = $1 WHERE event_id = $2', reporter_name, event_id)
            if reporter_number is not None:
                await connection.execute('UPDATE event_data SET reporter_number = $1 WHERE event_id = $2', reporter_number, event_id)
            if photos_link is not None:
                await connection.execute('UPDATE event_data SET photos_link = $1 WHERE event_id = $2', photos_link, event_id)
            if event_report is not None:
                await connection.execute('UPDATE event_data SET event_report = $1 WHERE event_id = $2', event_report, event_id)
            if proposal_form is not None:
                await connection.execute('UPDATE event_data SET proposal_form = $1 WHERE event_id = $2', proposal_form, event_id)
            if flyer_and_schedule is not None:
                await connection.execute('UPDATE event_data SET flyer_and_schedule = $1 WHERE event_id = $2', flyer_and_schedule, event_id)
            if list_of_participants is not None:
                await connection.execute('UPDATE event_data SET list_of_participants = $1 WHERE event_id = $2', list_of_participants, event_id)
        else:
            # Insert a new event record
            await connection.execute('''
                INSERT INTO event_data (reporter_name, reporter_number, photos_link,
                                        event_report, proposal_form, flyer_and_schedule, list_of_participants)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
            ''', reporter_name, reporter_number, photos_link, event_report, proposal_form, flyer_and_schedule, list_of_participants)
            print(f"New event data stored successfully.")
            return True
    except Exception as e:
        print(f"An error occurred while storing or updating event data: {e}")
        return False
    finally:
        await connection.close()


async def delete_event_data(event_id):
    if event_id is None:
        raise ValueError("event_id must be provided to delete an event record.")

    connection = await connect_pg_database()
    try:
        # Check if the event with the given ID exists
        query = 'SELECT * FROM event_data WHERE event_id = $1'
        existing_data = await connection.fetchrow(query, event_id)

        if existing_data:
            # Delete the event record
            await connection.execute('DELETE FROM event_data WHERE event_id = $1', event_id)
            print(f"Event with ID {event_id} has been deleted.")
            return True
        else:
            print(f"No event found with ID {event_id}.")
            return False
    except Exception as e:
        print(f"An error occurred while deleting event data: {e}")
        return False
    finally:
        await connection.close()


async def retrieve_event_data():
    # if event_id is None:
    #     raise ValueError("event_id must be provided to retrieve an event record.")

    connection = await connect_pg_database()
    try:
        # Fetch the event data based on event_id
        query = 'SELECT * FROM event_data'
        event_data = await connection.fetchrow(query)

        if event_data:
            print(f"Event data retrieved successfully: {event_data}")
            return event_data
        else:
            print(f"No event found.")
            return None
    except Exception as e:
        print(f"An error occurred while retrieving event data: {e}")
        return None
    finally:
        await connection.close()

 



async def create_permissions_table(): 
    connection = await connect_pg_database() 
    try: 
        query = ''' 
            CREATE TABLE IF NOT EXISTS permissions ( 
                chat_id BIGINT PRIMARY KEY, 
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
                list_of_participants TEXT 
            ) 
        ''' 
        await connection.execute(query) 
        print("Permissions table created.")
    except Exception as e: 
        print(f"An error occurred while creating the permissions table: {e}") 
    finally: 
        await connection.close() 



async def initialize_permissions(chat_id): 
    connection = await connect_pg_database() 
    try: 
        # Insert default values (False) for the given chat_id 
        await connection.execute(''' 
            INSERT INTO permissions ( 
                chat_id, events, clubs, edit_clubs, edit_events,  
                proposal_form, flyer, core_team, core_team_edit,  
                council_admin, enforcement_team, photos_drive_link,  
                reporter_details, report_upload, list_of_participants 
            )  
            VALUES ($1, FALSE, FALSE, NULL, NULL, NULL, NULL, FALSE, NULL,  
                    FALSE, FALSE, NULL, NULL, NULL, NULL) 
        ''', chat_id) 
    except Exception as e: 
        print(f"An error occurred while initializing permissions: {e}") 
    finally: 
        await connection.close() 

async def set_permissions(
    chat_id,
    events=False,
    clubs=False,
    edit_clubs=None,
    edit_events=None,
    proposal_form=None,
    flyer=None,
    core_team=False,
    core_team_edit=None,
    council_admin=False,
    enforcement_team=False,
    photos_drive_link=None,
    reporter_details=None,
    report_upload=None,
    list_of_participants=None,
    core_team_tasks=None
):
    connection = await connect_pg_database()
    
    try:
        # Fixing the parameter placeholder to $1, $2... format for PostgreSQL compatibility
        result = await connection.fetchrow('''                          
            SELECT chat_id FROM permissions WHERE chat_id = $1
        ''', chat_id)  # Check if the chat_id already exists

        if result is None:
            # Insert a new record if chat_id doesn't exist
            await connection.execute('''
                INSERT INTO permissions (
                    chat_id, events, clubs, edit_clubs, edit_events, 
                    proposal_form, flyer, core_team, core_team_edit, 
                    council_admin, enforcement_team, photos_drive_link, 
                    reporter_details, report_upload, list_of_participants
                ) 
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
            ''', (
                chat_id, events, clubs, edit_clubs, edit_events, 
                proposal_form, flyer, core_team, core_team_edit, 
                council_admin, enforcement_team, photos_drive_link, 
                reporter_details, report_upload, list_of_participants
            ))
        else:
            # Update the existing record if chat_id exists
            await connection.execute('''
                UPDATE permissions
                SET events = $1, clubs = $2, edit_clubs = $3, edit_events = $4, 
                    proposal_form = $5, flyer = $6, core_team = $7, core_team_edit = $8, 
                    council_admin = $9, enforcement_team = $10, photos_drive_link = $11, 
                    reporter_details = $12, report_upload = $13, list_of_participants = $14
                WHERE chat_id = $15
            ''', (
                events, clubs, edit_clubs, edit_events, 
                proposal_form, flyer, core_team, core_team_edit, 
                council_admin, enforcement_team, photos_drive_link, 
                reporter_details, report_upload, list_of_participants, chat_id
            ))

    except Exception as e:
        print(f"An error occurred while setting permissions: {e}")

    finally:
        await connection.close()

 
     
# Admin 
 
 
async def create_admins_table(): 
 
    connection = await connect_pg_database() 
    try: 
        await connection.execute(''' 
            CREATE TABLE IF NOT EXISTS admins ( 
                id SERIAL PRIMARY KEY, 
                name TEXT, 
                description TEXT, 
                dean TEXT, 
                dean_chat_id BIGINT, 
                president TEXT, 
                prdnt_chat_id BIGINT, 
                vice_president TEXT, 
                vice_prdnt_chat_id BIGINT, 
                meeting_schedule JSONB,        
                tasks JSONB, 
                calendar_privileges TEXT 
            ) 
        ''') 
    except Exception as e: 
        print(f"failed to create admin table {e} .")     
    finally: 
        await connection.close() 
 
 
import json

async def store_admin_info(admin_id, name, description=None, dean=None, dean_chat_id=None, 
                           president=None, prdnt_chat_id=None, vice_president=None, 
                           vice_prdnt_chat_id=None, meeting_schedule=None, tasks=None, 
                           calendar_privileges='read'):
    """
    Store admin information in the PostgreSQL database. If the admin already exists, update the information; 
    otherwise, insert a new record.
    """
    connection = await connect_pg_database()
    try:
        if admin_id is not None:
            # Update existing record
            result = await connection.fetchrow('SELECT * FROM admins WHERE id = $1', admin_id)
            if result:
                await connection.execute('''
                    UPDATE admins SET 
                        name = COALESCE($2, name),
                        description = COALESCE($3, description),
                        dean = COALESCE($4, dean),
                        dean_chat_id = COALESCE($5, dean_chat_id),
                        president = COALESCE($6, president),
                        prdnt_chat_id = COALESCE($7, prdnt_chat_id),
                        vice_president = COALESCE($8, vice_president),
                        vice_prdnt_chat_id = COALESCE($9, vice_prdnt_chat_id),
                        meeting_schedule = COALESCE($10, meeting_schedule),
                        tasks = COALESCE($11, tasks),
                        calendar_privileges = COALESCE($12, calendar_privileges)
                    WHERE id = $1
                ''', admin_id, name, description, dean, dean_chat_id, president, prdnt_chat_id, 
                    vice_president, vice_prdnt_chat_id, 
                    json.dumps(meeting_schedule) if meeting_schedule else None,
                    json.dumps(tasks) if tasks else None,
                    calendar_privileges)
            else:
                raise ValueError("Admin ID does not exist for update.")
        else:
            # Insert new record
            await connection.execute('''
                INSERT INTO admins (name, description, dean, dean_chat_id, president, prdnt_chat_id, 
                                    vice_president, vice_prdnt_chat_id, meeting_schedule, tasks, calendar_privileges)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            ''', name, description, dean, dean_chat_id, president, prdnt_chat_id, vice_president, 
                vice_prdnt_chat_id, json.dumps(meeting_schedule or []), json.dumps(tasks or []), 
                calendar_privileges)
             
    except Exception as e:
        print(f"Failed to store admin information in the PostgreSQL database: {e}.")
     
    finally:
        await connection.close()
 
 
 
async def create_core_team_table(): 
 
# Create the core_team table in PostgreSQL for storing core team members. 
 
    connection = await connect_pg_database() 
    try: 
        await connection.execute(''' 
            CREATE TABLE IF NOT EXISTS core_team ( 
                core_member_index SERIAL PRIMARY KEY, 
                core_name TEXT, 
                core_member_name TEXT, 
                core_member_chat_id BIGINT, 
                tasks JSONB 
            ) 
        ''') 
    except Exception as e: 
        print(f"Error while creating core team table in PG database{e}. ")   
     
    finally: 
        await connection.close() 
 
async def store_core_team_info(
    core_team_index=None,
    core_name=None,
    core_member_name=None,
    core_member_chat_id=None,
    tasks=None
):
    if core_team_index is None and (core_member_name is None or core_member_chat_id is None or core_name is None):
        raise ValueError("For new entries, core_name, core_member_name, and core_member_chat_id must all be provided.")
    
    connection = await connect_pg_database()
    try:
        if core_team_index is not None:
            # Update existing core team member
            result = await connection.fetchrow('SELECT * FROM core_team WHERE core_member_index = $1', core_team_index)
            if result:
                await connection.execute('''
                    UPDATE core_team SET 
                        core_name = COALESCE($2, core_name), 
                        core_member_name = COALESCE($3, core_member_name), 
                        core_member_chat_id = COALESCE($4, core_member_chat_id), 
                        tasks = COALESCE($5, tasks) 
                    WHERE core_member_index = $1
                ''', core_team_index, core_name, core_member_name, core_member_chat_id, json.dumps(tasks) if tasks else None)
            else:
                raise ValueError("Core team index does not exist for update.")
        else:
            # Insert new core team member
            await connection.execute('''
                INSERT INTO core_team (core_name, core_member_name, core_member_chat_id, tasks) 
                VALUES ($1, $2, $3, $4)
            ''', core_name, core_member_name, core_member_chat_id, json.dumps(tasks or []))

    except Exception as e:
        print(f"Error while storing core team details in PG database table {e}.")
    finally:
        await connection.close()

 
 
 
 
async def delete_core_team_member_by_chat_id(core_member_chat_id): 
 
#    Delete a core team member from the PostgreSQL database based on their chat ID. 
 
    connection = await connect_pg_database() 
    try: 
        result = await connection.fetchrow('SELECT * FROM core_team WHERE core_member_chat_id = $1', core_member_chat_id) 
        if result: 
            await connection.execute('DELETE FROM core_team WHERE core_member_chat_id = $1', core_member_chat_id) 
            print(f"Core team member with chat ID {core_member_chat_id} has been deleted.") 
        else: 
            raise ValueError(f"No core team member found with chat ID {core_member_chat_id}.") 
         
    except Exception as e: 
        print(f"Failed to delete the core team member {e}.")   
         
    finally: 
        await connection.close() 
 
async def retrive_core_team_members(): 
    """ 
    Retrieve all core team members from the PostgreSQL database. 
    """ 
    connection = await connect_pg_database() 
    try: 
        result = await connection.fetch('SELECT * FROM core_team') 
        return result 
     
    except Exception as e: 
        print(f"Failed to retrive all the team members information {e}.") 
             
    finally: 
        await connection.close() 
         
         
async def delete_core_member_by_index(core_member_index):
 
    connection = await connect_pg_database() 
    try: 
        result = await connection.fetchrow('SELECT core_name FROM core_team WHERE core_member_index = $1', core_member_index) 
        if result: 
            await connection.execute('DELETE FROM core_team WHERE core_member_index = $1', core_member_index) 
            return True 
        else: 
            raise ValueError("Core member index does not exist.") 
         
    except Exception as e: 
        print(f"Failed to Delete a core member from the PostgreSQL database using the core_member_index{e}.") 
         
    finally: 
        await connection.close() 
 
 

 
 
 
# Student Council Team Code 
 
 
async def create_student_council_table():
    connection = await connect_pg_database()
    try:
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS student_council (
                chat_id SERIAL PRIMARY KEY,
                Name TEXT,
                dean BOOLEAN NOT NULL DEFAULT FALSE,
                president BOOLEAN NOT NULL DEFAULT FALSE,
                vice_president BOOLEAN NOT NULL DEFAULT FALSE
            )
        ''')
        print("Student council table created successfully.")
        return True
    except Exception as e:
        print(f"Failed to create student council table: {e}.")
        return False
    finally:
        await connection.close()


async def store_student_council_info(chat_id, name=None, dean=None, president=None, vice_president=None):
    connection = await connect_pg_database()

    try:
        result = await connection.fetchrow('SELECT * FROM student_council WHERE chat_id = $1', chat_id)

        if result:
            # Update existing member
            if name is not None:
                await connection.execute('UPDATE student_council SET Name = $1 WHERE chat_id = $2', name, chat_id)
            if dean is not None:
                await connection.execute('UPDATE student_council SET dean = $1 WHERE chat_id = $2', dean, chat_id)
            if president is not None:
                await connection.execute('UPDATE student_council SET president = $1 WHERE chat_id = $2', president, chat_id)
            if vice_president is not None:
                await connection.execute('UPDATE student_council SET vice_president = $1 WHERE chat_id = $2', vice_president, chat_id)
        else:
            # Insert new member
            await connection.execute('''
                INSERT INTO student_council (chat_id, Name, dean, president, vice_president)
                VALUES ($1, $2, $3, $4, $5)
            ''', chat_id, name, dean, president, vice_president)
        print("Student council member stored/updated successfully.")
        return True
    except Exception as e:
        print(f"Failed to store/update student council member: {e}.")
        return False
    finally:
        await connection.close()


async def delete_student_council_member(chat_id):
    connection = await connect_pg_database()
    try:
        result = await connection.fetchrow('SELECT chat_id FROM student_council WHERE chat_id = $1', chat_id)
        if result:
            await connection.execute('DELETE FROM student_council WHERE chat_id = $1', chat_id)
            print("Student council member deleted successfully.")
            return True
        else:
            print("Chat ID does not exist.")
            return False
    except Exception as e:
        print(f"Failed to delete student council member: {e}.")
        return False
    finally:
        await connection.close()


async def retirve_all_student_council_info():
    connection = await connect_pg_database()
    try:
        result = await connection.fetch('SELECT * FROM student_council')
        return result
    except Exception as e:
        print(f"Error while retrieving all student council information: {e}.")
        return None
    finally:
        await connection.close()





async def create_enforcement_team_table():
 
    connection = await connect_pg_database() 
    try: 
        await connection.execute(''' 
            CREATE TABLE IF NOT EXISTS enforcement_team ( 
                chat_id SERIAL PRIMARY KEY, 
                name TEXT 
            ) 
        ''') 
         
    except Exception as e: 
        print(f"Failed to create enforcement team table: {e}") 
         
    finally: 
        await connection.close()
        

async def retrive_enforcement_team_team_info(): 
 
    connection = await connect_pg_database() 
    try: 
        result = await connection.fetchrow('SELECT * FROM enforcement_team') 
        return result
     
    except Exception as e: 
        print(f"Error while Retrieving all chat_ids from the enforcement_team table:{e}.") 
 
     
    finally: 
        await connection.close() 
    
    

async def store_enforcement_team_details(chat_id=None, name=None): 
 
 
    connection = await connect_pg_database() 
    try: 
        if chat_id is not None: 
            result = await connection.fetchrow('SELECT * FROM enforcement_team WHERE chat_id = $1', chat_id) 
             
            if result: 
                if name is not None: 
                    await connection.execute('UPDATE enforcement_team SET name = $1 WHERE chat_id = $2', name, chat_id) 
            else: 
                await connection.execute('INSERT INTO enforcement_team (chat_id, name) VALUES ($1, $2)', chat_id, name) 
     
    except Exception as e: 
        print(f"Failed to Store/Update enforcement team member information in the PostgreSQL database.{e}") 
             
                 
    finally: 
        await connection.close() 
 
 
 
async def delete_enforcement_team_member(chat_id): 
    """ 
    Deletes a member from the enforcement_team table using the chat_id. 
    """ 
    connection = await connect_pg_database() 
    try: 
        result = await connection.fetchrow('SELECT chat_id FROM enforcement_team WHERE chat_id = $1', chat_id) 
        if result: 
            await connection.execute('DELETE FROM enforcement_team WHERE chat_id = $1', chat_id) 
            return True 
        else: 
            raise ValueError("Chat ID does not exist.") 
         
    except Exception as e: 
        print(f"Failed to Delete a member from the enforcement_team table using the chat_id.{e}") 
               
         
    finally: 
        await connection.close()




async def create_violations_table(): 
  # write retrvie for this code
  
 
    connection = await connect_pg_database() 
    try: 
        await connection.execute(''' 
            CREATE TABLE IF NOT EXISTS violations ( 
                violation_id SERIAL PRIMARY KEY, 
                violation TEXT NOT NULL, 
                club_name TEXT NOT NULL, 
                status TEXT NOT NULL, 
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                time_remaining INTEGER 
            ) 
        ''') 
         
    except Exception as e: 
        print(f"Failed to create violations table: {e}") 
       
    finally: 
        await connection.close() 

 
 
async def store_violation_details(violation_id=None, violation=None, club_name=None, status=None, time_remaining=None): 
 
    connection = await connect_pg_database() 
    try: 
        if violation_id is not None: 
            result = await connection.fetchall('SELECT * FROM violations WHERE violation_id = $1', violation_id) 
             
            if result: 
                if violation is not None: 
                    await connection.execute('UPDATE violations SET violation = $1 WHERE violation_id = $2', violation, violation_id) 
                if club_name is not None: 
                    await connection.execute('UPDATE violations SET club_name = $1 WHERE violation_id = $2', club_name, violation_id) 
                if status is not None: 
                    await connection.execute('UPDATE violations SET status = $1 WHERE violation_id = $2', status, violation_id) 
                if time_remaining is not None: 
                    await connection.execute('UPDATE violations SET time_remaining = $1 WHERE violation_id = $2', time_remaining, violation_id) 
            else: 
                raise ValueError("Violation ID does not exist.") 
        else: 
            await connection.execute(''' 
                INSERT INTO violations (violation, club_name, status, time_remaining) 
                VALUES ($1, $2, $3, $4) 
            ''', violation, club_name, status, time_remaining) 
             
    except Exception as e: 
        print(f"Failed to Store/Update violation details in the PostgreSQL database.{e}") 
                       
    finally: 
        await connection.close() 
 
 
 
async def delete_violation(violation_id): 
    """ 
    Deletes a violation record from the PostgreSQL database using the violation_id. 
    """ 
    connection = await connect_pg_database() 
    try: 
        result = await connection.fetchrow('SELECT violation_id FROM violations WHERE violation_id = $1', violation_id) 
        if result: 
            await connection.execute('DELETE FROM violations WHERE violation_id = $1', violation_id) 
            return True 
        else: 
            raise ValueError("Violation ID does not exist.") 
         
    except Exception as e: 
        print(f"Error while Deleting a violation record from the PostgreSQL database using the violation_id.{e}")         
         
    finally: 
        await connection.close()
        
        

async def retirve_violations_table_info(): 
 
    connection = await connect_pg_database() 
    try: 
        result = await connection.fetchall('SELECT * FROM violations') 
        return result
     
    except Exception as e: 
        print(f"Error while Retrieving all ID'S from the violations table:{e}.") 
 
     
    finally: 
        await connection.close() 
    



async def store_core_team_table_info(core_member_index=None, core_name=None, core_member_name=None, core_member_chat_id=None, tasks=None):
    """Store or update information in the core_team table based on core_member_index."""
    connection = await connect_pg_database()
    try:
        if core_member_index is not None:
            # Check if the core_member_index exists
            result = await connection.fetchrow('SELECT * FROM core_team WHERE core_member_index = $1', core_member_index)

            if result:
                # Update fields based on provided arguments
                if core_name is not None:
                    await connection.execute('UPDATE core_team SET core_name = $1 WHERE core_member_index = $2', core_name, core_member_index)
                if core_member_name is not None:
                    await connection.execute('UPDATE core_team SET core_member_name = $1 WHERE core_member_index = $2', core_member_name, core_member_index)
                if core_member_chat_id is not None:
                    await connection.execute('UPDATE core_team SET core_member_chat_id = $1 WHERE core_member_index = $2', core_member_chat_id, core_member_index)
                if tasks is not None:
                    await connection.execute('UPDATE core_team SET tasks = $1 WHERE core_member_index = $2', tasks, core_member_index)
            else:
                raise ValueError("core_member_index does not exist.")
        else:
            # Insert new record if core_member_index is None
            await connection.execute('''
                INSERT INTO core_team (core_name, core_member_name, core_member_chat_id, tasks)
                VALUES ($1, $2, $3, $4)
            ''', core_name, core_member_name, core_member_chat_id, tasks)

    except Exception as e:
        print(f"Failed to Store/Update core_team details in the PostgreSQL database: {e}")
    finally:
        await connection.close()


async def retirve_core_team_table_info():
    """Retrieve all records from the core_team table."""
    connection = await connect_pg_database()
    try:
        result = await connection.fetch('SELECT * FROM core_team')
        return result

    except Exception as e:
        print(f"Error while retrieving all records from the core_team table: {e}")
    finally:
        await connection.close()


async def delete_core_team(core_member_index):
    """Delete a record from the core_team table using the core_member_index."""
    connection = await connect_pg_database()
    try:
        result = await connection.fetchrow('SELECT core_member_index FROM core_team WHERE core_member_index = $1', core_member_index)
        if result:
            await connection.execute('DELETE FROM core_team WHERE core_member_index = $1', core_member_index)
            return True
        else:
            raise ValueError("core_member_index ID does not exist.")

    except Exception as e:
        print(f"Error while deleting a core_team record: {e}")
    finally:
        await connection.close()
        



async def create_table_event_data():
# write store, delete functions

    connection = await connect_pg_database()
    
    try:
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS event_data (
                event_id INTEGER PRIMARY KEY,
                reporter_name TEXT,
                reporter_number TEXT,
                photos_link TEXT,
                event_report TEXT,
                proposal_form TEXT,
                flyer_and_schedule TEXT,  
                list_of_participants TEXT 
            )
        ''')
        print("event_data table created successfully.")
        return True
    
    except Exception as e:
        print(f"error while creating table_event_data")
        return False
        
    finally:
        await connection.close()
        
        
async def store_table_event_data(event_id, reporter_name, reporter_number, photos_link, event_report, proposal_form, flyer_and_schedule, list_of_participants):
    
    connection = await connect_pg_database() 
    try: 
        await connection.execute(''' 
            INSERT INTO event_data (event_id, reporter_name, reporter_number, photos_link, event_report, proposal_form, flyer_and_schedule, list_of_participants) 
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8) 
        ''', event_id, reporter_name, reporter_number, photos_link, event_report, proposal_form, flyer_and_schedule, list_of_participants) 
        print("Data inserted successfully.")
        return True
    except Exception as e: 
        print(f"Failed to Store/Update event_data details in the PostgreSQL database.{e}") 
        return False              
    finally: 
        await connection.close()
        
async def delete_table_event_data(event_id): 
    """ 
    Deletes a violation record from the PostgreSQL database using the event_id. 
    """ 
    connection = await connect_pg_database() 
    try: 
        result = await connection.fetchrow('SELECT event_id FROM event_data WHERE event_id = $1', event_id) 
        if result: 
            await connection.execute('DELETE FROM event_data WHERE event_id = $1', event_id) 
            return True 
        else: 
            raise ValueError("event_id ID does not exist.") 
         
    except Exception as e: 
        print(f"Error while Deleting a event_data record from the PostgreSQL database using the event_id.{e}")         
        return False
    finally: 
        await connection.close()


async def retrive_table_event_data():
 
    connection = await connect_pg_database() 
    try: 
        result = await connection.fetchrow('SELECT * FROM event_data') 
        print(f"successfully retrieved data using {retrive_table_event_data}")
        return result
     
    except Exception as e: 
        print(f"Error while Retrieving data from the event_data table:{e}.") 
        return None
     
    finally: 
        await connection.close() 
        
        
