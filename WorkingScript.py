import requests
from collections import defaultdict
import json
import numpy as np
import datetime
import csv


class Expense:
    def __init__(self, amount, date, category="", description="", currency="$"):
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description
        self.currency = currency

    def dict(self):
        return {
            'category': self.category,
            'amount': self.amount,
            'date': self.date,
            'description': self.description,
            'currency': self.currency
        }


expenses = []


def add_expense():
    amount = input("amount: ")
    category = input("category: ")
    date = input("date: ")
    description = input("description: ")
    currency = input("currency: ")
    expense = Expense(amount, date, category, description, currency)
    expenses = expense


def view_expenses():
    for exp in expenses:
        print(exp.dict())


def save_expenses_csv(filename):
    with open(filename, "w", newline='') as f:
        writer = csv.DictWriter(
            f, fieldnames=Expense.__init__.__code__.co_varnames[1:])
        writer.writeheader()
        for exp in expenses:
            writer.writerow(exp.dict())


def load_expenses_csv(filename):
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            expenses.append(Expense(**row))


def save_expenses_json(filename):
    with open(filename, "w") as f:
        json.dump([exp.dict() for exp in expenses], f, indent=2)


def load_expenses_json(filename):
    with open(filename) as f:
        for data in json.load(f):
            expenses.append(Expense(**data))


def analyze_expenses():
    total = sum(exp.amount for exp in expenses)
    by_category = defaultdict(float)
    for exp in expenses:
        by_category[exp.category] += exp.amount
    print(f"Total spent: {total}")
    for cat, amt in by_category.items():
        print(f"{cat}: {amt}")
    # Add more analysis as desired

# For numerical analysis:


def average_by_category():
    categories = defaultdict(list)
    for exp in expenses:
        categories[exp.category].append(exp.amount)
    for cat, amts in categories.items():
        print(f"{cat} average: {np.mean(amts):.2f}")


def fetch_exchange_rate(from_currency, to_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(url)
    rates = response.json().get("rates", {})
    return rates.get(to_currency, None)


while True:
    print("1. Add Expense\n2. View Expenses\n3. Save to CSV\n4. Load from CSV\n5. Analyze\n6. Exit")
    choice = input("Select: ")
    if choice == "1":
        add_expense()
        pass
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        save_expenses_csv('expenses.csv')
    elif choice == "4":
        load_expenses_csv('expenses.csv')
    elif choice == "5":
        analyze_expenses()
    elif choice == "6":
        break
    else:
        print("Invalid option.")
