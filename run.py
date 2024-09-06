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

def calculate_latest_order_cost(pricing_dict):
    """
    Fetches the latest row from the 'order-info' sheet, checks if 'cake-type' and 'treat-type' exist
    in the pricing dictionary, validates 'cake-quantity' and 'treat-quantity', and calculates
    the total order cost.
    
    Parameters:
        pricing_dict (dict): A dictionary with 'cake-type' or 'treat-type' as keys and their prices as values.
    
    Returns:
        float: The total calculated order cost. If no valid data is found, returns 0.
    """


    # Get the latest row from the order-info sheet
    latest_row = order_sheet.get_all_values()[-1]

    # Extract the relevant columns from the latest row
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

# Example usage of the function with a pricing dictionary
pricing_dict = {
    'chocolate biscuit': 25,
    'custom': 10,
    'vanilla cake': 20,
    'brownie treat': 5
}

latest_order_cost = calculate_latest_order_cost(pricing_dict)
print(f"The total order cost is: {latest_order_cost}")
