from semantic_kernel.functions import kernel_function

from app.agents.cashflow.services.cashflow_service import CashflowService

# import aiohttp
# async def fetch(session, url):
#   async with session.get(url) as response:
#     return await response.json()


  # @kernel_function(
  #     name="GetCost",
  #     description="Get the cost of the product",
  # )
  # async def get_cost(self):
  #   async with aiohttp.ClientSession() as session:
  #     url = "http://api.example.com/cost"
  #     response = await fetch(session, url)
  #     return response['cost']

class CashflowPlugin:
  def __init__(self, cashflow_service: CashflowService):
    self.cashflow_service = cashflow_service


  @kernel_function(
      name="Customer_Details_API",
      description="""This function returns the customer detail for the given customer ID.
      The customer detail includes the customer's business name, industry, business type, year established, and financial profile.
      The financial profile includes the current balance, outstanding loans, monthly revenue, monthly expenses, credit score, payment history.
      """,
  )
  async def get_customer_detail(self, customer_id: str):
    return self.cashflow_service.get_customer_detail(customer_id)

  @kernel_function(
      name="Customer_Transaction_API",
      description="""This function returns the customer transactions for the given customer ID.
      The customer detail includes the transaction id, date, category, subcategory, amount, balance and description.
      """,
  )
  async def get_customer_transactions(self, customer_id: str):
    return self.cashflow_service.get_customer_transactions(customer_id)
