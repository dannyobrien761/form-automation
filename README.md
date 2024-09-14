# Form Automation

#### Introduction:
The **Form Automation** project is a Python-based application designed to streamline data collection and management for cake orders. It integrates with Google Sheets, automatically updating records for both orders and customer information, and calculates the total cost of each order. The project’s primary goal is to simplify the process of gathering customer data, managing orders, and calculating costs efficiently, reducing manual errors and time spent on administrative tasks.

[live version of project](https://form-automation-369956b5546f.herokuapp.com/)

![am-i-responsive pic of heroku running application](/assets/images/am-i-responsive.PNG)
#### How to Use:
1. **User Input:** Customers input their name, email, cake type, desired order date, and quantity.
2. **Order Processing:** The system validates the inputs and updates the “order-info” sheet in Google Sheets with the new order.
![order-info spreadsheet pic](/assets/images/spreadsheet-snip.PNG)
3. **Cost Calculation:** The program calculates the total cost of the order based on the cake type and quantity.
4. **Customer Data Storage:** The system checks for duplicate records in the “customer-info” sheet and appends the new order details, including the order cost.
5. **Automated Email:** Emails can be sent to customers using their recorded information for notifications or follow-ups.

#### Features:
- **Data Validation:** Ensures inputs are correct, such as valid email formats and dates that provide sufficient preparation time.
- **Cost Calculation:** Automatically computes the cost of orders based on predefined pricing for cake types.
- **Duplicate Prevention:** Checks for duplicate customer entries to avoid multiple records for the same order.
- **Automated Data Updates:** Integrates seamlessly with Google Sheets, updating customer and order data in real-time. Here is a pic of how the customer-info spreadsheet is updated:

![pic of google spreadsheet app is updating](/assets/images/customer-info-snip.PNG)

#### Future Features:
- **Order Confirmation Emails:** Automatic emails sent to customers upon order submission.
- **Enhanced Data Validation:** More detailed checks on order types and special requests.
- **Order History Tracking:** Allow customers to track the status of their order and view past orders.
- **Analytics Dashboard:** Real-time reports on sales, popular cake types, and customer data trends.

#### Data Model:
- **order-info Sheet:**
  - Customer name, email, cake type, quantity, and order date are stored.
  - Each row represents one order.
- **customer-info Sheet:**
  - Customer email, name, and order costs are tracked.
  - Prevents duplication of customer entries.

#### Testing:
The project has been tested through:
- **PEP8 Linter:** Code has been validated to ensure it follows Python’s coding standards.
- **Invalid Inputs:** Handled invalid email formats, incorrect dates, and negative or zero quantities.
- **Local and Heroku Terminals:** Successfully ran tests both locally and in the Heroku terminal, ensuring smooth functionality across environments.

#### Bugs:
- **Initial `NoneType` Error in Cost Calculation:** Encountered when the cake type was not properly assigned in the order row, leading to a failure in calculating the cost.
- **Duplicate Customer Entries:** Initially, the system allowed duplicates in the “customer-info” sheet.
- **Unvalidated Cake Quantity:** The program sometimes allowed non-numeric values for cake quantity.

#### Solved Bugs:
- **Fixed `NoneType` Error:** Resolved by correctly passing the cake type from the user input to the order worksheet.
- **Duplicate Prevention:** Implemented a check in the “customer-info” sheet to avoid appending the same customer multiple times.
- **Quantity Validation:** Added validation logic to ensure the cake quantity input is a valid positive integer.

#### Remaining Bugs:
- **Email Sending Integration:** The email notification system still requires proper integration and testing to function as expected.
  
#### Credits:
- **Google Sheets API Documentation:** Provided foundational information on interacting with Google Sheets using Python.
- **code institute** love sandwiches project by the code institure found here: https://github.com/Code-Institute-Solutions/love-sandwiches-p5-sourcecode
- **stack overflow** I took the validate email- expression in the run.py validate_order definition below from this thread : https://stackoverflow.com/questions/8022530/how-to-check-for-valid-email-address

# Validate email format using a regular expression
    #cred-stack overflow thread link in readme
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    if not re.match(email_regex, email):
        print("Error: Email isn't in valid format (e.g., some@example.com).")
        return False

    return True