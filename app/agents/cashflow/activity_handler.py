from microsoft.agents.builder import ActivityHandler, MessageFactory, TurnContext
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole

from app.agents.cashflow.agent import CashflowAgent


class CashflowAgentActivityHandler(ActivityHandler):
    def __init__(self):
        super().__init__()
        self.agent = CashflowAgent().initialize_agent()

    async def on_message_activity(self, turn_context: TurnContext):
        # Create a chat history thread for the agent
        thread = await self.agent.create_channel()
        message = turn_context.activity.text

        # Add the user message to the thread
        chat_message = ChatMessageContent(
            role=AuthorRole.USER,
            content=message,
        )
        thread.add_message(chat_message)

        # Invoke the agent with the thread
        responses = self.agent.invoke(messages=chat_message)
        first_response = await anext(responses, None)
        return await turn_context.send_activity(
            MessageFactory.text(f"Echo: {first_response if first_response else 'No response'}")
        )
