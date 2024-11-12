from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from templates import council_templates
from keyboards import student_council_keyboard
from services import student_council_service
from handlers import club_event_handler
from utils import sqlitedb,time,PostgresSQL
import json,os
# from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup

ADMIN_AUTHORIZATION_CODE = os.environ.get("ADMIN_AUTHORIZATION_PASS")


async def add_admin_by_authorization(bot,message):
    """
    This Function is used to add Admin access to the user by authorizing the message sent.
    :param bot: Pyrogram client
    :param message: Message sent by the user"""
    chat_id = message.chat.id
    authorization_code = message.text.split()[1:][0]
    if authorization_code == ADMIN_AUTHORIZATION_CODE:
        # await managers_handler.store_as_admin(admin_name,chat_id)
        # await pgdatabase.store_as_admin(admin_name,chat_id)
        await sqlitedb.store_student_council_info(chat_id=chat_id)
        # await PostgresSQL.store_student_council_info(chat_id=chat_id)
        await bot.send_message(chat_id,"Authorized Successfully for Admin access, use \"/admin\" to start admin panel.")
        #  Save to postgres database to make sure it saves permanently.
        await PostgresSQL.store_student_council_info(chat_id=chat_id)
        await message.delete()

async def initialize_storing_core_values(chat_id):
    # try:
    # print(await sqlitedb.retrieve_temp_core_info_by_chat_id(chat_id))
    # Retrieve temporary core team information from the database
    temp_chat_id, core_name, core_member_name, core_member_chat_id = await sqlitedb.retrieve_temp_core_info_by_chat_id(chat_id)
    
    # Store the core team information into the main core team table
    await sqlitedb.store_core_team_info(
        core_name=core_name,
        core_member_name=core_member_name,
        core_member_chat_id=core_member_chat_id,
        tasks=json.dumps({})
    )
    await PostgresSQL.store_core_team_info(
        core_name=core_name,
        core_member_name=core_member_name,
        core_member_chat_id=core_member_chat_id,
        tasks=json.dumps({})
    )
    # After storing the core team information, delete it from the temporary table
    await sqlitedb.delete_temp_core_team_member_by_user_chat_id(chat_id)
    # print(await sqlitedb.get_all_core_team_members())
    # except Exception as e:
    #     print(f"Error storing the core team values to the database: {e}")

async def initialize_storing_temp_enforcement_team_values(temp_chat_id):
    # try:
    # Retrieve temporary enforcement team information from the database
    temp_chat_id, enft_chat_id,enft_mem_name = await sqlitedb.retrieve_temp_enforcement_team_member(temp_chat_id)
    # Store the core team information into the main core team table
    if await sqlitedb.store_enforcement_team_details(
        chat_id=enft_chat_id,  # Enforcement team member chat_id.
        name=enft_mem_name # Enforcement team member name.
    ):
    
    # After storing the core team information, delete it from the temporary table
        await sqlitedb.delete_temp_enforcement_team_member(temp_chat_id)
        await PostgresSQL.store_enforcement_team_details(
        chat_id=enft_chat_id,  # Enforcement team member chat_id.
        name=enft_mem_name # Enforcement team member name.
        )

    # except Exception as e:
    #     print(f"Error storing the ENFT team values to the database: {e}")

async def store_edited_core_values(chat_id):
    try:
        # Retrieve temporary core team information from the database
        temp_chat_id, core_name, core_member_name, core_member_chat_id = await sqlitedb.retrieve_temp_core_info_by_chat_id(chat_id)
        
        # Store the core team information into the main core team table
        await sqlitedb.store_core_team_info(
            core_name=core_name,
            core_member_name=core_member_name,
            core_member_chat_id=core_member_chat_id
        )
        await PostgresSQL.store_core_team_info(
            core_name=core_name,
            core_member_name=core_member_name,
            core_member_chat_id=core_member_chat_id
        )
        
        # After storing the core team information, delete it from the temporary table
        await sqlitedb.delete_temp_core_team_member_by_user_chat_id(chat_id)

    except Exception as e:
        print(f"Error storing the values to the database: {e}")


