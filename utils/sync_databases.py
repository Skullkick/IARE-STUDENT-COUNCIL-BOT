from utils import sqlitedb,PostgresSQL

async def sync_databases():
    await perform_sync_student_council()
    await perform_sync_clubs_table()
    await perform_sync_event_table()
    
    # await create_event_table()
    
    await perform_sync_core_team_table_info()
    await perform_sync_enforcement_team_info()
    # await create_permissions_table()



async def perform_sync_student_council():
    student_council_data = await PostgresSQL.retirve_all_student_council_info()
    """         chat_id SERIAL PRIMARY KEY, 
                Name TEXT, 
                dean BOOLEAN NOT NULL DEFAULT FALSE, 
                president BOOLEAN NOT NULL DEFAULT FALSE, 
                vice_president BOOLEAN NOT NULL DEFAULT FALSE """
    if student_council_data:
        for row in student_council_data:
            print(row)
            chat_id,name,dean,president,vice_president = row
            await sqlitedb.store_student_council_info(chat_id, name, dean, president, vice_president)
        print("student_council Successfully synced database with sqlite")
    else:
        print("No data in Student council table to synce with the database")
      


async def perform_sync_clubs_table():
    clubs_table_data = await PostgresSQL.retrive_club_info()
    
    # this below code is for only reference purpose.
    """
                id SERIAL PRIMARY KEY,   
                name TEXT NOT NULL,
                description TEXT, 
                president TEXT, 
                pres_chat_id INTEGER, 
                vice_president TEXT, 
                vice_pres_chat_id INTEGER
    
    """
    
    if clubs_table_data:
        for row in clubs_table_data:
            print(row)
            club_id,name,description,president,pres_chat_id,vice_president,vice_pres_chat_id = row
            await sqlitedb.store_club_info(club_id, name, description, president, pres_chat_id, vice_president, vice_pres_chat_id)
        print("clubs_table Successfully synced database with sqlite")
    else:
        print("No data in clubs table to synce with the database")
        
        
async def perform_sync_event_table():
    event_table_data = await PostgresSQL.retrieve_event_data()
    """
            id SERIAL PRIMARY KEY, 
            name TEXT, 
            number_of_days INTEGER, 
            date_time TEXT, 
            venue TEXT, 
            audience_size INTEGER, 
            type TEXT CHECK(type IN ('Tech', 'Non-Tech'))
    """
    if event_table_data:
        for row in event_table_data:
            print(row)
            event_id,name,number_of_days,date_time,venue,audience_size,type = row
            await sqlitedb.store_event_info(event_id,name,number_of_days,date_time,venue,audience_size,type)
        print("event_table Sucessfully synced database with sqlite")
    else:
        print("No data in events to sync with sqlite")
       
       

        
      
async def perform_sync_core_team_table_info():
    core_team = await PostgresSQL.retirve_core_team_table_info()
    
    """         core_member_index SERIAL PRIMARY KEY, 
                core_name TEXT, 
                core_member_name TEXT, 
                core_member_chat_id BIGINT, 
                tasks JSONB 
                """
    if core_team:
        for row in core_team:
            print(row)
            core_member_index , core_name , core_member_name, core_member_chat_id , tasks = row
            await sqlitedb.store_core_team_info(core_member_index , core_name , core_member_name, core_member_chat_id , tasks)
            
        print("core_team_table_info Sucessfully synced database with sqlite")
        
    else:
        print("No data in core_team to sync with sqlite")
        
        
        
async def perform_sync_enforcement_team_info():

    enforcement_team = await PostgresSQL.retrive_enforcement_team_team_info()

    if enforcement_team:
        for row in enforcement_team:
            print(row)
            chat_id, name = row
            await sqlitedb.store_enforcement_team_details(chat_id, name)
        print("enforcement_team_info Sucessfully synced database with sqlite")    
    else:
        print("No data in enforcement_team to sync with sqlite")


        
async def perform_sync_permissions_table():
    permissions_table_data = await PostgresSQL.retrieve_permissions_info()
    
    if permissions_table_data:
        for row in permissions_table_data:
            print(row)
            permission_id, user_id, permission_level, description = row
            await sqlitedb.store_permissions_info(permission_id, user_id, permission_level, description)
        print("permissions_table Successfully synced permissions table with sqlite")
    else:
        print("No data in permissions table to sync with sqlite")



import asyncio

async def create_permissions_table():
    connection = await sqlitedb.connect_sqlite_database()
    await connection.execute('''
        CREATE TABLE IF NOT EXISTS permissions (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            permission_level TEXT,
            description TEXT
        )
    ''')
    await connection.commit()
    await connection.close()


async def create_student_council_table():
    connection = await sqlitedb.connect_sqlite_database()
    await connection.execute('''
        CREATE TABLE IF NOT EXISTS student_council (
            chat_id INTEGER PRIMARY KEY,
            name TEXT,
            dean BOOLEAN NOT NULL DEFAULT FALSE,
            president BOOLEAN NOT NULL DEFAULT FALSE,
            vice_president BOOLEAN NOT NULL DEFAULT FALSE
        )
    ''')
    await connection.commit()
    await connection.close()

