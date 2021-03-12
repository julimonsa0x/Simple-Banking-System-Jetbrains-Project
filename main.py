import random
import sqlite3

card_list = []
pin_list = []
last_card_used = []
bank_status = True
valid_log = False
wrong_card = False
wrong_pin = False

# we first create and connect to card.db
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

# if card TABLE already exists, delete it and start again
cur.execute("DROP TABLE IF EXISTS card;")

cur.execute("""CREATE TABLE IF NOT EXISTS card 
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    number TEXT, 
    pin TEXT, 
    balance INTEGER DEFAULT 0);""")

# commit changes
conn.commit()


def sum_nums_of_str(text: str):
    final_sum = sum(int(digit) for digit in text)
    return final_sum  # type = int


def check_luhn(card: str) -> bool:
    """Checks Luhn Algorithm for a card number of class <string>"""
    checksum = int(card[15])  # to access card last digit easily
    test_card = []

    if len(card) == 16:
        # step 3
        start = 0
        for i in card[:15]:
            if start % 2 == 0:
                test_card.append(str(int(i) * 2))
            if start % 2 != 0:
                test_card.append(str(i))
            start += 1
        # step 4
        for idx, val in enumerate(test_card):
            if int(val) >= 10:
                test_card[int(idx)] = str(int(val) - 9)
        card_without_checksum = ''.join(test_card)
        final_num = sum_nums_of_str(card_without_checksum) + checksum
        if final_num % 10 == 0:
            return True
        elif final_num % 10 != 0:
            return False


def exit_account():
    print("\nBye!")
    exit()


def main_menu():
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit\n")

# 1
def show_balance():
    """Shows balance of current logged account. Used in 1st option of logged_in menu"""
    with conn:
        cur.execute("SELECT balance FROM card WHERE number=?", (last_card_used[-1],))
        balance = str(cur.fetchone()[0])
        print(f"Balance: {balance}")

# 2
def add_income():
    """Adds income of current logged account. Used in 2nd option of logged_in menu"""
    print("Enter income: ")
    income = input()
    with conn:
        cur.execute("UPDATE card SET BALANCE = (balance + ?) WHERE number=?;", (income, last_card_used[-1]))
    print("Income was added!\n")

# 3
def do_transfer():
    """Do proper transfer if possible from current logged account. Used in 3rd option of logged_in menu"""
    print("Transfer\nEnter card number:")
    receiver_account = input()
    with conn:
        cur.execute("SELECT balance FROM card WHERE number=?", (last_card_used[-1],))
        check_balance = int(cur.fetchone()[0])  # check if amount to send is available
        cur.execute("SELECT number FROM card WHERE number=?", (last_card_used[-1],))
        this_same_card = str(cur.fetchone()[0])  # check if receiver is sender
        cur.execute("SELECT EXISTS(SELECT number FROM card WHERE number=?)", (receiver_account,))  # if exists returns 1, else returns 0
        check_receiver = str(cur.fetchone()[0])  # check if receiver exist

    valid_transfer = False
    if not check_luhn(receiver_account):
        print("Probably you made a mistake in the card number. Please try again!\n")
        return
    elif check_luhn(receiver_account):
        valid_transfer: bool = True

    if this_same_card == receiver_account:
        print("You can't transfer money to the same account!\n")
        return
    elif this_same_card != receiver_account:
        valid_transfer: bool = True

    if check_receiver == "0SS":  # 1 means it's the exact card
        print("Such a card does not exist.")
        return
    elif check_receiver == "1":  # 0 means it's not the same card
        valid_transfer: bool = True

    if valid_transfer:
        print("Enter how much money you want to transfer:")
        sending_amount = input()
        if check_balance < int(sending_amount):
            print("Not enough money!")
        else:
            with conn:
                cur.execute("UPDATE card SET balance = (balance + ?) WHERE number=?", (sending_amount, receiver_account))
                cur.execute("UPDATE card SET balance = (balance - ?) WHERE number=?", (sending_amount, last_card_used[-1]))
            print("Success!")


# 4
def close_account():
    """Deletes current account from database"""
    with conn:
        cur.execute("DELETE FROM card WHERE number=?", (last_card_used[-1],))
    print("The account has been closed!")


def add_data(card: str, pin: str):
    """Adds card_number and pin_number to database."""
    with conn:
        cur.execute("INSERT INTO card(number, pin) VALUES(?,?);", (card, pin))


def check_card(card_to_check: str):
    with conn:
        cur.execute("SELECT number FROM card WHERE number=?", (card_to_check,))  # use when not in pycharm/hyperskill
        #cur.execute("SELECT number FROM card")
        # use only 2nd cur.ex... when editing in pycharm
        # apparently there is a bug that raises a TypeError...
        # and misschecks the card and pin login...
        retrieved_card = cur.fetchone()[0]
    if card_to_check in retrieved_card:
        return True
    else:
        return False


def check_pin(pin_to_check: str):
    with conn:
        cur.execute("SELECT pin FROM card WHERE pin=?", (pin_to_check,))  # use when no in pycharm/hyperskill
        #cur.execute("SELECT pin FROM card")
        # use only 2nd cur.ex... when editing in pycharm
        # apparently there is a bug that raises a TypeError...
        # and misschecks the card and pin login...
        retrieved_pin = cur.fetchone()[0]
    if pin_to_check in retrieved_pin:
        return True
    else:
        return False


def logging_menu():
    valid_card = False
    valid_pin = False
    while not valid_card and not valid_pin:
        print("Enter your card number:")
        card_input = input()
        print("Enter your PIN:")
        pin_input = input()
        if not check_card(card_input):
            print("Wrong card number or PIN!")
            break
        elif check_card(card_input):
            valid_card = True

        if not check_pin(pin_input):
            print("Wrong card number or PIN!")
            break
        elif check_pin(pin_input):
            valid_pin = True

        global valid_log
        valid_log = True

    if valid_card and valid_pin and valid_log:
        print("You have successfully logged in!\n")
        last_card_used.append(card_input)
    elif wrong_card or wrong_pin:
        print("Wrong card number or PIN!\n")


def logged_in():
    while True:
        print("\n1. Balance")
        print("2. Add Income")
        print("3. Do transfer")
        print("4. Close account")
        print("5. Log out")
        print("0. Exit")
        option = int(input())
        if option == 1:
            show_balance()
        elif option == 2:
            add_income()
        elif option == 3:
            do_transfer()
        elif option == 4:
            close_account()
            break
        elif option == 5:
            print("You have successfully logged out!")
            break
        elif option == 0:
            conn.close()
            exit_account()


def card_creation():
    card_validity = False
    while not card_validity:
        # pin creation
        pin = random.randrange(1, 10 ** 4)
        pin_number = str(pin).zfill(4)
        # card creation
        iin = str(400000)
        num = random.randrange(1, 10 ** 9)
        account_number = str(num).zfill(9)
        checksum = str(random.randint(0, 9))
        card_number = str(int(iin + account_number + checksum))
        # test card validity with Luhn Algorithm
        if check_luhn(card_number):
            add_data(card_number, pin_number)
            card_validity = True
        elif not check_luhn(card_number):
            pass

    if card_validity:
        print("Your card has been created")
        print("Your card number:")
        print(card_number)
        print("Your card PIN:")
        print(pin_number + "\n")


# run app
while bank_status:
    main_menu()
    choice = int(input())
    if choice == 1:
        card_creation()
    elif choice == 2:
        logging_menu()
        if valid_log:
            logged_in()
    elif choice == 0:
        conn.close()
        exit_account()
