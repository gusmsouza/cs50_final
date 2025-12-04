def main():
    print("Welcome to the Budget Tracker!")
    # Additional code for the budget tracker would go here
    selection = call_menu()

    if selection == 1:
        print("Adding new expense...")
    elif selection == 2:
        print("Checking budget...")
    else:
        print("Invalid option selected.")
            

def call_menu():
    print("***SELECT OPTION***")
    print("1. Add new expense")
    print("2. Check budget status")
    try:
        return int(input("Option: "))
    except ValueError:
        print("Invalid input. Please enter a number corresponding to the options.")
        return call_menu()

    
if __name__ == "__main__":
    main()