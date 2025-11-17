import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import numpy as np


class StockAnalyzer:
    """Stock price analysis utility"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = "https://api.example.com"

    def get_stock_data(self, symbol: str, period: str = "1y") -> pd.DataFrame:
        """Fetch historical stock data"""
        # Simulated data - replace with real API
        dates = pd.date_range(end=datetime.now(), periods=365)
        data = {
            'Date': dates,
            'Close': np.random.uniform(100, 150, 365),
            'Volume': np.random.randint(1000000, 10000000, 365)
        }
        return pd.DataFrame(data)

    def calculate_moving_average(self, prices: List[float], window: int = 20) -> List[float]:
        """Calculate moving average"""
        return pd.Series(prices).rolling(window=window).mean().tolist()

    def calculate_rsi(self, prices: List[float], period: int = 14) -> List[float]:
        """Calculate Relative Strength Index"""
        deltas = np.diff(prices)
        gains = [d if d > 0 else 0 for d in deltas]
        losses = [-d if d < 0 else 0 for d in deltas]

        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])

        if avg_loss == 0:
            return [100] * len(prices)

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return [rsi] * len(prices)

    def predict_price(self, prices: List[float]) -> float:
        """Simple price prediction using linear regression"""
        x = np.arange(len(prices))
        z = np.polyfit(x, prices, 1)
        p = np.poly1d(z)
        return float(p(len(prices)))
