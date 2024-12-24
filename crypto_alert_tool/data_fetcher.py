import ccxt
import pandas as pd
import json
from typing import Dict, Any
import logging

def fetch_data() -> pd.DataFrame:
    """
    Fetches cryptocurrency OHLCV (Open, High, Low, Close, Volume) data from Binance exchange.
    
    The function reads configuration from a JSON file containing API credentials and trading parameters,
    connects to Binance using ccxt library, and retrieves historical price data.
    
    Returns:
        pd.DataFrame: A pandas DataFrame containing OHLCV data with timestamp as index and columns:
            - open: Opening price for the period
            - high: Highest price for the period
            - low: Lowest price for the period
            - close: Closing price for the period
            - volume: Trading volume for the period
            
    Raises:
        FileNotFoundError: If the config.json file is not found
        json.JSONDecodeError: If the config file contains invalid JSON
        ccxt.NetworkError: If there are connection issues with the exchange
    """
    
    try:
        with open("crypto_alert_tool/config.json", "r") as f:
            config: Dict[str, Any] = json.load(f)
    except FileNotFoundError:
        logging.error("Config file config.json not found")
        raise
    except json.JSONDecodeError:
        logging.error("Config file contains invalid JSON")
        raise

    try:
        exchange: ccxt.binance = ccxt.binance({
            "apiKey": config["api_key"],
            "secret": config["secret_key"],
            'enableRateLimit': True,
            'options': {
                'adjustForTimeDifference': True
            }
        })
        
        exchange.load_time_difference()

        ohlcv: list = exchange.fetch_ohlcv(config["symbol"],
                                         timeframe=config["timeframe"], 
                                         limit=config["limit"])
    except ccxt.NetworkError:
        logging.error("Network error while connecting to exchange")
        raise
    except ccxt.ExchangeError as e:
        logging.error(f"Exchange error: {str(e)}")
        raise
    except KeyError as e:
        logging.error(f"Missing key {str(e)} in config file")
        raise

    try:
        df: pd.DataFrame = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)
        return df
    except Exception as e:
        logging.error(f"Error processing data: {str(e)}")
        raise
