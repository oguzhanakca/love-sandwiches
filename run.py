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

def get_last_5_entries_sales():
    sales = SHEET.worksheet("sales")
    columns = []
    for i in range(1,7):
        column = sales.col_values(i)
        columns.append(column)


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


def update_worksheet(data,worksheet):
    """
    Update worksheet, add new row with the list data provided.
    """
    print(f"Updating {worksheet} worksheet...")
    sales_worksheet = SHEET.worksheet("surplus")
    sales_worksheet.append_row(data)
    print(f"Worksheet {worksheet} updated succesfully.")

def calculate_surplus_data(sales_row):
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    surplus_data = []
    for stock, sales in zip(stock_row,sales_row):
        surplus = int(stock)-int(sales)
        surplus_data.append(surplus)
    return surplus_data

def main():
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data,"sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data,"surplus")

main()