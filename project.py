from datetime import date
import csv
import sys

BUDGET_FILE = "budget.csv"
EXPENSES_FILE = "expenses.csv"
CARDS_FILE = "cards.csv"

GREENTEXT = "\033[32m"
ORANGETEXT = "\033[38;2;255;165;0m"

def main():
    print(f"{ORANGETEXT}Welcome to the Budget Tracker!\033[0m")
    budget = load_csv_file(BUDGET_FILE)
    expense_history = load_csv_file(EXPENSES_FILE)
    cards = [card["card"] for card in load_csv_file(CARDS_FILE)]
    categories = list(set(item["category"] for item in budget))
    while True:
        selection = call_menu() 
        if selection == 1:
            add_expense(expense_history, categories, cards)
        elif selection == 2:
            check_budget(categories, expense_history, budget)
        elif selection == 0:
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid option selected.")
            break
            

def load_csv_file(file_name):
    data = []
    try:
        with open(file_name, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        sys.exit(f"No file named {file_name} found. Please create/restore the file and restart program")
    return data


def call_menu():
    print(f"{GREENTEXT}____SELECT OPTION____\033[0m")
    print("   1. Add new expense")
    print("   2. Check budget status")
    print("   3. Check Trends (Coming Soon!)")
    print("   3. Check expense per category (Coming Soon!)")
    print("   0. Exit the Program\n")    
    try:
        return int(input("Option: "))
    except ValueError:
        print("Invalid input. Please enter a number corresponding to the options.")
        return call_menu()


def add_expense(history, categories, cards):
    while True:
        amount = input("Enter expense amount ($XX.YY) :$")
        category = get_from_list(categories)
        card = get_from_list(cards)
        ymd = input("Enter date (YYYY-MM-DD) or leave blank for today: ") # Allow -1 -2 etc for previows days
        if not ymd:
            ymd = str(date.today())
        description = input("Brief description of the expense: ")
        
        with open(EXPENSES_FILE, "a") as file:        
            file.write(f"{ymd},{category},{card},{amount},{description} \n")
        history.append({"date": ymd, "category": category, "amount": amount, "card": card, "description": description})
        print (f"Expense of ${amount} added successfully.")            
        
        more = input("Do you want to add a new expense? (y/n): ").strip().lower()
        if more != 'y' and more != 'yes':
            break


def get_from_list(items):
    i = 1
    print("Select from the list:")
    for item in items:
        print(f"{i}. {item}")
        i += 1
    index = int(input("Enter number: ")) - 1            
    return items[index]
    

def check_budget(categories, history, budget):
    budget_status = []   
    for category in categories:
        cat = {"category": category, "budgeted": 0, "spent": 0, "remaining": 0}
        for item in budget:
            if item["category"].lower() == category.lower():
                cat["budgeted"] = float(item["amount"])
        for expense in history:
            if expense["category"].lower() == category.lower():
                cat["spent"] += float(expense["amount"])
        cat["remaining"] = cat["budgeted"] - cat["spent"]
        budget_status.append(cat)
    
    print("\n\033[34m--- Budget Status per Category ---\033[0m")
    for status in budget_status:
        print(f"Category: {status['category'].capitalize()}")
        print(f"  Budgeted: ${status['budgeted']:.2f}")
        print(f"  Spent:    ${status['spent']:.2f}")
        print(f"  Remaining:${status['remaining']:.2f}\n")


if __name__ == "__main__":
    main()