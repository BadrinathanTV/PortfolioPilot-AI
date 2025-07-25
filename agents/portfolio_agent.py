# agents/portfolio_agent.py
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from core.llm_provider import llm
# --- THE CHANGE ---
# Import both tools
from tools.zerodha_tools import get_holdings, get_open_positions

@tool
def portfolio_agent_tool(query: str) -> str:
    """
    Use this agent for questions about personal stock portfolio, holdings, P&L,
    or open positions for the current day.
    """
    # --- THE CHANGE ---
    # Update the prompt to make the agent aware of the two different tools
    system_prompt = """
    You are a data-driven portfolio analysis agent. Your job is to use your tools to
    answer questions about the user's portfolio. You have two tools:

    1. `get_holdings`: Use this for questions about long-term, settled stocks.
    2. `get_open_positions`: Use this for questions about trades made today or intraday positions.

    - If the user asks a general question like "show me my stocks" or "what do I own?", you should use **both tools** to provide a complete picture.
    - If the user asks a specific question about "holdings", use `get_holdings`.
    - If the user asks a specific question about "positions", use `get_open_positions`.
    
    NEVER answer from your own knowledge. Base your entire response on the data from your tools.
    """
    # --- THE CHANGE ---
    # Give the agent access to both tools
    agent_tools = [get_holdings, get_open_positions]

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    agent = create_tool_calling_agent(llm, agent_tools, prompt)
    executor = AgentExecutor(agent=agent, tools=agent_tools, verbose=True)
    result = executor.invoke({"input": query})
    return result['output']
