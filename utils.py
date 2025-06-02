from typing import List, Dict

def format_currency(amount: float) -> str:
    """Format amount as currency"""
    if amount is None:
        return "N/A"
    return f"${amount:,.2f}"

def format_percentage(percentage: float) -> str:
    """Format percentage with proper sign and color class"""
    if percentage is None:
        return "N/A"
    
    sign = "+" if percentage > 0 else ""
    return f"{sign}{percentage:.2f}%"

def get_percentage_class(percentage: float) -> str:
    """Get CSS class for percentage based on positive/negative"""
    if percentage is None:
        return ""
    return "text-success" if percentage >= 0 else "text-danger"

def format_volume(volume: int) -> str:
    """Format trading volume in readable format"""
    if volume is None:
        return "N/A"
    
    if volume >= 1_000_000:
        return f"{volume / 1_000_000:.1f}M"
    elif volume >= 1_000:
        return f"{volume / 1_000:.1f}K"
    else:
        return str(volume)

def get_popular_stocks() -> List[str]:
    """Return list of popular stock symbols for the main dashboard"""
    return [
        'AAPL',   # Apple Inc.
        'MSFT',   # Microsoft Corporation
        'GOOGL',  # Alphabet Inc.
        'AMZN',   # Amazon.com Inc.
        'TSLA',   # Tesla Inc.
        'META',   # Meta Platforms Inc.
        'NVDA',   # NVIDIA Corporation
        'JPM',    # JPMorgan Chase & Co.
    ]

def get_all_available_stocks() -> List[Dict[str, str]]:
    """Return comprehensive list of available stocks for user selection"""
    return [
        {'symbol': 'AAPL', 'name': 'Apple Inc.'},
        {'symbol': 'MSFT', 'name': 'Microsoft Corporation'},
        {'symbol': 'GOOGL', 'name': 'Alphabet Inc.'},
        {'symbol': 'AMZN', 'name': 'Amazon.com Inc.'},
        {'symbol': 'TSLA', 'name': 'Tesla Inc.'},
        {'symbol': 'META', 'name': 'Meta Platforms Inc.'},
        {'symbol': 'NVDA', 'name': 'NVIDIA Corporation'},
        {'symbol': 'JPM', 'name': 'JPMorgan Chase & Co.'},
        {'symbol': 'JNJ', 'name': 'Johnson & Johnson'},
        {'symbol': 'V', 'name': 'Visa Inc.'},
        {'symbol': 'PG', 'name': 'Procter & Gamble Company'},
        {'symbol': 'MA', 'name': 'Mastercard Incorporated'},
        {'symbol': 'UNH', 'name': 'UnitedHealth Group'},
        {'symbol': 'HD', 'name': 'Home Depot Inc.'},
        {'symbol': 'BAC', 'name': 'Bank of America Corporation'},
        {'symbol': 'DIS', 'name': 'Walt Disney Company'},
        {'symbol': 'NFLX', 'name': 'Netflix Inc.'},
        {'symbol': 'ADBE', 'name': 'Adobe Inc.'},
        {'symbol': 'CRM', 'name': 'Salesforce Inc.'},
        {'symbol': 'PYPL', 'name': 'PayPal Holdings Inc.'},
        {'symbol': 'INTC', 'name': 'Intel Corporation'},
        {'symbol': 'AMD', 'name': 'Advanced Micro Devices'},
        {'symbol': 'IBM', 'name': 'International Business Machines'},
        {'symbol': 'ORCL', 'name': 'Oracle Corporation'},
        {'symbol': 'WMT', 'name': 'Walmart Inc.'},
        {'symbol': 'KO', 'name': 'Coca-Cola Company'},
        {'symbol': 'PEP', 'name': 'PepsiCo Inc.'},
        {'symbol': 'NKE', 'name': 'Nike Inc.'},
        {'symbol': 'MCD', 'name': 'McDonald\'s Corporation'},
        {'symbol': 'SBUX', 'name': 'Starbucks Corporation'}
    ]

def safe_float(value, default=0.0):
    """Safely convert value to float"""
    try:
        return float(value) if value is not None else default
    except (ValueError, TypeError):
        return default

def safe_int(value, default=0):
    """Safely convert value to integer"""
    try:
        return int(value) if value is not None else default
    except (ValueError, TypeError):
        return default
