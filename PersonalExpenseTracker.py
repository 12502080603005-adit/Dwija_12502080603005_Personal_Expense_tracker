import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import date

# File to store expense records
FILE_NAME = "expenses.json"

# List to store dictionaries
expenses = []


# Load expenses from file
def load_expenses():
    global expenses

    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                expenses = json.load(file)
        except (json.JSONDecodeError, OSError):
            expenses = []
    else:
        expenses = []


# Save expenses to file
def save_expenses():
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(expenses, file, indent=4)
    except OSError:
        messagebox.showerror("Error", "Unable to save expenses.")


# Display expenses in the table
def display_expenses():
    for item in expense_table.get_children():
        expense_table.delete(item)

    for index, expense in enumerate(expenses):
        expense_table.insert(
            "",
            tk.END,
            iid=str(index),
            values=(
                expense["name"],
                expense["amount"],
                expense["category"],
                expense["date"]
            )
        )

    total = sum(expense["amount"] for expense in expenses)
    total_label.config(text=f"Total Expenses: Rs. {total:.2f}")


# Add a new expense
def add_expense():
    name = name_entry.get().strip()
    amount_text = amount_entry.get().strip()
    category = category_box.get().strip()
    expense_date = date_entry.get().strip()

    if not name or not amount_text or not category or not expense_date:
        messagebox.showwarning(
            "Input Error",
            "Please fill in all fields."
        )
        return

    try:
        amount = float(amount_text)

        if amount <= 0:
            messagebox.showwarning(
                "Input Error",
                "Amount must be greater than zero."
            )
            return

        date.fromisoformat(expense_date)

    except ValueError:
        messagebox.showwarning(
            "Input Error",
            "Enter a valid amount and date (YYYY-MM-DD)."
        )
        return

    # Dictionary stores one expense
    expense = {
        "name": name,
        "amount": amount,
        "category": category,
        "date": expense_date
    }

    # List stores multiple expenses
    expenses.append(expense)

    save_expenses()
    display_expenses()

    name_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    category_box.set("")
    date_entry.delete(0, tk.END)
    date_entry.insert(0, str(date.today()))

    messagebox.showinfo(
        "Success",
        "Expense added successfully!"
    )


# Delete the selected expense
def delete_expense():
    selected = expense_table.selection()

    if not selected:
        messagebox.showwarning(
            "Selection Error",
            "Please select an expense to delete."
        )
        return

    index = int(selected[0])

    del expenses[index]

    save_expenses()
    display_expenses()

    messagebox.showinfo(
        "Success",
        "Expense deleted successfully!"
    )


# Main application window
root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("800x550")
root.resizable(False, False)

# Heading
heading = tk.Label(
    root,
    text="PERSONAL EXPENSE TRACKER",
    font=("Arial", 20, "bold")
)
heading.pack(pady=15)

# Input frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Expense name
tk.Label(input_frame, text="Expense Name:").grid(
    row=0, column=0, padx=5, pady=5, sticky="w"
)
name_entry = tk.Entry(input_frame, width=20)
name_entry.grid(row=0, column=1, padx=5, pady=5)

# Amount
tk.Label(input_frame, text="Amount (Rs.):").grid(
    row=0, column=2, padx=5, pady=5, sticky="w"
)
amount_entry = tk.Entry(input_frame, width=20)
amount_entry.grid(row=0, column=3, padx=5, pady=5)

# Category
tk.Label(input_frame, text="Category:").grid(
    row=1, column=0, padx=5, pady=5, sticky="w"
)
category_box = ttk.Combobox(
    input_frame,
    values=[
        "Food",
        "Travel",
        "Shopping",
        "Education",
        "Bills",
        "Other"
    ],
    width=17,
    state="readonly"
)
category_box.grid(row=1, column=1, padx=5, pady=5)

# Date
tk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(
    row=1, column=2, padx=5, pady=5, sticky="w"
)
date_entry = tk.Entry(input_frame, width=20)
date_entry.grid(row=1, column=3, padx=5, pady=5)
date_entry.insert(0, str(date.today()))

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="Add Expense",
    width=15,
    command=add_expense
).grid(row=0, column=0, padx=10)

tk.Button(
    button_frame,
    text="Delete Expense",
    width=15,
    command=delete_expense
).grid(row=0, column=1, padx=10)

# Expense table
columns = ("Name", "Amount", "Category", "Date")

expense_table = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=12
)

for column in columns:
    expense_table.heading(column, text=column)
    expense_table.column(column, width=170, anchor="center")

expense_table.pack(padx=20, pady=10)

# Total expenses
total_label = tk.Label(
    root,
    text="Total Expenses: Rs. 0.00",
    font=("Arial", 14, "bold")
)
total_label.pack(pady=10)

# Load saved records and display them
load_expenses()
display_expenses()

# Run application
root.mainloop()
