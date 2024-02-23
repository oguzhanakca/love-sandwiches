import gspread
from google.oauth2.service_account import Credentials

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
    print("Please enter sales data from the last market.\nData should be six number, seperated by commas.\nExample: 10,20,30,40,50,60")
    data_str = input("Enter your data here: ")
    validate_data(data_str)


def validate_data(values):
    try:
        if len(values) != 6:
            raise ValueError(
                f"You should enter 6 different value, you provided {len(values)} different values"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.")


get_sales_data()