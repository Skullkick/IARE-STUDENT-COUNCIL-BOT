from utils import sqlitedb
from handlers import council_members
from keyboards import student_council_keyboard
from templates import council_templates
async def add_core_team_details(bot, chat_id):
    """
    Prompt the user for core team details if any fields are missing in the temporary database.
    
    :param bot: The bot instance.
    :param chat_id: The chat ID of the user to send the prompts.
    """
    field_presence_dictionary = await sqlitedb.check_temp_core_team_field_presence(chat_id)
    
    # Check each field and prompt for missing core team details
    if not field_presence_dictionary["core_name"]:
        await bot.send_message(chat_id, "Send the name of the core")
    elif not field_presence_dictionary["core_member_name"]:
        await bot.send_message(chat_id, "Send the name of the core team member")
    elif not field_presence_dictionary["core_member_chat_id"]:
        await bot.send_message(chat_id, "Send the chat ID of the core team member")
    else:
        await sqlitedb.set_permissions(chat_id, core_team=False)
        await council_members.initialize_storing_core_values(chat_id)
        # All fields are filled, proceed to confirmation or next step
        await bot.send_message(chat_id, "All core team details are complete. Thank you!")
        await bot.send_message(chat_id,council_templates.council_text[0],reply_markup = student_council_keyboard.add_view_core_button)

async def add_student_council_details(bot, chat_id):
    """
    Prompt the user for student council details if any fields are missing in the database.
    
    :param bot: The bot instance.
    :param chat_id: The chat ID of the user to send the prompts.
    """
    # Check field presence in the student council table
    field_presence_dictionary = await sqlitedb.check_student_council_field_presence(chat_id)

    # Check each field and prompt for missing student council details
    if not field_presence_dictionary["name"]:
        await bot.send_message(chat_id, "Send the name of the student council member")
    elif not field_presence_dictionary["any_position"]:
        await bot.send_message(chat_id,"Choose the position in student council",reply_markup = student_council_keyboard.choose_student_council_position)
        
    else:
        await sqlitedb.set_permissions(chat_id, council_member=True)  # Update permissions as needed
        # All fields are filled, proceed to confirmation or next step
        await bot.send_message(chat_id, "All student council details are complete. Thank you!")

async def add_enforcement_team_details(bot, chat_id):
        # Check if the user already exists in the enforcement_team table
    field_presence_dictionary = await sqlitedb.check_temp_enforcement_team_field_presence(chat_id)
    # print(field_presence_dictionary)

    # Check if the user's details are missing and prompt for the missing ones
    if not field_presence_dictionary["chat_id"]:
        await bot.send_message(chat_id, "Please provide the chat ID for enforcement team member.")
    elif not field_presence_dictionary["name"]:
        await bot.send_message(chat_id, "Please provide the name for the enforcement team member.")
    else:
        # All fields are filled, proceed to confirmation or next step
        await bot.send_message(chat_id, "You have successfully registered member of the enforcement team.")
