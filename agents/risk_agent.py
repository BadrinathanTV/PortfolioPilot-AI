# agents/risk_agent.py
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from core.llm_provider import llm
from tools.risk_tools import calculate_sector_exposure
from tools.market_tools import search_tool

@tool
def risk_agent_tool(query: str) -> str:
    """
    Use this agent for portfolio risk analysis, diversification, or sector exposure.
    It can search for real-time market conditions before its analysis.
    """

    system_prompt = """
    You are a sophisticated, data-driven risk analysis agent.
    Your goal is to provide a comprehensive risk analysis based on both the user's portfolio structure and real-time market data.

    You have two tools:
    1. `calculate_sector_exposure`: Use this to get the user's portfolio breakdown.
    2. `search_tool`: Use this to find recent news or market sentiment that might affect the risk of specific sectors.

    Your process should be:
    1. First, use `calculate_sector_exposure` to understand the portfolio's structure.
    2. Then, use the `search_tool` to look for any relevant news or risks associated with the top 2-3 sectors in the portfolio. For example, if the portfolio is heavy in IT, search for "risks in Indian IT sector".
    3. Finally, synthesize the information from both tools to provide a complete answer. State the sector exposure percentages and then add a brief comment on any market risks you found for those sectors.
    **NEVER answer from your own knowledge. Your entire analysis must be based on the data from your tools.**
    """

    agent_tools = [calculate_sector_exposure, search_tool]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    agent = create_tool_calling_agent(llm, agent_tools, prompt)
    executor = AgentExecutor(agent=agent, tools=agent_tools, verbose=True)
    result = executor.invoke({"input": query})
    return result['output']
