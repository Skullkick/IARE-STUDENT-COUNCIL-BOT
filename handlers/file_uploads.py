import os
from utils import sqlitedb
from templates import report_template,club_events_templates

async def download_pdf(bot, message, options,event_id):
    chat_id = message.chat.id
    download_folder = "pdfs"
    # Checks the Status
    print(f"Event id : {event_id}")
    event_data = await sqlitedb.retrieve_event_data(event_id=event_id)
    event_name = await sqlitedb.get_event_info_by_id(event_id=event_id) #[1]
    event_name = event_name[1]
    print(f"event name : {event_name}, event data : {event_data}")
    # print(event_data)
    # Checks if the message is document or not.
    if message.document:
        mime_type = message.document.mime_type
        if mime_type == "application/pdf":
            # If download_folder does not exist then it creates a directory
            if not os.path.exists(download_folder):
                os.makedirs(download_folder)
            # Message Receiving the PDF.
            message_in_receive = await bot.send_message(chat_id,report_template.PDF_MESSAGE)
            # Download the PDF file with progress callback
            await message.download(
                file_name=os.path.join(download_folder, f"{event_name}_{options}.pdf"),
            )
            # Message After Receiving the PDF.
            await bot.edit_message_text(chat_id,message_in_receive.id, report_template.RECEIVED_PDF_MSG)
            # check_pdf_size returns 2 values whether the pdf is above 10mb or not and size of pdf
            await sqlitedb.set_permissions(chat_id)   
            student_council_chat_ids = await sqlitedb.get_all_student_council_chat_ids()
            for member_chat_id in student_council_chat_ids:
                await bot.send_document(member_chat_id,await get_pdf_path(pdf_folder=download_folder,pdf_name=f"{event_name}_{options}.pdf"))
            if options == "proposal_form":
                proposal_form_ = event_data['proposal_form'].split("-")
                print(proposal_form_)
                proposal_form = proposal_form_[0] + "-submitted"
                print(proposal_form)
                await sqlitedb.store_or_update_event_data(event_id=event_id,proposal_form=proposal_form)
            elif options == "flyer_schedule":
                flyer_ = event_data["flyer_and_schedule"].split("-")
                flyer = flyer_[0] + "-submitted"
                print(flyer)
                await sqlitedb.store_or_update_event_data(event_id=event_id,flyer_and_schedule=flyer)
            elif options == "report":
                report_ = event_data["event_report"].split("-")
                report_status = report_[0] + "-submitted"
                await sqlitedb.store_or_update_event_data(event_id=event_id,event_report=report_status)
            elif options == "list_of_participants":
                list_of_participants_ = event_data['list_of_participants'].split("-")
                participants_status = list_of_participants_[0] + "-submitted"
                await sqlitedb.store_or_update_event_data(event_id=event_id,list_of_participants=participants_status)
            await sqlitedb.set_permissions(chat_id)
            await bot.send_message(chat_id,club_events_templates.ADD_EVENT_DATA[5])
        else:
            await bot.send_message(chat_id, "This File type is not supported.")

async def recieve_link(bot, message):
    chat_id = message.chat.id
    event_id = await sqlitedb.check_permission(chat_id=chat_id,photos_drive_link=True)
    if message.text:
        text = message.text
        # Add the code to store the link in the event database
        event_data = await sqlitedb.retrieve_event_data(event_id=event_id)
        event_name = await sqlitedb.get_event_info_by_id(event_id=event_id)[1]
        # dd/mm/yy-status-link.
        photos_link_ = event_data['photos_link'].data.split("-")
        if len(photos_link_) == 2:
            photos_link = photos_link_[0] + f"-submitted-{text}"
        await sqlitedb.store_or_update_event_data(event_id=event_id,photos_link=photos_link)
        student_council_chat_ids = await sqlitedb.get_all_student_council_chat_ids()
        for member_chat_id in student_council_chat_ids:
            await bot.send_message(member_chat_id,f"Event name : {event_name}\n\nEvent photos : {text}")
        await sqlitedb.set_permissions(chat_id)
        await bot.send_message(chat_id,club_events_templates.ADD_EVENT_DATA[4])

async def get_pdf_path(pdf_folder, pdf_name):
    """
    Constructs the absolute path for a PDF file based on the folder and file name provided.

    :param pdf_folder: The folder where the PDF is located.
    :param pdf_name: The name of the PDF file.
    :return: The absolute path of the PDF file.
    """
    pdf_path = os.path.join(pdf_folder, pdf_name)
    return os.path.abspath(pdf_path)