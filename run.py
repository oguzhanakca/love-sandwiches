import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json",scopes=SCOPE)
GSPREAD_CLIENT = gspread.authorize(CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")

def get_sales_data():
    """
    Get sales figures input from the user
    """
    while True:
        print("Please enter sales data from the last market.\nData should be six number, seperated by commas.\nExample: 10,20,30,40,50,60")
        data_str = input("Enter your data here: ")
        sales_data = data_str.split(",")
        if validate_data(sales_data):
            print("Valid Data!")
            break
    return sales_data


def validate_data(values):
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"You should enter 6 different value, you provided {len(values)} different values"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.")
        return False
    return True

def update_sales_workheet(data):
    """
    Update Sales worksheet, add new row with the list data provided.
    """
    print("Updating sales worksheet...")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated succesfully.")

def calculate_surplus_data(sales_row):
    stock = SHEET.worksheet("stock").get_all_values()
    pprint(stock)

def main():
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_workheet(sales_data)
    calculate_surplus_data(sales_data)

main()