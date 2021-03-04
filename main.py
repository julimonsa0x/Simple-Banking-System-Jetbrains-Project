import random

card_list = []
pin_list = []
bank_status = True
valid_log = False


def exit_account():
    print("\nBye!")
    exit()

def main_menu():
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit\n")
    
def logging_menu():
    valid_card = False
    valid_pin = False
    while not valid_card and not valid_pin:
        print("Enter your card number:")
        card_input = input()
        if card_input not in card_list:
            print("Wrong card number or PIN!")
            break
        elif card_input in card_list:
            valid_card = True

        print("Enter your PIN:")
        pin_input = input()
        if pin_input not in pin_list:
            print("Wrong card number or PIN!")
            break
        elif pin_input in pin_list:
            valid_pin = True
        
        global valid_log
        valid_log = True
    if valid_card and valid_pin and valid_log:
        print("You have successfully logged in!\n")

def logged_in():
    while True:
        print("1. Balance")
        print("2. Log out")
        print("0. Exit\n")
        option = int(input())
        if option == 1:
            print("Balance: 0")
        elif option == 2:
            print("You have successfully logged out!")
            break
        elif option == 0:
            exit_account()

    
    
def card_creation():
    iin = str(400000)
    num = random.randrange(1, 10**9)
    account_number = str(num).zfill(9)
    checksum = str(random.randint(0, 9))
    card_number = str(int(iin + account_number + checksum))
    card_list.append(card_number)   
    pin = random.randrange(1, 10**4)
    pin_number = str(pin).zfill(4) 
    pin_list.append(pin_number)
    print(card_number)   
    print("Your card PIN:")
    print(pin_number)
    
    
def create_account():
    print("Your card has been created")
    print("Your card number:")
    card_creation()

while bank_status:
    main_menu()
    choice = int(input())
    if choice == 1:
        create_account()
    elif choice == 2:
        logging_menu()
        if valid_log:
            logged_in()
    elif choice == 0:
        exit_account()

