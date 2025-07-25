# tools/zerodha_tools.py
from langchain_core.tools import tool
import logging

# This global client will be set by main.py at startup
zerodha_client = None

def set_client(client):
    """Allows the main application to set the initialized Zerodha client."""
    global zerodha_client
    zerodha_client = client
    logging.info("Zerodha client has been set in tools module.")

def _get_holdings_logic():
    """The actual logic to fetch settled holdings."""
    if not zerodha_client:
        return {"error": "Zerodha client is not initialized."}
    try:
        holdings = zerodha_client.holdings()
        # Ensure consistent return type
        return holdings if holdings else []
    except Exception as e:
        logging.error(f"Error fetching holdings: {e}")
        return {"error": f"An error occurred while fetching holdings: {e}"}

def _get_open_positions_logic():
    """The actual logic to fetch open positions."""
    if not zerodha_client:
        return {"error": "Zerodha client is not initialized."}
    try:
        positions_data = zerodha_client.positions()
        net_positions = positions_data.get('net', [])
        # Ensure consistent return type
        return net_positions if net_positions else []
    except Exception as e:
        logging.error(f"Error fetching positions: {e}")
        return {"error": f"An error occurred while fetching positions: {e}"}

# --- TOOL DEFINITIONS ---
# These are the functions the agents will call. They are just thin wrappers.
@tool
def get_holdings() -> list:
    """
    Fetches the user's long-term stock holdings (stocks held for more than one day) 
    that are settled in their Demat account.
    """
    logging.info("🤖 [Tool Called] get_holdings()")
    return _get_holdings_logic()

@tool
def get_open_positions() -> list:
    """
    Fetches the user's open positions for the current trading day.
    This includes intraday trades and stocks bought today that have not yet settled.
    """
    logging.info("🤖 [Tool Called] get_open_positions()")
    return _get_open_positions_logic()