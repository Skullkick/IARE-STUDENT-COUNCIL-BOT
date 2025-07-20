from utils import sqlitedb
from keyboards import student_council_keyboard
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
import json
# from 

council_text = ("Add or view core team","Add or View Enforcement team","Welcome to the student council management dashboard","Your resignation as an Student counil Admin has been processed. We value your efforts and wish you the best.",
                "Choose a task to view its details.")
core_team = ("Click on a member to view and edit priviliges","There are no core members available")

async def core_member_info(core_member_id,edit_core = False,delete_tasks = False):
    """This function formats and returns the core member information as a string.

    :param core_member_id: The ID of the core member.
    """
    core_member_info = await sqlitedb.get_core_info_by_id(core_member_id)
    if core_member_info:
        core_name, core_member_name, core_member_chat_id,tasks = core_member_info
        # print(tasks,core_member_info)
    # if tasks:
    #     print(tasks)
    #     tasks_assigned = "\n".join(tasks.split("-")) if len(tasks) >= 2 else tasks
    # else:
    #     tasks_assigned = "No tasks have been assigned"
    if tasks:
        tasks = json.loads(tasks)
        # Initialize an empty list to store the formatted text
        task_text = []

        # Iterate over the tasks dictionary
        for key, value in tasks.items():
            # Get task status as "Not done" if status is False, "Done" if True
            status = "Not done" if not value['status'] else "Done"

            # Format the text for each task and append it to the task_text list
            task_text.append(f"{key}) {value['task']}, status : {status}")

        # Join all the formatted task texts into one string
        tasks_assigned = "\n".join(task_text)
    else:
        tasks_assigned = "No tasks have been assigned"

    core_info_text = f"""
```CORE MEMBER INFO

CORE NAME: {core_name}\n
CORE MEMBER NAME: {core_member_name}\n
TASKS ASSIGNED : \n{tasks_assigned}
```
"""
    if edit_core == True:
        core_info_text = f"""
```CORE MEMBER INFO

CORE NAME: {core_name}\n
CORE MEMBER NAME: {core_member_name}\n
TASKS ASSIGNED : \n{tasks_assigned}

What you would like to edit.
```
"""
    if delete_tasks == True:
        # tasks_assigned = "\n".join(f"{index+1}: {task.strip()}" for index, task in enumerate(tasks_assigned))
        core_info_text = f"""
```TASKS
Choose the index to delete a task\n
{tasks_assigned}
"""
    return core_info_text

async def delete_core_member(core_member_id):
    """
    Deletes a core member from the database and returns a confirmation message including the core member's name.
    
    :param core_member_id: The ID of the core member to be deleted.
    :return: A message indicating the core member has been deleted successfully.
    """
    try:
        # Retrieve the core name of the member before deletion
        core_details_dict = await sqlitedb.get_core_member_details(core_member_id=core_member_id, core_name=True)
        
        if not core_details_dict or 'core_name' not in core_details_dict:
            return f"Core member with ID {core_member_id} not found."

        core_name = core_details_dict['core_name']
        if await sqlitedb.delete_core_member_by_index(core_member_index=core_member_id) is True:
            # Return success message
            return f"'{core_name}' has been deleted successfully."

    except Exception as e:
        print(f"Error deleting core member: {e}")
        return f"An error occurred while trying to delete the core member with ID {core_member_id}."


async def start_student_council_buttons(bot,message):
    chat_id = message.chat.id
    # Step 1: Check the chat_id in the database
    council_details = await sqlitedb.get_student_council_member_details(chat_id)
    
    if council_details is None:
        # Handle case where chat_id is not found
        await bot.send_message(chat_id, "You are not part of the Student Council.")
        return
    
    name = council_details.get("Name")
    position = council_details.get("position")

    # Step 2: Generate welcome message based on position and name
    if position and name:
        welcome_message = f"Welcome {name}, the esteemed {position} of the Student Council!"
    else:
        welcome_message = "Welcome to the Student Council!"
    await message.reply_text(welcome_message,reply_markup = student_council_keyboard.start_buttons_student_council)

async def start_enforcement_member_buttons(bot,chat_id):
    text = "Click on \"View Violations\" to view the violations"
    button = [InlineKeyboardButton("View Violations",callback_data="ENFT-view_violations")]
    button = InlineKeyboardMarkup(inline_keyboard=button)
    await bot.send_message(chat_id,text,reply_markup = button)

# async def start_core_member_buttons(bot,chat_id):
#     print("Trying to retrieve data from database.")
#     core_member_data = await sqlitedb.get_core_member_info_by_chat_id(chat_id)
#     print("2")
#     core_member_id = core_member_data['core_member_index']
#     print("3")
#     text = await core_member_info(core_member_id=core_member_id)
#     print("4")
#     try:
#         print("2")
#         button = []
#         button.append(InlineKeyboardButton("Back",callback_data="CORE-Toggle_task_status"))
#         button = InlineKeyboardMarkup(inline_keyboard=[button])
#         print(button)
#     except Exception as e:
#         print(f"Error while generating button for core member : {e}")
#     await bot.send_message(chat_id,text,reply_markup=button)

async def start_core_member_buttons(bot,message):
    chat_id = message.chat.id
    core_member_info = await sqlitedb.get_core_member_info_by_chat_id(chat_id)
    core_name = core_member_info.get('core_name')
    core_member_name = core_member_info.get('core_member_name')
    core_member_chat_id = core_member_info.get('core_member_chat_id')
    tasks = core_member_info.get('tasks')
    if tasks:
        tasks = json.loads(tasks)
        # Initialize an empty list to store the formatted text
        task_text = []
        # Iterate over the tasks dictionary
        for key, value in tasks.items():
            # Get task status as "Not done" if status is False, "Done" if True
            status = "Not done" if not value['status'] else "Done"

            # Format the text for each task and append it to the task_text list
            task_text.append(f"{key}) {value['task']}, status : {status}")

        # Join all the formatted task texts into one string
        tasks_assigned = "\n".join(task_text)
    else:
        tasks_assigned = "No tasks have been assigned"
    # Create a structured message with the core team member details
    message = (f"Core Team Name: {core_name}\n"
               f"Core Member Name: {core_member_name}\n"
               f"Tasks: {tasks_assigned}")
    button = []
    button.append(InlineKeyboardButton("Toggle Task Status", callback_data="CORE-Toggle_task_status"))
    button = InlineKeyboardMarkup(inline_keyboard=[button])
    print(button)
    await bot.send_message(chat_id,message,reply_markup = button)

async def student_council_member_profile_text(chat_id):
    council_details = await sqlitedb.get_student_council_member_details(chat_id=chat_id)

    name = council_details.get("Name")
    position = council_details.get("position")

    if position and name:
        profile_text = (
                    f"Student Council Member Profile:\n"
                    f"Name: {name}\n"
                    f"Position: {position}\n"
                )
        return profile_text

    
async def generate_club_info_text_single_message(club_info: dict) -> str:
    """
    Generate a single message based on the club information.
    
    Args:
        club_info (dict): The dictionary containing club information.
        
    Returns:
        str: A single string containing all club details.
    """
    if not club_info:
        return "No club information found for the given chat ID."
    
    return f"""
```CLUB
Club Name: {club_info['name']}, "
Description: {club_info['description']}, "
President: {club_info['president']}, "
Vice President: {club_info['vice_president']}"
```
"""

