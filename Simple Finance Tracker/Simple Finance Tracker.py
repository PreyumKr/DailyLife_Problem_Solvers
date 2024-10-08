import sqlite3
from datetime import datetime, timedelta
import openpyxl
from tabulate import tabulate
from colorama import Fore, Style, init
import os

# Initialize colorama for colored terminal text
init(autoreset=True)

# Database setup
DB_NAME = 'finance_tracker.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS records (
                        id INTEGER PRIMARY KEY,
                        type TEXT,
                        amount REAL,
                        description TEXT,
                        date TEXT
                      )''')
    conn.commit()
    conn.close()

# Add new expense or income

def add_record(record_type, amount, description):
    try:
        # Convert the amount to float to ensure it's a valid number
        amount = float(amount)
    except ValueError:
        print(Fore.RED + "Error: Amount must be a numeric value.")
        return

    # Proceed with adding the record if the amount is valid
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO records (type, amount, description, date) VALUES (?, ?, ?, ?)",
                   (record_type, amount, description, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    print(Fore.GREEN + "Record added successfully.")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO records (type, amount, description, date) VALUES (?, ?, ?, ?)",
                   (record_type, amount, description, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    print(Fore.GREEN + f"✅ Added {record_type} of {amount}: {description}")

# Edit an existing record
def edit_record(record_id, amount=None, description=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records WHERE id=?", (record_id,))
    record = cursor.fetchone()

    if record:
        new_amount = amount if amount is not None else record[2]
        new_description = description if description else record[3]
        cursor.execute("UPDATE records SET amount=?, description=? WHERE id=?",
                       (new_amount, new_description, record_id))
        conn.commit()
        print(Fore.YELLOW + f"✏️ Updated record {record_id}")
    else:
        print(Fore.RED + f"❌ Record with ID {record_id} not found.")
    
    conn.close()

# Delete a record
def delete_record(record_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM records WHERE id=?", (record_id,))
    conn.commit()
    conn.close()
    print(Fore.RED + f"🗑️ Deleted record {record_id}")

# View all records
def view_records(record_type=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    if record_type:
        cursor.execute("SELECT * FROM records WHERE type=?", (record_type,))
    else:
        cursor.execute("SELECT * FROM records")
        
    records = cursor.fetchall()
    conn.close()

    if records:
        headers = ["ID", "Type", "Amount", "Description", "Date"]
        print(Fore.CYAN + tabulate(records, headers, tablefmt="pretty"))
    else:
        print(Fore.YELLOW + "⚠️ No records found.")

# Generate summary report and export to Excel
def generate_summary(period='daily'):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    today = datetime.now()
    if period == 'daily':
        start_date = today.date()
    elif period == 'weekly':
        start_date = (today - timedelta(days=today.weekday())).date()
    elif period == 'monthly':
        start_date = today.replace(day=1).date()

    cursor.execute("SELECT * FROM records WHERE date(date) >= ?", (start_date,))
    records = cursor.fetchall()
    conn.close()

    if records:
        total_expenses = sum([rec[2] for rec in records if rec[1] == 'expense'])
        total_incomes = sum([rec[2] for rec in records if rec[1] == 'income'])
        net_balance = total_incomes - total_expenses

        print(Fore.CYAN + f"\nSummary for {period} period:")
        print(Fore.GREEN + f"Total Incomes: {total_incomes}")
        print(Fore.RED + f"Total Expenses: {total_expenses}")
        print(Fore.BLUE + f"Net Balance: {net_balance}")

        export_to_excel(records, period)

    else:
        print(Fore.YELLOW + "⚠️ No records found for the specified period.")

# Export report to Excel
def export_to_excel(records, period):
    file_name = f"finance_report_{period}.xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"{period.capitalize()} Report"

    # Add headers
    headers = ["ID", "Type", "Amount", "Description", "Date"]
    ws.append(headers)

    # Add data rows
    for record in records:
        ws.append(record)

    # Save to Excel file
    wb.save(file_name)
    print(Fore.GREEN + f"📊 Report saved as {file_name}")

# Main menu
def main_menu():
    init_db()
    while True:
        print(Fore.MAGENTA + "\n=== Simple Finance Tracker ===")
        print(Fore.CYAN + Style.BRIGHT + "1. " + Fore.YELLOW + "Add Expense")
        print(Fore.CYAN + Style.BRIGHT + "2. " + Fore.GREEN + "Add Income")
        print(Fore.CYAN + Style.BRIGHT + "3. " + Fore.LIGHTMAGENTA_EX + "Edit Expense/Income")
        print(Fore.CYAN + Style.BRIGHT + "4. " + Fore.RED + "Delete Expense/Income")
        print(Fore.CYAN + Style.BRIGHT + "5. " + Fore.BLUE + "View Expenses")
        print(Fore.CYAN + Style.BRIGHT + "6. " + Fore.GREEN + "View Incomes")
        print(Fore.CYAN + Style.BRIGHT + "7. " + Fore.LIGHTCYAN_EX + "Generate Summary Report")
        print(Fore.CYAN + Style.BRIGHT + "0. " + Fore.LIGHTRED_EX + "Exit")

        choice = input(Fore.CYAN + "Choose an option: ")

        if choice == '1':
            amount = float(input(Fore.CYAN + "Enter amount: "))
            description = input(Fore.CYAN + "Enter description: ")
            add_record('expense', amount, description)
        elif choice == '2':
            amount = float(input(Fore.CYAN + "Enter amount: "))
            description = input(Fore.CYAN + "Enter description: ")
            add_record('income', amount, description)
        elif choice == '3':
            record_id = int(input(Fore.CYAN + "Enter record ID to edit: "))
            amount = float(input(Fore.CYAN + "Enter new amount (leave blank to skip): ") or 0)
            description = input(Fore.CYAN + "Enter new description (leave blank to skip): ")
            edit_record(record_id, amount if amount != 0 else None, description or None)
        elif choice == '4':
            record_id = int(input(Fore.CYAN + "Enter record ID to delete: "))
            delete_record(record_id)
        elif choice == '5':
            view_records('expense')
        elif choice == '6':
            view_records('income')
        elif choice == '7':
            period = input(Fore.CYAN + "Enter period (daily, weekly, monthly): ").lower()
            generate_summary(period)
        elif choice == '0':
            print(Fore.GREEN + "Goodbye!")
            break
        else:
            print(Fore.RED + "❌ Invalid choice. Please try again.")

if __name__ == '__main__':
    main_menu()
