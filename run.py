import gspread
from google.oauth2.service_account import Credentials


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

print(order_data)

# Access the worksheet containing the pricing model
pricing_sheet = SHEET.worksheet('price-list')
pricing_data = pricing_sheet.get_all_values()

print(pricing_data)

# Convert the pricing data to a dictionary for easier lookup
# Assuming the pricing model has 'cake-type' in the first column and price in the second
pricing_dict = {row[0]: float(row[1]) for row in pricing_data[1:]}  # Skipping header

# Iterate through each row in the order data (skipping header)
for row in order_data[1:]:
    cake_type = row[4]  # Assuming 'cake-type' is in the 5th column (index 4)
    cake_quantity = row[5]  # Assuming 'cake quantity' is in the 6th column (index 5)
    
    # Check if the cake type exists and quantity is valid
    if cake_type in pricing_dict and cake_quantity:
        # Convert cake quantity to an integer for calculation
        cake_quantity = int(cake_quantity)
        
        # Calculate the cost for the current row
        cake_cost = pricing_dict[cake_type] * cake_quantity
        
        print(f"Cake Type: {cake_type}, Quantity: {cake_quantity}, Total Cost: €{cake_cost}")
    else:
        print(f"Skipping row due to missing or invalid cake type/quantity: {row}")

        