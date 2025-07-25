# tools/risk_tools.py
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
import logging
import json

# Import the shared LLM instance
from core.llm_provider import llm 

# Import the INTERNAL LOGIC functions, not the tools, to avoid recursion.
from .zerodha_tools import _get_holdings_logic, _get_open_positions_logic


def get_full_portfolio():
    """Fetches both holdings and positions to get a complete portfolio view."""
    logging.info("   -> Fetching full portfolio (holdings + positions)...")
    all_stocks = []
    
    holdings_result = _get_holdings_logic()
    if isinstance(holdings_result, list):
        all_stocks.extend(holdings_result)

    positions_result = _get_open_positions_logic()
    if isinstance(positions_result, list):
        all_stocks.extend(positions_result)

    cleaned_portfolio = []
    for stock in all_stocks:
        symbol = stock.get('tradingsymbol')
        quantity = stock.get('quantity')
        # We only care about stocks with a positive quantity
        if symbol and quantity and quantity > 0:
            # Get the best available price for calculation
            price = stock.get('average_price') or stock.get('last_price', 0)
            if price > 0:
                cleaned_portfolio.append({
                    "symbol": symbol,
                    "quantity": quantity,
                    "value": quantity * price
                })
    return cleaned_portfolio


@tool
def calculate_sector_exposure() -> dict:
    """
    Calculates the portfolio's exposure to different market sectors by analyzing
    the user's complete portfolio using an LLM to determine the sector for each stock.
    """
    logging.info("🤖 [Tool Called] calculate_sector_exposure() using LLM-direct method.")
    full_portfolio = get_full_portfolio()

    if not full_portfolio:
        return {"message": "Your portfolio appears to be empty."}

    # --- NEW LLM-DIRECT LOGIC ---
    try:
        logging.info("   -> Asking LLM to analyze portfolio sectors...")
        
        # --- PROMPT FIX ---
        # The curly braces in the example JSON must be escaped with double braces {{}}
        # so that LangChain's prompt formatter ignores them.
        analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are a financial analyst expert. Your task is to analyze the user's stock portfolio and calculate the sector diversification.
            1. For each stock in the provided list, identify its primary business sector.
            2. Calculate the total value of stocks in each sector.
            3. Calculate the percentage of the total portfolio value that each sector represents.
            4. Respond with ONLY a valid JSON object. The keys should be the sector names and the values should be the percentage exposure (as a number, not a string).
            
            Example Input:
            [...omitted for brevity...]

            Example Output:
            {{"Oil & Gas": 50.0, "IT - Software": 30.0, "Private Sector Bank": 20.0}}
            """),
            ("user", "Please analyze this portfolio: {portfolio_list}")
        ])

        analysis_chain = analysis_prompt | llm
        
        # Format the portfolio list for the prompt
        portfolio_str = json.dumps(full_portfolio)
        
        response = analysis_chain.invoke({"portfolio_list": portfolio_str})
        
        # The LLM should return a JSON string, so we parse it
        sector_exposure = json.loads(response.content)
        
        logging.info(f"   -> LLM analysis successful: {sector_exposure}")
        return sector_exposure

    except Exception as e:
        logging.error(f"   -> An error occurred during LLM sector analysis: {e}")
        return {"error": "Failed to analyze portfolio sectors using the LLM."}

