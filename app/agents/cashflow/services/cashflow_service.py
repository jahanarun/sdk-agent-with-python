
import json
from pathlib import Path


class CashflowService:

  root_dir = Path(__file__).resolve().parent.parent
  data_dir = root_dir / "data"

  def get_customer_detail(self, customer_id):
    customer_file = self.data_dir / "customer-portfolios.json"

    # Read customer data
    with open(customer_file, 'r') as file:
      data = json.load(file)
    
    customers = data["customers"]
    customer = next((c for c in customers if c["customerId"] == customer_id), None)

    if customer:
      return customer
    else:
      return None


  def get_customer_transactions(self, customer_id):
    customer_file = self.data_dir / "bank-transactions.json"

    # Read customer data
    with open(customer_file, 'r') as file:
      data = json.load(file)
    
    all_transactions = data["transactions"]
    customer_transactions = [item for item in all_transactions if item['customerId'] == customer_id]

    return customer_transactions
