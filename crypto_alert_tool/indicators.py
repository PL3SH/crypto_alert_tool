import pandas as pd
import ta
from typing import Union, Optional

def calculate_indicators(
    df: pd.DataFrame,
    fast_ema_period: int,
    slow_ema_period: int,
    rsi_period: int
) -> pd.DataFrame:
    """
    Calculates technical indicators for a market data DataFrame.

    Args:
        df (pd.DataFrame): Market data DataFrame that must include a 'close' column
        fast_ema_period (int): Period for the fast EMA calculation
        slow_ema_period (int): Period for the slow EMA calculation
        rsi_period (int): Period for the RSI indicator calculation

    Returns:
        pd.DataFrame: Original DataFrame with three new columns:
            - Fast_EMA: Fast Exponential Moving Average
            - Slow_EMA: Slow Exponential Moving Average
            - RSI: Relative Strength Index

    Raises:
        ValueError: If 'close' column is missing from DataFrame
        ValueError: If any period parameter is less than 1
        TypeError: If df is not a pandas DataFrame
    """
    # Validate input types
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")

    # Validate required columns
    if 'close' not in df.columns:
        raise ValueError("DataFrame must contain a 'close' column")

    # Validate period parameters
    if any(period < 1 for period in [fast_ema_period, slow_ema_period, rsi_period]):
        raise ValueError("All period parameters must be greater than 0")

    try:
        df['Fast_EMA'] = ta.trend.ema_indicator(df['close'], window=fast_ema_period)
        df['Slow_EMA'] = ta.trend.ema_indicator(df['close'], window=slow_ema_period)
        df['RSI'] = ta.momentum.rsi(df['close'], window=rsi_period)
        return df
    except Exception as e:
        raise RuntimeError(f"Error calculating indicators: {str(e)}")
