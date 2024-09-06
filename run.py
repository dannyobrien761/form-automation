import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint


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

def is_valid_row(row):
    """
    Checks if the row contains meaningful data and is not just an empty row.
    
    Parameters:
        row (list): The row data from the sheet.
    
    Returns:
        bool: True if the row contains valid data, False otherwise.
    """
    # Check if key fields (e.g., 'cake-type', 'cake-quantity') are non-empty
    cake_type = row[4].strip()  # Assuming 'cake-type' is in the 5th column (index 4)
    cake_quantity = row[5].strip()  # Assuming 'cake quantity' is in the 6th column (index 5)
    
    return bool(cake_type and cake_quantity) 

def get_latest_valid_row(sheet):
    """
    Gets the latest valid row from the 'order-info' sheet that contains valid data.
    
    Parameters:
        sheet (gspread.Worksheet): The worksheet object for 'order-info'.
    
    Returns:
        list: The latest valid row with data, or None if no valid row is found.
    """
    # Get all rows from the sheet
    all_rows = sheet.get_all_values()

    # Iterate from the last row backwards to find the latest valid row
    for row in reversed(all_rows):
        if is_valid_row(row):
            return row  # Return the first valid row found from the bottom up
    
    # If no valid row is found, return None
    return None

def calculate_latest_order_cost(pricing_dict):
    """
    Fetches the latest valid row from the 'order-info' sheet, checks if 'cake-type' and 'treat-type' exist
    in the pricing dictionary, validates 'cake-quantity' and 'treat-quantity', and calculates
    the total order cost.
    
    Parameters:
        pricing_dict (dict): A dictionary with 'cake-type' or 'treat-type' as keys and their prices as values.
    
    Returns:
        float: The total calculated order cost. If no valid data is found, returns 0.
    """
    
    # Get the latest valid row
    latest_row = get_latest_valid_row(order_sheet)

    if latest_row is None:
        print("No valid row found. No cost calculation.")
        return 0  # Return 0 if no valid row is found

    # Extract the relevant columns from the latest valid row
    cake_type = latest_row[4]  # Assuming 'cake-type' is in the 5th column (index 4)
    cake_quantity = latest_row[5]  # Assuming 'cake quantity' is in the 6th column (index 5)
    treat_type = latest_row[7]  # Assuming 'treat-type' is in the 8th column (index 7)
    treat_quantity = latest_row[8]  # Assuming 'treat-quantity' is in the 9th column (index 8)

    order_cost = 0  # Initialize the order cost

    # Check if 'cake-type' exists in the pricing dictionary and 'cake-quantity' is valid
    if cake_type in pricing_dict:
        try:
            cake_quantity = int(cake_quantity)  # Convert to integer if valid
            order_cost += pricing_dict[cake_type] * cake_quantity
        except ValueError:
            print(f"Invalid cake quantity for {cake_type}. Skipping cake cost calculation.")

    # Check if 'treat-type' exists in the pricing dictionary and 'treat-quantity' is valid
    if treat_type in pricing_dict:
        try:
            treat_quantity = int(treat_quantity)  # Convert to integer if valid
            order_cost += pricing_dict[treat_type] * treat_quantity
        except ValueError:
            print(f"Invalid treat quantity for {treat_type}. Skipping treat cost calculation.")

    return order_cost

# pricing dictionary for cake and treat types
pricing_dict = {
    'chocolate-biscuit': 25,
    'custom': 10,
    'vanilla-cake': 20,
    'brownie': 5
}

latest_order_cost = calculate_latest_order_cost(pricing_dict)
print(f"The total order cost is: {latest_order_cost}")
