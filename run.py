import gspread
from google.oauth2.service_account import Credentials
import re
from datetime import datetime, timedelta

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# access sheet using open object and passing it name of given spreadsheet katescakes-automation
SHEET = GSPREAD_CLIENT.open('katescakes-automation')


# Access the worksheet containing the order info
order_sheet = SHEET.worksheet('order-info')
order_data = order_sheet.get_all_values()
# Access the worksheet containing customer-info
customer_email_sheet = SHEET.worksheet('customer-info')




def get_customer_data():
    """
    Get order data (name and email) from the user.
    The data should be a valid name and a valid email address.
    """
    while True:
        print("if you would like to order a cake please fill out the below.")
        print("what is your name and email ? please seperate them  by a comma.")
        print("Example: John Doe,johndoe@example.com")

        data_str = input("Enter your data here:\n")
        customer_data = data_str.split(",")

        if validate_order_data(customer_data):
            print("Order data is valid!")
            break

    return customer_data

def validate_order_data(customer_data):
    """
    Validate the order data. The name should not be empty, and the email
    must be in a valid format (e.g., someone@example.com).
    """
    if len(customer_data) != 2:
        print(f"Invalid input. You must provide exactly 2 values (name and email).")
        return False

    name = customer_data[0].strip()
    email = customer_data[1].strip()

    # Validate name (non-empty)
    if not name:
        print("Invalid data: Name cannot be empty.")
        return False

    # Validate email format using a regular expression
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    if not re.match(email_regex, email):
        print("Invalid data: Email is not in a valid format (e.g., someone@example.com).")
        return False

    return True


def get_cake_date():
    """
    Get a valid cake order date from the user.
    The date must be in the format 'YYYY-MM-DD'.
    """
    while True:
        print("Please enter the date you want the cake by, but you must give us two days notice to get your cake ready.")
        print("Data should be in the format: year-month-day.")
        print("Example: 2024-09-25\n")

        date_str = input("Enter the date here:\n")

        if validate_cake_date(date_str):
            print("Date is valid!")
            break

    return date_str


def validate_cake_date(date_str):
    """
    Validate that the input is in 'YYYY-MM-DD' format, is a valid date,
    and the date is at least two days in the future.
    """
    try:
        # Try to parse the date string into a datetime object
        order_date = datetime.strptime(date_str, "%Y-%m-%d")
        
        # Get the current date
        current_date = datetime.now()

        # Check if the order date is at least two days in the future
        if order_date < current_date + timedelta(days=2):
            print("Invalid date: The order must be at least two days in the future.")
            return False
    except ValueError:
        print("Invalid data: Date must be in the format 'YYYY-MM-DD' and a valid date.")
        return False

    return True








def get_cake_type():
    """
    Get the cake type selected by the customer.
    The cake type must be one of the available options.
    """
    cake_options = {
        "1": "chocolate biscuit",
        "2": "vanilla cake"
    }

    while True:
        print("Please choose the cake type from the following options:")
        print("1. Chocolate Biscuit")
        print("2. Vanilla cake\n")

        cake_type_choice = input("Enter your choice (1 or 2):\n")

        if cake_type_choice in cake_options:
            print(f"Cake type '{cake_options[cake_type_choice]}' selected!")
            return cake_options[cake_type_choice]
        else:
            print("Invalid cake type. Please enter '1' for Chocolate Biscuit or '2' for Vanilla Sponge.")



def validate_cake_type(cake_type):
    """
    Validate the cake type input.
    It must be '1' for 'Chocolate Biscuit' or '2' for 'Vanilla Sponge'.
    """
    valid_options = {"1": "Chocolate Biscuit", "2": "Vanilla Sponge"}

    if cake_type not in valid_options:
        print("Invalid cake type. Please enter '1' for Chocolate Biscuit or '2' for Vanilla Sponge.")
        return False

    return True


def get_cake_quantity():
    """
    Get the cake quantity from the customer.
    It must be a positive integer greater than zero.
    """
    while True:
        print("Please enter the quantity of cakes:")
        cake_quantity = input("Enter the cake quantity (must be a number greater than 0):\n")

        if validate_cake_quantity(cake_quantity):
            print("Cake quantity is valid!")
            break

    return int(cake_quantity)


