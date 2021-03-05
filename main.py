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

def sum_nums_of_str(str):
    final_sum = sum(int(digit) for digit in str)
    return final_sum  #type = int

def check_luhn(card: str):
    checksum = int(card[15])  # to access card last digit easily
    test_card = []

    if len(card) == 16:
        # step 3
        start = 0
        for i in card[:15]:
            if start % 2 == 0:
                test_card.append(str(int(i)*2))
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
            #validity_message = f"Tarjeta valida! --> {final_num}"
            return True
        elif final_num % 10 != 0:
            #validity_message = f"Tarjeta no valida :( {final_num}"
            return False

def card_creation():
    card_validity = False
    while card_validity == False:
        try:
            # pin creation
            pin = random.randrange(1, 10**4)
            pin_number = str(pin).zfill(4) 
            pin_list.append(pin_number)
            # card creation
            iin = str(400000)
            num = random.randrange(1, 10**9)
            account_number = str(num).zfill(9)
            checksum = str(random.randint(0, 9))
            card_number = str(int(iin + account_number + checksum))
            if check_luhn(card_number):
                card_list.append(card_number)   
                card_validity = True  
            elif not check_luhn(card_number):
                pass
        except:
            pass
    
    if card_validity:
        print("Your card has been created")
        print(card_number)   
        print("Your card PIN:")
        print(pin_number)

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
        exit_account()