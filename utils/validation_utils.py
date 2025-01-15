from email_validator import validate_email, EmailNotValidError
import phonenumbers, re,datetime
from tkinter_utils import MessageBoxHandler

#for full name inputs
def is_valid_name(name):
    try:
        name_pattern = r'^([A-Za-zÄÖÜäöüß]+(-[A-Za-zÄÖÜäöüß]+)?)\s+([A-Za-zÄÖÜäöüß]+(-[A-Za-zÄÖÜäöüß]+)?)$'
        if re.match(name_pattern, name, re.UNICODE):
            return True
        else:
            raise ValueError("Invalid name: Must only contain letters and optional hyphen.")
    except ValueError as e:
        MessageBoxHandler.show_error("Validation Error", str(e))
        return False

def is_valid_first_name(first_name):
    first_name_pattern = r'^([A-Za-zÄÖÜäöüß]+(-[A-Za-zÄÖÜäöüß]+)?$'
    try:
        if re.match(first_name_pattern, first_name, re.UNICODE):
            return True
        else:
            raise ValueError("Invalid first name: Must only contain letters and optional hyphen.")
    except ValueError as e:
        MessageBoxHandler.show_error("Validation Error", str(e))
        False
    
def is_valid_last_name(second_name):
    try:
        second_name_pattern = r'^[A-Za-zÄÖÜäöüß]+(-[A-Za-zÄÖÜäöüß]+)?)$'
        if re.match(second_name_pattern, second_name, re.UNICODE):
            return True
        else:
            raise ValueError("Invalid last name: Must only contain letters and optional hyphen.")
    except ValueError as e:
        MessageBoxHandler.show_error("Validation Error", str(e))
        False

def capitalize_name(name):
    def capitalize_hyphen(part):
        return '-'.join(word.capitalize() for word in part.split('-'))
    return ' '.join(capitalize_hyphen(part) for part in name.split())


def is_valid_address(address):
    try:
        address_pattern = r'^([A-Za-zäöüÄÖÜß\s-]+)\s+(\d+)(?:\s((?:Apt|Apartment|Top|Unit|Flat|/)\.?\s*\d+))?\s+(\d{4})\s+([A-Za-zäöüÄÖÜß\s.-]+)$'
        if re.match(address_pattern, address, re.UNICODE):
            return True
        else:
            raise ValueError("Invalid address: Must follow the patter '<Street Name> <House Number> [Optional Unit] <Postal Code> <City>'.")
    except ValueError as e:
        MessageBoxHandler.show_error("Validation Error", str(e))
        False

def is_valid_date(date):
    try:
        date_pattern = r'^(0?[1-9]|[12][0-9]|3[01])\.(0?[1-9]|1[0-2])\.(19[2-9][0-9]|20[0-1][0-9]|202[0-4])$'
        date = re.sub(r'[-/,_]', ".", date)
        if re.match(date_pattern, date):
            day, month, year = map(int, date.split('.'))
            validated_date = datetime.datetime(year, month, day)
            return validated_date.strftime("%d.%m.%Y")
        else:
            raise ValueError("Date format is incorrect. Must be DD.MM.YYYY.")
    except ValueError as e:
        MessageBoxHandler.show_error("Validation Error", str(e))
        False
    

def is_valid_phone_number(number):
    try:
        number = phonenumbers.parse(number)
        return phonenumbers.is_valid_number(number)
    except phonenumbers.phonenumberutil.NumberParseException as e:
        MessageBoxHandler.show_error("Validation Error", str(e))
        False

def is_valid_email_address(email_address):
    try:
        email_address = validate_email(email_address).normalized
        return True
    except EmailNotValidError as e:
        MessageBoxHandler.show_error("Validation Error", f"Invalid email address: {str(e)}")
        return False

