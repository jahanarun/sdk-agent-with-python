import asyncio
from typing import AsyncIterable, override

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.chat_completion_client_base import (
    ChatCompletionClientBase,
)
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.agents.agent import AgentResponseItem, AgentThread
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)
from semantic_kernel.connectors.ai.function_choice_behavior import (
    FunctionChoiceBehavior,
)
from semantic_kernel.agents import ChatCompletionAgent

from app.agents.cashflow.services.cashflow_service import CashflowService
from app.models.custom_agent import CustomAgent


from .plugin import CashflowPlugin


class CashflowAgent(ChatCompletionAgent, CustomAgent):

    @staticmethod
    def what_can_i_do() -> str:
        return """
    I am a specialized Cashflow Agent designed to assist with queries related to income, expenses, transactions, financial trends, and overall business cash health.
    I provide clear, data-driven insights and actionable advice based on verified financial data.
    """

    @property
    def is_async_initialization(self) -> bool:
        return False

    def __init__(self):
        kernel = Kernel()
        kernel.add_service(AzureChatCompletion())
        kernel.add_plugin(CashflowPlugin(CashflowService()), "cashflow_plugin")

        # Invoke the superclass's __init__ method
        super().__init__(
            kernel=kernel,
            name="cashflow_agent",
            #  instructions="Responsible for giving advice on the cashflow by looking at the recent cashflow data"
            instructions="""
You are the Cashflow Agent in a multi-agent assistant for a small business banking platform.
You specialize in helping users with cashflow-related queries by analyzing verified financial data using authorized APIs and tools.
Start with a Friendly Greeting: Always begin your response by thanking or acknowledging the user for contacting the Cashflow Desk.

Your Core Responsibilities:
1. Think step-by-step before forming a response to ensure clarity and accuracy.
2. Understand the user's request: Determine if it’s about income, expenses, trends, anomalies, or overall financial health.
3. Retrieve and analyze data: Use available APIs/tools to extract relevant transaction and profile data.
4. Summarize findings based on the user’s intent: Highlight exactly what the user is looking for, Use clear, category-based summaries and relevant numeric insights.
5. Provide grounded advice (only if asked):
    Offer actionable, data-supported advice for managing or improving cashflow.
    Ensure all suggestions are appropriate for the user’s situation and derived from their data.

Communication Guidelines:
1. Be friendly, helpful, and easy to understand.
2. Avoid jargon; explain in plain language.
3. Emphasize key numbers, trends, and comparisons.
4. Ask clarifying questions if data is incomplete or the user’s request is unclear.

Guardrails:
1. Do not fabricate or guess answers — always rely solely on verified data from tools and APIs.
2. Do not engage with requests that are illegal, harmful, or clearly inappropriate for the user’s financial situation.
3. Do not answer questions outside your domain (e.g., loans, product eligibility, investments).
      Politely respond: “I'm focused on helping with cashflow insights ”

Example Responses:
1. User: “How’s my cashflow this quarter?”
   You: “Thanks for contacting the Cashflow Desk! Here's your cashflow summary: Net positive ₹28,700. Inflows rose by 12%, primarily from customer payments. Expenses remained steady, led by salaries and logistics.”
2. User: “Should I invest my surplus?”
   You: “Glad to see you’re in surplus! I focus on cashflow, so for investment decisions, our financial advisor assistant would be better suited to help.”
""",
        )
