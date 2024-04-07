user_account = {}
epay_money = {"Available": 10000000000}


def register():
    print("\nWelcome to E-Pay\n\nPay Cashless. Pay E-nywhere\n\n---Register a New Account---")
    while True:
        try:
            user_number = input("\nEnter your number (leave blank to go back): ")
            balance = 0
            credit_score = 400
            loan = 0
            if not user_number:
                main()
            if user_number in user_account:
                print("\nUsername Taken. Try Again.")
                continue
            else:
                while True:
                    try:
                        password = input("\nEnter your 4 digit pin:  ")
                        if not password:
                            main()
                        if len(password) < 4:
                            print("Your pin must be 4 characters.")
                            continue
                        elif len(password) > 4:
                            print("Your pin must be 4 characters.")
                        elif len(password) == 4:
                            username = input("\nEnter your Username: ")
                            user_account[user_number] = {"username": username, "password": password,
                                                         "balance": balance, "Credit Score": credit_score,
                                                         "loan": loan}
                            print("\nSigned Up Successfully\n")
                            main()
                        else:
                            print("\nInvalid input. Try Again.")
                            continue
                    except ValueError as e:
                        register()
        except ValueError as e:
            register()


def log_in():
    print("\n---Log In to your Account---")
    while True:
        try:
            user_number = input("\nEnter mobile number: ")
            if not user_number:
                main()
            password = input("\nEnter Password: ")
            if user_account.get(user_number) and user_account[user_number]['password'] == password:
                print("\nLogin Successful")
                usermenu(user_number)
            else:
                print("\nInvalid username or password. Try again")
                log_in()
        except ValueError as e:
            main()


def usermenu(user_number):
    while True:
        print(f"\nWelcome to your Dashboard {user_account[user_number]['username']}")
        print(f"\nCurrent Balance: {user_account[user_number]['balance']}")

        print("\nWhat would you like to do?")
        print("1. Send Money")
        print("2. Borrow Money")
        print("3. Cash In")
        print("4. Log out")
        choice = int(input("\nEnter your choice: "))

        if choice == 1:
            send_money(user_number)
        if choice == 2:
            loanmenu(user_number)
        if choice == 3:
            cashin(user_number)
        if choice == 4:
            main()
        else:
            print("Invalid Input. Try Again.")


def send_money(user_number):
    print("\n---Send Money---")
    while True:
        try:
            who_to_send = input("\nEnter the number of the user you want send money to: ")
            if not who_to_send:
                usermenu(user_number)
            if who_to_send not in user_account:
                print("\nUser does not exist. Try again.")
                send_money(user_number)
            else:
                amt_to_send = int(input(f"\nEnter the amount to send to {user_account[who_to_send]['username']}: "))
                if amt_to_send > user_account[user_number]['balance']:
                    choice = int(input("Not Enough Balance. Enter 1 to go to cash in and 2 to go back: "))
                    if choice == 1:
                        cashin(user_number)
                    if choice == 2:
                        usermenu(user_number)
                    else:
                        print("Invalid Input")
                else:
                    confirmation = input("Press 'y' to confirm transfer: ")
                    if confirmation == 'y':
                        user_account[user_number]['balance'] -= amt_to_send
                        user_account[who_to_send]['balance'] += amt_to_send
                        print("---Transfer Successful!!----")
                        go_back = input("Press 'x' to Send Money again or 'y' to go back to menu: ")
                        if go_back == 'x':
                            send_money(user_number)
                        if go_back == 'y':
                            usermenu(user_number)
                        else:
                            print("Invalid Input")
                    else:
                        print("Going back to User Menu.")
                        usermenu(user_number)
        except ValueError as e:
            usermenu(user_number)


def loanmenu(user_number):
    print("\n---Gcash Loan Menu---")
    while True:
        try:
            choice = int(input("\n1. Loan Money \n\n2. Pay Balance\n\nEnter Choice (leave blank to go back): "))

            if not choice:
                usermenu(user_number)
            if choice == 1:
                loan(user_number)
            if choice == 2:
                paybalance(user_number)
            else:
                print("Invalid Input")
        except ValueError as e:
            usermenu(user_number)


def loan(user_number):
    while True:
        try:
            print("\n---Loan Money---")

            max_loan_amt = user_account[user_number]['Credit Score'] * 100

            print(
                f"\nThe maximum amount you can loan based on your Credit Score of {user_account[user_number]["Credit Score"]} is {max_loan_amt}PHP.")

            loan_amt = int(input("\nEnter the amount you want to loan: "))

            if loan_amt <= max_loan_amt:
                gcash_money["Available"] -= loan_amt
                user_account[user_number]['loan'] += loan_amt
                user_account[user_number]['balance'] += loan_amt

                print(f"\nUpdated Balance: {user_account[user_number]['balance']}")

                print("\nLoan Successful\n\nReturning to Dashboard...")
                usermenu(user_number)
            else:
                choice = int(input(
                    "\nYour Credit Score is insufficient for that amount. \n\nPress 1 to continue or 2 to go back: "))

                if choice == 1:
                    loan(user_number)
                if choice == 2:
                    usermenu(user_number)
                else:
                    print("Invalid Input.")
                    usermenu(user_number)
        except ValueError as e:
            usermenu(user_number)


def paybalance(user_number):
    print("\n---Pay Balance---")
    while True:
        try:
            print(f"\nYour remaining loan balance is {user_account[user_number]['loan']}")

            if user_account[user_number]['balance'] < user_account[user_number]['loan']:
                print("\nInsufficient Funds. Mag grind ka pa gar")
            else:
                amt_to_pay = int(input("\nEnter the due amount: "))
                if amt_to_pay > user_account[user_number]['loan']:
                    print("\nSobra gar palong palo ka naman mag bayad.")
                    paybalance(user_number)
                else:
                    user_account[user_number]['loan'] -= amt_to_pay
                    user_account[user_number]['balance'] -= amt_to_pay
                    new_credit_score = amt_to_pay // 10
                    user_account[user_number]['Credit Score'] += new_credit_score

                    print("\nBalance paid successfully!!")
                    print(
                        f"\nEto ang bago mong Credit Score. {user_account[user_number]['Credit Score']}. Sheeesh mas malaki na maloloan mo")

                    usermenu(user_number)
        except ValueError as e:
            usermenu(user_number)


def cashin(user_number):
    print("\n---Cash In---")
    while True:
        try:
            amt_to_add = int(input("Enter amount to add to your account: "))
            if amt_to_add <= 1:
                print("\nCan't add that amount. Try again")
                cashin
            else:
                choice = input("\nPress y to continue: ")
                if choice == 'y' or 'Y':
                    user_account[user_number]['balance'] += amt_to_add
                    print(
                        f"\nSuccessfullly Added {amt_to_add} to your balance. \nUpdated Wallet: {user_account[user_number]['balance']}")
                    usermenu(user_number)
                else:
                    usermenu(user_number)
        except ValueError as e:
            usermenu(user_number)

def main():
    print("Welcome to E-Pay")
    print("\n1. Sign Up")
    print("2. Log In")
    choice = int(input("\nChoice: "))

    if choice == 1:
        register()
    if choice == 2:
        log_in()
    else:
        print("Invalid Choice. Please try again.")
        main()


main()


