from abc import ABC, abstractmethod
from collections.abc import AsyncIterable
from semantic_kernel.agents.agent import AgentResponseItem
from semantic_kernel.contents.chat_message_content import ChatMessageContent


class CustomAgent(ABC):
    @staticmethod
    @abstractmethod
    def what_can_i_do() -> str:
        pass

    @property
    @abstractmethod
    def is_async_initialization(self) -> bool:
      """
      Abstract property to indicate if the agent requires async initialization.
      """
      pass

    async def initialize_agent(self):
      """
      Abstract method for initializing the agent. To be implemented by subclasses.
      """
      pass

    async def invoke(self, messages, thread, **kwargs) -> AsyncIterable[AgentResponseItem[ChatMessageContent]]:
        """
        Abstract method for invoking the agent. To be implemented by subclasses.
        """
        pass
