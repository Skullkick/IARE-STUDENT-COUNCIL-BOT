from datetime import datetime, timedelta
import pytz

async def modify_event_date(event_date:str, num_of_days:int)->str:
    """
    Modifies the event_date by increasing or decreasing the number of days,
    considering Indian Standard Time (IST).

    :param event_date: The event date in 'DD/MM/YYYY' format.
    :param num_of_days: The number of days to increase or decrease (negative for reducing).
    :return: The updated event date in 'DD/MM/YYYY' format.
    """
    try:
        ist = pytz.timezone('Asia/Kolkata')
        date_obj = datetime.strptime(event_date, "%d/%m/%Y")
        localized_date = ist.localize(date_obj)
        updated_date = localized_date + timedelta(days=num_of_days)
        return updated_date.strftime("%d/%m/%Y")
    
    except ValueError:
        raise ValueError("The event_date must be in 'DD/MM/YYYY' format.")

async def get_current_date():
    """
    Asynchronously retrieves the current date in the Indian timezone (IST).

    Returns:
        date: The current date in the format YYYY-MM-DD in IST.
    """
    ist = pytz.timezone('Asia/Kolkata')

    # Get the current date and time in IST
    current_time_ist = datetime.now(ist)

    # Extract the current date
    current_date_ist = current_time_ist.date()

    return current_date_ist

async def is_future_date(date_str):
    if date_str:
        try:
            date = datetime.strptime(date_str, "%d/%m/%Y")  # Modify as per your actual date format
            return date > datetime.now()
        except ValueError:
            print(f"Invalid date format for {date_str}. Expected format is DD/MM/YYYY.")
            return False
    return False


async def check_field_violation(field_data, field_name):
    """
    Checks if the field has a violation considering IST timezone.
    :param field_data: The data stored in the format 'dd/mm/yyyy-status'.
    :param field_name: The name of the field being checked.
    :return: A dictionary with the field name and violation date if violated, otherwise None.
    """
    if field_data:
        try:
            # Extract date and status
            date_str, status = field_data.split('-')
            # Convert date string to a datetime object
            ist = pytz.timezone('Asia/Kolkata')
            due_date = datetime.strptime(date_str, "%d/%m/%Y")
            due_date = ist.localize(due_date).date()
            # Get the current date in IST
            today_date = await get_current_date()
            # If the deadline has passed and the status is 'not_submitted'
            if due_date < today_date and status == "not_submitted":
                return {
                    "field": field_name,
                    "due_date": date_str
                }
        except ValueError:
            print(f"Error parsing date for {field_name}: {field_data}")
    return None