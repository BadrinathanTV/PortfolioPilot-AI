# core/graph_state.py

from typing import List, TypedDict, Annotated
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """
    Represents the state of our agent.

    Attributes:
        messages: A list of messages in the conversation. The `Annotated` part
                  ensures that new messages are appended to the list, maintaining
                  the conversation history.
    """
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]