async def receive_core_info(bot, message):
    chat_id = message.chat.id
    fields_status = await sqlitedb.check_temp_core_team_field_presence(chat_id)
    
    # Check if message contains text
    if message.text:
        text = message.text
        
        # Update the 'core_name' field if it's False
        if not fields_status['core_name']:
            await sqlitedb.store_temp_core_team_info(chat_id, core_name=text)
            await student_council_service.add_core_team_details(bot, chat_id)
        
        # Update the 'core_member_name' field if 'core_name' is True and 'core_member_name' is False
        elif not fields_status['core_member_name']:
            await sqlitedb.store_temp_core_team_info(chat_id, core_member_name=text)
            await student_council_service.add_core_team_details(bot, chat_id)
        
        # Update the 'core_member_chat_id' field if 'core_member_name' is True and 'core_member_chat_id' is False
        elif not fields_status['core_member_chat_id']:
            if await club_event_handler.is_valid_integer(text) is False:
                await bot.send_message(chat_id,"Chat ID is a numeric value. Please enter the value again.")
                return
            await sqlitedb.store_temp_core_team_info(chat_id=chat_id, core_member_chat_id=int(text),tasks=json.dumps({}))
            await student_council_service.add_core_team_details(bot, chat_id)
        
        # notifying that all fields are complete
        else:
            await message.reply_text("All core fields have been set.")


async def receive_edit_core_info(bot, message):
    chat_id = message.chat.id
    edit_action = await sqlitedb.check_permission(chat_id, edit_core=True)

    if edit_action == "core_name":
        text = message.text
        if text:
            await sqlitedb.store_temp_core_team_info(chat_id, core_name=text)
            await sqlitedb.set_permissions(chat_id)
            await store_edited_core_values(chat_id)
            await message.reply_text(f"Core name has been set to: {text}")

    elif edit_action == "core_member_name":
        text = message.text
        if text:
            await sqlitedb.store_temp_core_team_info(chat_id, core_member_name=text)
            await sqlitedb.set_permissions(chat_id)
            await store_edited_core_values(chat_id)
            await message.reply_text(f"Core member name has been set to: {text}")

    elif edit_action == "core_member_chat_id":
        text = message.text
        if text:
            if await club_event_handler.is_valid_integer(text) is False:
                await bot.send_message(chat_id,"Chat ID is a numeric value. Please enter the value again.")
                return
            await sqlitedb.store_temp_core_team_info(chat_id, core_member_chat_id=int(text))
            await sqlitedb.set_permissions(chat_id)
            await store_edited_core_values(chat_id)
            await message.reply_text(f"Core member chat_id has been set to: {text}")

    else:
        await message.reply_text("No valid edit action detected.")


async def recieve_council_admin_info(bot,message):
    chat_id = message.chat.id
    fields_status = await sqlitedb.check_student_council_field_presence(chat_id)
    # Check if message contains text
    if message.text:
        text = message.text
        if not fields_status['name']:
            await sqlitedb.store_student_council_info(chat_id,name=text)
            await student_council_service.add_student_council_details(bot, chat_id)
            await sqlitedb.set_permissions(chat_id)
        else:
            await bot.send_message("All the details of student council admin have been saved")
    
async def recieve_enforcement_team_info(bot,message):
    temp_chat_id = message.chat.id
    field_status = await sqlitedb.check_temp_enforcement_team_field_presence(temp_chat_id=temp_chat_id)
    if message.text:
        text = message.text
        if not field_status['chat_id']:
            if await club_event_handler.is_valid_integer(text) is False:
                await bot.send_message(temp_chat_id,"Chat_id of a Member should be a numeric value.")
                return
            await sqlitedb.store_temp_enforcement_team_details(temp_chat_id=temp_chat_id,chat_id=text)
            await student_council_service.add_enforcement_team_details(bot,temp_chat_id)
        elif not field_status['name']:
            await sqlitedb.store_temp_enforcement_team_details(temp_chat_id=temp_chat_id,name=text)
            await student_council_service.add_enforcement_team_details(bot,temp_chat_id)
            await initialize_storing_temp_enforcement_team_values(temp_chat_id=temp_chat_id)
            await sqlitedb.set_permissions(chat_id=temp_chat_id)

async def recieve_tasks_core_team(bot,message):
    chat_id = message.chat.id
    core_member_id = await sqlitedb.check_permission(chat_id=chat_id,core_team_tasks=True)
    if message.text:
        core_member_details = await sqlitedb.get_core_member_details(core_member_id=core_member_id,tasks=True)
        # print(core_member_details)
        # print(core_member_details['tasks'])
        if core_member_details['tasks'] is None:
            tasks = {}
        else:
            tasks = json.loads(core_member_details['tasks'])
        # stored_tasks = json.loads(await sqlitedb.get_core_info_by_id(core_member_id=core_member_id)[3])
        if len(tasks) == 0:
            tasks[1] = {'task':message.text,'status':False}
        else:
            tasks[len(tasks)+1] = {'task':message.text,'status':False}
        await sqlitedb.store_core_team_info(core_team_index=core_member_id,tasks=json.dumps(tasks))
        # button = []
        await bot.send_message(chat_id,"The task has been successfully assigned.",reply_markup = await student_council_keyboard.generate_back_button_to_core(core_member_id=core_member_id))
        # await bot.send_message(chat_id,"")
        await sqlitedb.set_permissions(chat_id=chat_id)

