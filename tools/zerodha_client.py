# tools/zerodha_client.py
from kiteconnect import KiteConnect
import logging
from config.settings import settings
import getpass

def initialize_zerodha_client(request_token=None, generate_url_only=False):
    """
    Initializes the Zerodha Kite Connect client.
    Can be used to either generate a login URL or create a new session.
    """
    try:
        kite = KiteConnect(api_key=settings.ZERODHA_API_KEY)

        # --- FIX: Handle URL generation mode ---
        if generate_url_only:
            return kite.login_url()
        
        # --- Existing session generation logic ---
        if request_token:
            data = kite.generate_session(request_token, api_secret=settings.ZERODHA_API_SECRET)
            kite.set_access_token(data["access_token"])
            logging.info("✅ Zerodha connection successful!")
            return kite
        
        return None

    except Exception as e:
        logging.error(f"❌ Failed during Zerodha client initialization: {e}")
        return None

