import yfinance as yf
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd
from functools import lru_cache
import time

class YFinanceAPI:
    """Handler for Yahoo Finance API integration using yfinance"""
    
    def __init__(self):
        """Initialize the API client with empty cache"""
        self._cache = {}
        self._cache_timeout = 300  # 5 minutes cache
        
    def _is_cache_valid(self, key: str) -> bool:
        """Check if cached data is still valid"""
        if key not in self._cache:
            return False
        return time.time() - self._cache[key]['timestamp'] < self._cache_timeout
    
    def _get_from_cache(self, key: str):
        """Get data from cache if valid"""
        if self._is_cache_valid(key):
            return self._cache[key]['data']
        return None
    
    def _set_cache(self, key: str, data):
        """Set data in cache"""
        self._cache[key] = {
            'data': data,
            'timestamp': time.time()
        }
        
    def get_latest_price(self, symbol: str) -> Optional[Dict]:
        """Get latest price for a stock symbol"""
        cache_key = f"latest_{symbol.upper()}"
        cached_data = self._get_from_cache(cache_key)
        if cached_data:
            return cached_data
            
        try:
            ticker = yf.Ticker(symbol.upper())
            hist = ticker.history(period="2d")
            
            if hist.empty:
                logging.error(f"No data found for symbol: {symbol}")
                return None
                
            # Get the most recent data
            latest = hist.iloc[-1]
            previous = hist.iloc[-2] if len(hist) > 1 else latest
            
            # Get additional info with minimal data to speed up
            try:
                info = ticker.info
                exchange = info.get('exchange', 'NASDAQ')
            except:
                exchange = 'NASDAQ'  # Fallback if info fails
            
            result = {
                'symbol': symbol.upper(),
                'open': float(latest['Open']),
                'high': float(latest['High']),
                'low': float(latest['Low']),
                'close': float(latest['Close']),
                'volume': int(latest['Volume']),
                'date': latest.name.strftime('%Y-%m-%d'),
                'exchange': exchange,
                'previous_close': float(previous['Close'])
            }
            
            self._set_cache(cache_key, result)
            return result
            
        except Exception as e:
            logging.error(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def get_historical_data(self, symbol: str, date_from: Optional[str] = None, 
                           date_to: Optional[str] = None, limit: int = 30) -> Optional[List[Dict]]:
        """Get historical stock data"""
        try:
            ticker = yf.Ticker(symbol.upper())
            
            if date_from and date_to:
                hist = ticker.history(start=date_from, end=date_to)
            else:
                # Add extra days to account for weekends/holidays
                end_date = datetime.now()
                start_date = end_date - timedelta(days=limit * 2)  # Request more days to ensure we get enough trading days
                hist = ticker.history(start=start_date, end=end_date)
            
            if hist.empty:
                logging.error(f"No historical data found for symbol: {symbol}")
                return None
            
            # Convert to list of dictionaries
            historical_data = []
            for date, row in hist.iterrows():
                historical_data.append({
                    'symbol': symbol.upper(),
                    'date': date.strftime('%Y-%m-%d'),
                    'open': float(row['Open']),
                    'high': float(row['High']),
                    'low': float(row['Low']),
                    'close': float(row['Close']),
                    'volume': int(row['Volume'])
                })
            
            # Sort by date descending (most recent first)
            historical_data.sort(key=lambda x: x['date'], reverse=True)
            
            # Return exactly the number of days requested
            return historical_data[:limit]
            
        except Exception as e:
            logging.error(f"Error fetching historical data for {symbol}: {str(e)}")
            return None
    
    def get_multiple_symbols(self, symbols: List[str]) -> Optional[List[Dict]]:
        """Get latest data for multiple symbols - optimized batch processing"""
        if not symbols:
            return None
        
        cache_key = f"multiple_{','.join(sorted(symbols))}"
        cached_data = self._get_from_cache(cache_key)
        if cached_data:
            return cached_data
            
        try:
            # Use yfinance's batch download feature for better performance
            symbols_str = ' '.join([s.upper() for s in symbols])
            data = yf.download(symbols_str, period="2d", group_by="ticker", progress=False)
            
            if data.empty:
                return None
            
            stock_data = []
            
            for symbol in symbols:
                symbol = symbol.upper()
                try:
                    if len(symbols) == 1:
                        # Single symbol case
                        symbol_data = data
                    else:
                        # Multiple symbols case
                        symbol_data = data[symbol]
                    
                    if symbol_data.empty:
                        continue
                        
                    latest = symbol_data.iloc[-1]
                    previous = symbol_data.iloc[-2] if len(symbol_data) > 1 else latest
                    
                    stock_data.append({
                        'symbol': symbol,
                        'open': float(latest['Open']),
                        'high': float(latest['High']),
                        'low': float(latest['Low']),
                        'close': float(latest['Close']),
                        'volume': int(latest['Volume']),
                        'date': latest.name.strftime('%Y-%m-%d'),
                        'exchange': 'NASDAQ',  # Simplified for performance
                        'previous_close': float(previous['Close'])
                    })
                    
                except Exception as e:
                    logging.error(f"Error processing {symbol}: {str(e)}")
                    continue
            
            result = stock_data if stock_data else None
            if result:
                self._set_cache(cache_key, result)
            return result
            
        except Exception as e:
            logging.error(f"Error fetching multiple symbols: {str(e)}")
            # Fallback to individual requests if batch fails
            stock_data = []
            for symbol in symbols:
                data = self.get_latest_price(symbol)
                if data:
                    stock_data.append(data)
            return stock_data if stock_data else None
    
    def search_symbol(self, query: str) -> Optional[Dict]:
        """Search for stock symbols"""
        return self.get_latest_price(query)