def validate_cake_quantity(cake_quantity):
    """
    Validate the cake quantity input.
    It must be a positive integer greater than zero.
    """
    try:
        quantity = int(cake_quantity)
        if quantity <= 0:
            raise ValueError("The quantity must be greater than zero.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        return False

    return True




def update_order_worksheet(customer_data, cake_date, cake_type, cake_quantity):
    """
    Update the 'order-info' worksheet by adding a new row with the provided data.
    """
    print("Updating order-info worksheet...\n")
    
    # Access the 'order-info' worksheet
    order_worksheet = SHEET.worksheet('order-info')
    
    # Create a new row to append, based on the provided input
    # Assume customer_data is a list with [name, email]
    new_order_row = [
        customer_data[0],  # name
        customer_data[1],  # email
        cake_date,         # date of cake order
        cake_type,         # type of cake
        cake_quantity      # quantity of cakes
    ]
    
    # Append the new row to the worksheet
    order_worksheet.append_row(new_order_row)

    print("Order-info worksheet updated successfully.\n")
    return new_order_row  # Return the row to use in other functions
    
    
    

"""
# section to handle updating customer-info sheet from order-infor page
def is_valid_row(row):
    
    Checks if the row contains meaningful data and is not just an empty row.
    
    Parameters:
        row (list): The row data from the sheet.
    
    Returns:
        bool: True if the row contains valid data, False otherwise.
    
    # Check if key fields (e.g., 'cake-type', 'cake-quantity') are non-empty
    cake_type = row[4].strip()  # Assuming 'cake-type' is in the 5th column (index 4)
    cake_quantity = row[5].strip()  # Assuming 'cake quantity' is in the 6th column (index 5)
    
    return bool(cake_type and cake_quantity) 

"""
"""
def get_latest_valid_row(sheet):
   
    Gets the latest valid row from the 'order-info' sheet that contains valid data.
    
    Parameters:
        sheet (gspread.Worksheet): The worksheet object for 'order-info'.
    
    Returns:
        list: The latest valid row with data, or None if no valid row is found.
   
    # Get all rows from the sheet
    all_rows = sheet.get_all_values()

    # Iterate from the last row backwards to find the latest valid row
    for row in reversed(all_rows):
        if is_valid_row(row):
            return row  # Return the first valid row found from the bottom up
    
    # If no valid row is found, return None
    return None
 """

def calculate_order_cost(pricing_dict, row):
    """
    Fetches the latest valid row from the 'order-info' sheet, checks if 'cake-type' and 'treat-type' exist
    in the pricing dictionary, validates 'cake-quantity' and 'treat-quantity', and calculates
    the total order cost.
    
    Parameters:
        pricing_dict (dict): A dictionary with 'cake-type' or 'treat-type' as keys and their prices as values.
        row (list): The row data from the sheet.
    
    Returns:
        float: The total calculated order cost.
    """
    cake_type = row[3]  # Assuming 'cake-type' is in the 5th column (index 4)
    cake_quantity = row[4]  # Assuming 'cake quantity' is in the 6th column (index 5)
    #treat_type = row[6]  # Assuming 'treat-type' is in the 8th column (index 7)
    #treat_quantity = row[7]  # Assuming 'treat-quantity' is in the 9th column (index 8)


    order_cost = 0  # Initialize the order cost

    # Check if 'cake-type' exists in the pricing dictionary and 'cake-quantity' is valid
    if cake_type in pricing_dict:
        try:
            cake_quantity = int(cake_quantity)  # Convert to integer if valid
            order_cost += pricing_dict[cake_type] * cake_quantity
        except ValueError:
            print(f"Invalid cake quantity for {cake_type}. Skipping cake cost calculation.")

    # Check if 'treat-type' exists in the pricing dictionary and 'treat-quantity' is valid
    #if treat_type in pricing_dict:
        #try:
           # treat_quantity = int(treat_quantity)  # Convert to integer if valid
            #order_cost += pricing_dict[treat_type] * treat_quantity
        #except ValueError:
            #print(f"Invalid treat quantity for {treat_type}. Skipping treat cost calculation.")

    print(f"your order costs: {order_cost}.")
    return order_cost




"""
def append_to_customer_info(order_sheet, customer_info_sheet, pricing_dict):
    
    Appends the latest valid row to the 'customer-info' sheet if it's not a duplicate.
    
    Parameters:
        order_sheet (gspread.Worksheet): The worksheet object for 'order-info'.
        customer_info_sheet (gspread.Worksheet): The worksheet object for 'customer-info'.
        pricing_dict (dict): A dictionary with pricing information.
    
    # Get the latest valid row from the 'order-info' sheet
    latest_row = get_latest_valid_row(order_sheet)
    
    if latest_row is None:
        print("No valid row found. No data to append.")
        return

    # Extract name, email, and order-date from the latest row
    name = latest_row[0]  # Assuming 'name' is in the 1st column (index 0)
    email = latest_row[1]  # Assuming 'email' is in the 2nd column (index 1)
    order_date = latest_row[2]  # Assuming 'order-date' is in the 3rd column (index 2)

    # Calculate the order cost
    order_cost = calculate_order_cost(pricing_dict, latest_row)


    # Append order_cost to the latest_row
    latest_row.append(order_cost)  # Add order cost as the last column

    # Check if the combination of email and order_date already exists in the 'customer-info' sheet
    customer_data = customer_info_sheet.get_all_values()
    for row in customer_data:
        if len(row) > 2 and row[1] == email and row[2] == order_date:
            print(f"Entry with email {email} and order date {order_date} already exists. No duplicate added.")
            return

    # Append the latest_row to the 'customer-info' sheet
    customer_info_sheet.append_row([name, email, order_date, order_cost])
    print(f"Added new entry to customer-info: {name}, {email}, {order_date}, {order_cost}")

    latest_order_cost = calculate_order_cost(pricing_dict, latest_row)
    print(f"The total order cost is: {latest_order_cost}")
"""

def append_new_entries_to_customer_info(order_sheet, customer_info_sheet, pricing_dict):
    """
    Appends all new entries from the 'order-info' sheet to the 'customer-info' sheet.
    Only rows that have not yet been added (based on 'email' and 'order-date' combination) will be appended.
    
    Parameters:
        order_sheet (gspread.Worksheet): The worksheet object for 'order-info'.
        customer_info_sheet (gspread.Worksheet): The worksheet object for 'customer-info'.
        pricing_dict (dict): A dictionary with pricing information.
    """
    # Get all rows from the 'order-info' sheet
    all_order_rows = order_sheet.get_all_values()

    # Get all rows from the 'customer-info' sheet (to check for duplicates)
    customer_data = customer_info_sheet.get_all_values()
    
    # Extract the email and order-date combinations from customer-info for quick comparison
    customer_info_combinations = set((row[1], row[2]) for row in customer_data[1:])  # Exclude header

    # Iterate over each row in the 'order-info' sheet
    for row in all_order_rows[1:]:  # Exclude header
        # Extract email and order-date
        email = row[1]  # Assuming 'email' is in the 2nd column (index 1)
        order_date = row[2]  # Assuming 'order-date' is in the 3rd column (index 2)
        
        # Check if the combination of email and order_date already exists in customer-info
        if (email, order_date) not in customer_info_combinations:
            # If not a duplicate, calculate the order cost and append the new entry
            order_cost = calculate_order_cost(pricing_dict, row)
    
            
            # Append order_cost to the row
            row.append(order_cost)

            # Append name, email, order_date, and order_cost to customer-info
            customer_info_sheet.append_row([row[0], email, order_date, order_cost])
            
            # Update the set with the new combination
            customer_info_combinations.add((email, order_date))

            print(f"Added new entry: {row[0]}, {email}, {order_date}, {order_cost}")
        else:
            pass


def process_new_order(customer_data, cake_date, cake_type, cake_quantity, treat_type=None, treat_quantity=0, pricing_dict=None):
    """
    Update order-info sheet with new customer data, calculate the order cost,
    and append the new entry (including cost) to the customer-info sheet.
    """
    # Update the order-info sheet
    new_order_row = update_order_worksheet(customer_data, cake_date, cake_type, cake_quantity)
    
    # Calculate the order cost using the new_order_row
    order_cost = calculate_order_cost(pricing_dict, new_order_row)
    print(f"Total order cost calculated: {order_cost} EUR")

    # Append to customer-info sheet
    append_new_entries_to_customer_info(order_sheet, customer_info_sheet, pricing_dict)

    print("Order processed successfully.")


# Example usage
def main():
    # Authorize and access the spreadsheet
    GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
    SHEET = GSPREAD_CLIENT.open('katescakes-automation')

    # Access the worksheets
    order_sheet = SHEET.worksheet('order-info')
    customer_info_sheet = SHEET.worksheet('customer-info')

    # Define pricing dictionary
    pricing_dict = {
        'chocolate biscuit': 25,
        'vanilla cake': 20,
        'delivery_fee': 10  # Delivery fee
    }

    # Example Usage
    customer_data = get_customer_data()  # Get and validate name and email
    cake_date = get_cake_date()       # Get and validate date
    cake_type = get_cake_type()       # Get and validate cake type
    cake_quantity = get_cake_quantity()  # Get and validate cake quantity
    process_new_order(customer_data, cake_date, cake_type, cake_quantity, pricing_dict)
    # Update the 'order-info' worksheet
    #new_order_row = update_order_worksheet(customer_data, cake_date, cake_type, cake_quantity)
    #order_cost = calculate_order_cost(pricing_dict, new_order_row)
    # Append to customer-info sheet
    #append_to_customer_info(order_sheet, customer_info_sheet, pricing_dict)
    #append_new_entries_to_customer_info(order_sheet, customer_info_sheet, pricing_dict)

    

if __name__ == "__main__":
    main()
