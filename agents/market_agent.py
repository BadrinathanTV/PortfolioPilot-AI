from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from tools.market_tools import search_tool
from config.settings import settings
from core.llm_provider import llm

@tool
def market_agent_tool(query: str) -> str:
    """
    Use this agent for questions about general market news, live stock prices, or any external financial data.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a specialized market research agent. You must use your search tool to find the most relevant, up-to-date information. Summarize your findings in 3-4 clear bullet points."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    tools = [search_tool]
    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    result = executor.invoke({"input": query})
    return result['output']