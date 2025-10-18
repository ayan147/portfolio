import csv
import os
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class Transaction:
    """Represents a single income or expense entry."""
    def __init__(self, date, category, amount, description, t_type):
        self.date = date
        self.category = category
        self.amount = float(amount)
        self.description = description
        self.type = t_type  # 'income' or 'expense'

    def to_dict(self):
        return {
            "date": self.date,
            "category": self.category,
            "amount": self.amount,
            "description": self.description,
            "type": self.type
        }


class BudgetManager:
    """Handles all budget operations including saving, loading, analytics, and reporting."""
    def __init__(self, data_file="budget_data.csv"):
        self.data_file = data_file
        self.transactions = []
        self.load_data()

    def load_data(self):
        """Loads transactions from the CSV file if it exists."""
        if not os.path.exists(self.data_file):
            return
        with open(self.data_file, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                t = Transaction(
                    date=row["date"],
                    category=row["category"],
                    amount=row["amount"],
                    description=row["description"],
                    t_type=row["type"]
                )
                self.transactions.append(t)

    def save_data(self):
        """Saves all transactions to the CSV file."""
        with open(self.data_file, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ["date", "category", "amount", "description", "type"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for t in self.transactions:
                writer.writerow(t.to_dict())

    def add_transaction(self, category, amount, description, t_type):
        """Adds a new transaction."""
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_transaction = Transaction(date, category, amount, description, t_type)
        self.transactions.append(new_transaction)
        self.save_data()

    def summarize(self):
        """Prints a basic financial summary and spending evaluation."""
        total_income = sum(t.amount for t in self.transactions if t.type == "income")
        total_expense = sum(t.amount for t in self.transactions if t.type == "expense")
        balance = total_income - total_expense

        print("\n--- Financial Summary ---")
        print(f"Total Income:  £{total_income:.2f}")
        print(f"Total Expenses: £{total_expense:.2f}")
        print(f"Current Balance: £{balance:.2f}")

        # Evaluate spending level
        self.evaluate_spending(total_income, total_expense)
        return balance

    def evaluate_spending(self, income, expenses):
        """Evaluates user's spending level based on expense/income ratio."""
        if income == 0:
            print("Cannot evaluate spending level — no income data found.")
            return

        ratio = expenses / income
        print("\n--- Spending Evaluation ---")

        if ratio <= 0.5:
            level = "Excellent"
            advice = "You're saving effectively. Keep up your disciplined budgeting!"
        elif ratio <= 0.8:
            level = "Moderate"
            advice = "Your spending is balanced, but watch for unnecessary expenses."
        else:
            level = "Overspending"
            advice = "You're spending more than 80% of your income. Review your expenses."

        print(f"Spending Level: {level}")
        print(f"Expense Ratio: {ratio:.2f}")
        print(f"Advice: {advice}")

        trend = self.detect_spending_trend()
        if trend:
            print(f"Trend Warning: {trend}")

    def detect_spending_trend(self):
        """Detects whether expenses are increasing significantly over time."""
        expenses = [t.amount for t in self.transactions if t.type == "expense"]
        if len(expenses) < 6:
            return None  # Not enough data for trend detection

        third = len(expenses) // 3
        early_avg = sum(expenses[:third]) / third
        late_avg = sum(expenses[-third:]) / third

        if late_avg > early_avg * 1.25:
            return "Your expenses have increased by more than 25% recently."
        return None

    def show_expense_breakdown(self):
        """Displays a category-wise expense breakdown."""
        expenses = defaultdict(float)
        for t in self.transactions:
            if t.type == "expense":
                expenses[t.category] += t.amount

        if not expenses:
            print("No expenses recorded yet.")
            return

        print("\n--- Expense Breakdown by Category ---")
        for category, amount in expenses.items():
            print(f"{category}: £{amount:.2f}")

        plt.figure(figsize=(7, 5))
        plt.pie(expenses.values(), labels=expenses.keys(), autopct='%1.1f%%', startangle=140)
        plt.title("Expense Distribution by Category")
        plt.tight_layout()
        plt.show()

    def clear_all_data(self):
        """Deletes all stored transactions and clears the CSV file."""
        confirm = input("Are you sure you want to delete all data? (yes/no): ").strip().lower()
        if confirm == "yes":
            self.transactions = []
            if os.path.exists(self.data_file):
                with open(self.data_file, "w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(["date", "category", "amount", "description", "type"])
            print("All data has been cleared.")
        else:
            print("Data deletion cancelled.")

    def display_data_table(self):
        """Displays all data using pandas and numpy for analysis."""
        if not self.transactions:
            print("No data available to display.")
            return

        data = [t.to_dict() for t in self.transactions]
        df = pd.DataFrame(data)

        print("\n--- All Transactions ---")
        print(df.to_string(index=False))

        # Numpy statistics
        amounts = np.array(df["amount"], dtype=float)
        print("\n--- Quick Stats ---")
        print(f"Total Entries: {len(amounts)}")
        print(f"Average Amount: £{np.mean(amounts):.2f}")
        print(f"Maximum Transaction: £{np.max(amounts):.2f}")
        print(f"Minimum Transaction: £{np.min(amounts):.2f}")

        income_df = df[df["type"] == "income"]
        expense_df = df[df["type"] == "expense"]

        if not expense_df.empty:
            print("\nTop Expense Categories:")
            print(expense_df.groupby("category")["amount"].sum().sort_values(ascending=False).head(5))


def main():
    print("Welcome to Syed Ayan's Smart Budget Manager")
    manager = BudgetManager()

    while True:
        print("\n1. Add Income")
        print("2. Add Expense")
        print("3. View Summary")
        print("4. Show Expense Breakdown")
        print("5. Clear All Data")
        print("6. Display Data Table (Pandas/Numpy)")
        print("7. Exit")

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            category = input("Enter income source: ")
            amount = input("Enter amount (£): ")
            description = input("Enter description: ")
            manager.add_transaction(category, amount, description, "income")
            print("Income added successfully.")

        elif choice == "2":
            category = input("Enter expense category: ")
            amount = input("Enter amount (£): ")
            description = input("Enter description: ")
            manager.add_transaction(category, amount, description, "expense")
            print("Expense added successfully.")

        elif choice == "3":
            manager.summarize()

        elif choice == "4":
            manager.show_expense_breakdown()

        elif choice == "5":
            manager.clear_all_data()

        elif choice == "6":
            manager.display_data_table()

        elif choice == "7":
            print("Goodbye! Data saved.")
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
