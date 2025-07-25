# tools/technical_tools.py
from langchain_core.tools import tool
import yfinance as yf
import pandas as pd
import logging

def get_rsi(data: pd.DataFrame, window: int = 14) -> pd.Series:
    """Calculates the Relative Strength Index (RSI)."""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

@tool
def calculate_rsi(ticker: str) -> str:
    """
    Calculates the 14-day Relative Strength Index (RSI) for a given stock ticker.
    An RSI > 70 is overbought, < 30 is oversold.
    """
    print(f"🤖 [Tool Called] calculate_rsi() for ticker: {ticker}")
    
    # For Indian stocks on NSE, yfinance expects a ".NS" suffix.
    full_ticker = ticker.upper()
    if ".NS" not in full_ticker:
        full_ticker += ".NS"

    try:
        # Download historical data for the last year
        data = yf.download(full_ticker, period="1y", progress=False, auto_adjust=True)

        if data.empty:
            return f"Error: Could not retrieve data for ticker {ticker}. It might be an invalid symbol."

        # Calculate RSI
        data['RSI'] = get_rsi(data)
        
        # Get the most recent RSI value
        current_rsi = data['RSI'].iloc[-1]
        
        # Convert pandas object to a standard Python float before formatting
        current_rsi_float = current_rsi.item()

        return f"The current 14-day RSI for {ticker} is {current_rsi_float:.2f}"

    except Exception as e:
        logging.error(f"Error in RSI tool for {ticker}: {e}")
        return f"An error occurred while calculating RSI for {ticker}: {e}"