async def remove_task_and_store(core_member_id, index,callback_query):
    core_member_info = await sqlitedb.get_core_member_details(core_member_id,tasks=True)
    # # print(core_member_info['tasks'])
    # print(core_member_info)
    # return
    tasks = json.loads(core_member_info['tasks'])
    # print(tasks_assigned)
    # if 0 <= index <= len(tasks_assigned):
    #     tasks_assigned.pop(index)  # Remove the task at the specified index
    #     print(tasks_assigned)
    # print(tasks)
    # print(type(index))
    # print(index)
    tasks.pop(str(index))
    # re indexing in a consecutive manner
    tasks = {i+1: tasks[key] for i, key in enumerate(sorted(tasks.keys()))}
    # updated_tasks = " - ".join(task.strip() for task in tasks_assigned)
    await sqlitedb.store_core_team_info(core_team_index=core_member_id,tasks=json.dumps(tasks))
    await PostgresSQL.store_core_team_info(core_team_index=core_member_id,tasks=tasks)
    data_part = callback_query.data.split("-")
    core_member_id = data_part[2]
    await callback_query.edit_message_text(
        'Task has been successfully deleted',
        reply_markup = await student_council_keyboard.generate_back_button_to_core(core_member_id=core_member_id)
    )


async def update_task_status(core_member_id, index, callback_query):
# async def toggle_core_task_status(callback_query, core_member_id, index):
    # Retrieve core member info and parse tasks
    core_member_info = await sqlitedb.get_core_member_details(core_member_id, tasks=True)
    tasks = json.loads(core_member_info['tasks'])
    # print(tasks)
    
    # Initialize the "Back" button
    button = [InlineKeyboardButton("Back", callback_data="CORE-Toggle_task_status")]
    button = InlineKeyboardMarkup(inline_keyboard=[button])  # Inline keyboard for the "Back" button
    
    # Check if the specified task index exists
    if str(index) in tasks:
        current_status = tasks[str(index)].get('status', False)
        print(f"Current Status: {current_status}")
        tasks[str(index)]['status'] = not current_status
        # Store updated tasks back in the database
        await sqlitedb.store_core_team_info(core_team_index=core_member_id, tasks=json.dumps(tasks))
        
        # task = tasks[str(index)]['tasks']
        # Notify the user of successful update
        await callback_query.edit_message_text(
            f"Task {index} \n\nStatus changed to {'Done' if not current_status else 'Not done'}",
            reply_markup=button
        )
    else:
        # Handle case where the task index does not exist
        await callback_query.edit_message_text(
            'Task not found',
            reply_markup=button
        )


async def get_enft_team_violations():
    # Used to get the violations for the enforcement team
    all_event_ids = await sqlitedb.get_all_event_ids()
    for event_id in all_event_ids:
        event_data = await sqlitedb.retrieve_event_data(event_id=event_id)
        todays_date = await time.get_current_date()
        

async def store_enft_team_violations():
    """
    Retrieves all event records and checks for violations in relevant fields.
    Returns a list of violations with the corresponding field and due date.
    """
    all_event_ids = await sqlitedb.get_all_event_ids()

    # Loop through all event records
    for event_id in all_event_ids:
        event_data = await sqlitedb.retrieve_event_data(event_id=event_id)
        club_id = await sqlitedb.get_club_id_by_event_id(event_id=event_id)
        club_name = await sqlitedb.get_club_name_by_club_id(club_id=club_id)
        violations = []
        if event_data:
            # Check each field for violations
            violation = await time.check_field_violation(event_data['photos_link'], 'photos_link')
            if violation:
                violations.append(violation)

            violation = await time.check_field_violation(event_data['event_report'], 'event_report')
            if violation:
                violations.append(violation)

            violation = await time.check_field_violation(event_data['proposal_form'], 'proposal_form')
            if violation:
                violations.append(violation)

            violation = await time.check_field_violation(event_data['flyer_and_schedule'], 'flyer_and_schedule')
            if violation:
                violations.append(violation)

            violation = await time.check_field_violation(event_data['list_of_participants'], 'list_of_participants')
            if violation:
                violations.append(violation)
        if violations:
            for violation in violations:
                await sqlitedb.store_violation_details(violation=violation,club_name=club_name,status='open',time_remaining='72')
                # Implement a method such that the violations are loaded at a time into postgres database so that it saves the time.
                await PostgresSQL.store_violation_details(violation=violation,club_name=club_name,status='open',time_remaining='72')

