# core/graph_builder.py

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from core.graph_state import AgentState
# Import ALL AGENTS as tools for the supervisor
from agents.portfolio_agent import portfolio_agent_tool
from agents.market_agent import market_agent_tool
from agents.risk_agent import risk_agent_tool
from agents.technical_agent import technical_agent_tool 
from config.settings import settings

# Define the supervisor agent's prompt with all four agents
supervisor_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
        You are the supervisor. Your job is to analyze the user's request and delegate it to the correct specialist agent.
        You have four specialist agents available:
        1. Portfolio Agent: For questions about the user's personal stock holdings.
        2. Market Agent: For questions about general market news, stock prices, or financial data.
        3. Risk Agent: For questions about portfolio risk, diversification, or sector exposure.
        4. Technical Agent: For technical analysis of a specific stock, like its RSI.
        
        Based on the user's query, you must call the appropriate agent's tool. Do not try to answer the question yourself.
        """),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# The full list of tools for the supervisor
tools = [
    portfolio_agent_tool, 
    market_agent_tool, 
    risk_agent_tool, 
    technical_agent_tool
]

# Create the supervisor agent runnable
llm = ChatOpenAI(model="gpt-4o-mini", api_key=settings.OPENAI_API_KEY)
supervisor_agent_runnable = supervisor_prompt | llm.bind_tools(tools)

# Define the graph nodes
def agent_node(state: AgentState):
    result = supervisor_agent_runnable.invoke(state)
    return {"messages": [result]}

tool_node = ToolNode(tools)

def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    # Check if the message has tool calls and if they are not empty
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "continue"
    return "end"

# --- Build the Graph ---
graph = StateGraph(AgentState)
graph.add_node("supervisor", agent_node)
graph.add_node("tools", tool_node)
graph.set_entry_point("supervisor")
graph.add_conditional_edges(
    "supervisor",
    should_continue,
    {"continue": "tools", "end": END},
)
graph.add_edge("tools", "supervisor")
graph = graph.compile()

print("✅ Supervisor Graph compiled successfully with FULL CORE TEAM!")

