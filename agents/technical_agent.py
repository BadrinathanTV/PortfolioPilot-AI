# agents/technical_agent.py
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from core.llm_provider import llm
from tools.technical_tools import calculate_rsi
from tools.market_tools import search_tool

@tool
def technical_agent_tool(query: str) -> str:
    """
    Use this agent to get technical analysis for a specific stock, such as its RSI,
    and provide context by searching for related news.
    """

    system_prompt = """
    You are a sophisticated technical analysis agent.
    Your goal is to provide the RSI for a stock and add relevant context from recent news.

    You have two tools:
    1. `calculate_rsi`: Use this to get the numerical RSI value for a stock ticker.
    2. `search_tool`: Use this to find recent news that might explain the stock's recent price action and RSI value.

    Your process should be:
    1. First, use `calculate_rsi` to get the indicator value.
    2. Then, use `search_tool` to find the latest news for that same stock.
    3. Finally, present both pieces of information. State the RSI value and its meaning (e.g., overbought, oversold, neutral), and then provide a brief summary of the news that might be influencing the stock's momentum.
    **Your entire analysis must be based on the data from your tools.**
    """

    agent_tools = [calculate_rsi, search_tool]

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    agent = create_tool_calling_agent(llm, agent_tools, prompt)
    executor = AgentExecutor(agent=agent, tools=agent_tools, verbose=True)
    result = executor.invoke({"input": query})
    return result['output']