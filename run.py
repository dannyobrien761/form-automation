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
    cake_type = row[4]  # Assuming 'cake-type' is in the 5th column (index 4)
    cake_quantity = row[5]  # Assuming 'cake quantity' is in the 6th column (index 5)
    treat_type = row[7]  # Assuming 'treat-type' is in the 8th column (index 7)
    treat_quantity = row[8]  # Assuming 'treat-quantity' is in the 9th column (index 8)


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





def append_to_customer_info(order_sheet, customer_info_sheet, pricing_dict):
    """
    Appends the latest valid row to the 'customer-info' sheet if it's not a duplicate.
    
    Parameters:
        order_sheet (gspread.Worksheet): The worksheet object for 'order-info'.
        customer_info_sheet (gspread.Worksheet): The worksheet object for 'customer-info'.
        pricing_dict (dict): A dictionary with pricing information.
    """
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
        'custom': 10,
        'vanilla cake': 20,
        'brownie treat': 5,
        'delivery_fee': 10  # Delivery fee
    }

    # Append to customer-info sheet
    append_to_customer_info(order_sheet, customer_info_sheet, pricing_dict)

    

if __name__ == "__main__":
    main()
