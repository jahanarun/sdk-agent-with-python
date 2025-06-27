#!/usr/bin/env python3
import json
import random
import datetime
import os
from pathlib import Path

# Define transaction categories appropriate for SMBs
TRANSACTION_CATEGORIES = {
    "Payments": ["Customer Payment", "Invoice Payment", "Service Fee", "Subscription Revenue", "Online Sales"],
    "Expenses": ["Inventory Purchase", "Supplier Payment", "Utility Bill", "Rent Payment", "Insurance Premium"],
    "Payroll": ["Staff Salary", "Contractor Payment", "Payroll Taxes", "Bonus Payment", "Commission Payout"],
    "Marketing": ["Ad Campaign", "Social Media Promotion", "Event Sponsorship", "Marketing Materials", "Promotional Discount"],
    "Operational": ["Equipment Purchase", "Maintenance Cost", "Software Subscription", "Office Supplies", "Professional Services"]
}

def get_random_date(start_date, end_date):
    """Generate a random date between start_date and end_date."""
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_days = random.randrange(days_between_dates)
    return start_date + datetime.timedelta(days=random_days)

def generate_transaction_amount(category, business_type):
    """Generate a realistic transaction amount based on category and business type."""
    base_amounts = {
        "Payments": {
            "Coffee Shop Chain": (500, 2500),
            "Software Development": (2000, 15000),
            "Grocery Store": (100, 1500),
            "Fitness Center": (50, 500),
            "Furniture Making": (1000, 8000)
        },
        "Expenses": {
            "Coffee Shop Chain": (200, 5000),
            "Software Development": (500, 8000),
            "Grocery Store": (1000, 20000),
            "Fitness Center": (300, 3000),
            "Furniture Making": (500, 10000)
        },
        "Payroll": {
            "Coffee Shop Chain": (1000, 5000),
            "Software Development": (5000, 15000),
            "Grocery Store": (800, 3000),
            "Fitness Center": (1500, 8000),
            "Furniture Making": (2000, 7000)
        },
        "Marketing": {
            "Coffee Shop Chain": (200, 1500),
            "Software Development": (1000, 5000),
            "Grocery Store": (100, 800),
            "Fitness Center": (300, 2500),
            "Furniture Making": (200, 1200)
        },
        "Operational": {
            "Coffee Shop Chain": (100, 2000),
            "Software Development": (200, 5000),
            "Grocery Store": (300, 3000),
            "Fitness Center": (500, 8000),
            "Furniture Making": (300, 5000)
        }
    }
    
    min_amount, max_amount = base_amounts.get(category, {}).get(business_type, (100, 1000))
    return round(random.uniform(min_amount, max_amount), 2)

def is_income(category):
    """Determine if a transaction is income (positive) or expense (negative)."""
    if category == "Payments":
        return True
    return False

def generate_transactions_for_customer(customer, num_transactions=25):
    """Generate transactions for a specific customer."""
    customer_id = customer["customerId"]
    business_name = customer["businessName"]
    business_type = customer["businessType"]
    
    # Set date range for transactions (last 90 days)
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=90)
    
    transactions = []
    
    for _ in range(num_transactions):
        # Select random category and subcategory
        category = random.choice(list(TRANSACTION_CATEGORIES.keys()))
        subcategory = random.choice(TRANSACTION_CATEGORIES[category])
        
        # Generate transaction amount
        amount = generate_transaction_amount(category, business_type)
        
        # Determine if it's income or expense
        if not is_income(category):
            amount = -amount
        
        # Generate random date
        transaction_date = get_random_date(start_date, end_date)
        
        # Create transaction object
        transaction = {
            "transactionId": f"TXN-{customer_id}-{random.randint(1000, 9999)}",
            "customerId": customer_id,
            "date": transaction_date.strftime("%Y-%m-%d"),
            "category": category,
            "subcategory": subcategory,
            "amount": amount,
            "balance": None,  # Will calculate after sorting
            "description": f"{subcategory} - {business_name}"
        }
        
        transactions.append(transaction)
    
    # Sort transactions by date
    transactions.sort(key=lambda x: x["date"])
    
    # Calculate running balance
    running_balance = customer["financialProfile"]["currentBalance"] - sum(t["amount"] for t in transactions)
    for transaction in transactions:
        running_balance += transaction["amount"]
        transaction["balance"] = round(running_balance, 2)
    
    return transactions

def main():
    # Get the absolute path to the customer portfolios file
    script_dir = Path(__file__).resolve().parent.parent
    customer_file = script_dir / "customer-portfolios.json"
    
    # Read customer data
    with open(customer_file, 'r') as file:
        data = json.load(file)
    
    all_transactions = []
    
    # Generate transactions for each customer
    for customer in data["customers"]:
        customer_transactions = generate_transactions_for_customer(customer, num_transactions=25)
        all_transactions.extend(customer_transactions)
    
    # Create transactions output file
    transactions_data = {"transactions": all_transactions}
    output_file = script_dir / "bank-transactions.json"
    
    with open(output_file, 'w') as file:
        json.dump(transactions_data, file, indent=2)
    
    print(f"Generated {len(all_transactions)} transactions for {len(data['customers'])} customers")
    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    main()