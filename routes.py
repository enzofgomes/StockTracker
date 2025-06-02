from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app
from forms import StockSearchForm, QuickSearchForm
from yfinance_api import YFinanceAPI
from utils import format_currency, format_percentage, get_popular_stocks, get_all_available_stocks
import logging
from datetime import datetime

# Initialize API client
api_client = YFinanceAPI()

@app.route('/')
def index():
    """Main dashboard page with user-selected stocks"""
    # Get user preferences from URL parameter or use defaults
    user_symbols = request.args.get('symbols')
    if user_symbols:
        popular_symbols = user_symbols.split(',')
    else:
        popular_symbols = get_popular_stocks()
    
    popular_stocks = []
    
    # Get current data for selected stocks
    stock_data = api_client.get_multiple_symbols(popular_symbols)
    if stock_data:
        for stock in stock_data:
            try:
                # Calculate percentage change
                current_price = stock.get('close', 0)
                previous_close = stock.get('previous_close', stock.get('open', current_price))
                
                if previous_close and previous_close != 0:
                    change_percent = ((current_price - previous_close) / previous_close) * 100
                else:
                    change_percent = 0
                
                popular_stocks.append({
                    'symbol': stock.get('symbol', ''),
                    'close': current_price,
                    'change_percent': change_percent,
                    'volume': stock.get('volume', 0),
                    'high': stock.get('high', 0),
                    'low': stock.get('low', 0)
                })
            except (KeyError, TypeError, ZeroDivisionError) as e:
                logging.error(f"Error processing stock data: {e}")
                continue
    
    quick_form = QuickSearchForm()
    return render_template('index.html', 
                         popular_stocks=popular_stocks,
                         quick_form=quick_form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Search page with simple form"""
    form = StockSearchForm()
    
    if form.validate_on_submit():
        symbol = form.symbol.data.upper()
        data_type = form.data_type.data
        exchange = form.exchange.data
        
        # Build URL with exchange parameter if provided
        if exchange:
            return redirect(url_for('stock_detail', symbol=symbol, data_type=data_type, exchange=exchange))
        else:
            return redirect(url_for('stock_detail', symbol=symbol, data_type=data_type))
    
    return render_template('search.html', form=form)

@app.route('/stock/<symbol>')
def stock_detail(symbol):
    """Show detailed stock information"""
    data_type = request.args.get('data_type', 'latest')
    
    stock_info = None
    historical_data = None
    chart_data = None
    
    try:
        if data_type == 'latest':
            # Get current stock price
            stock_info = api_client.get_latest_price(symbol)
            # Also get some historical data for chart
            historical_data = api_client.get_historical_data(symbol, limit=30)
            
        elif data_type == 'historical':
            # Get 30 days of historical data
            historical_data = api_client.get_historical_data(symbol, limit=30)
            if historical_data:
                stock_info = historical_data[0]  # Most recent data
        
        if not stock_info:
            flash(f'No data found for symbol: {symbol}', 'error')
            return redirect(url_for('search'))
        
        # Prepare chart data
        if historical_data:
            chart_data = {
                'labels': [data.get('date', '')[:10] for data in reversed(historical_data)],
                'prices': [data.get('close', 0) for data in reversed(historical_data)],
                'volumes': [data.get('volume', 0) for data in reversed(historical_data)]
            }
        
        # Calculate additional metrics
        if historical_data and len(historical_data) > 1:
            current_price = stock_info.get('close', 0)
            previous_price = historical_data[1].get('close', current_price)
            
            if previous_price and previous_price != 0:
                change_percent = ((current_price - previous_price) / previous_price) * 100
                change_amount = current_price - previous_price
            else:
                change_percent = 0
                change_amount = 0
                
            stock_info['change_percent'] = change_percent
            stock_info['change_amount'] = change_amount
        
    except Exception as e:
        logging.error(f"Error fetching stock data for {symbol}: {str(e)}")
        flash(f'Error fetching data for {symbol}: {str(e)}', 'error')
        return redirect(url_for('search'))
    
    return render_template('stock_detail.html', 
                         stock_info=stock_info,
                         historical_data=historical_data,
                         chart_data=chart_data,
                         symbol=symbol.upper())

@app.route('/quick_search', methods=['POST'])
def quick_search():
    """Handle quick symbol search from main page"""
    form = QuickSearchForm()
    
    if form.validate_on_submit():
        symbol = form.symbol.data.upper()
        return redirect(url_for('stock_detail', symbol=symbol))
    
    flash('Please enter a valid stock symbol', 'error')
    return redirect(url_for('index'))

@app.route('/favorites')
def favorites():
    """Simple favorites page with popular stocks"""
    # For beginners, use a simple predefined list
    favorite_symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']
    
    favorites_data = []
    stock_data = api_client.get_multiple_symbols(favorite_symbols)
    
    if stock_data:
        for stock in stock_data:
            try:
                symbol = stock.get('symbol', 'N/A')
                current_price = stock.get('price', 0)
                previous_close = stock.get('previous_close', current_price)
                
                if previous_close and previous_close != 0:
                    change_percent = ((current_price - previous_close) / previous_close) * 100
                else:
                    change_percent = 0.0
                
                favorites_data.append({
                    'symbol': symbol,
                    'price': current_price,
                    'change_percent': change_percent,
                    'volume': stock.get('volume', 0)
                })
            except Exception as e:
                logging.error(f"Error processing favorite stock data: {e}")
                continue
    
    return render_template('favorites.html', favorites=favorites_data)

@app.route('/preferences')
def preferences():
    """Simple preferences page for stock selection"""
    return render_template('preferences.html')

@app.route('/api/stock/<symbol>')
def api_stock_data(symbol):
    """API endpoint for AJAX requests"""
    try:
        stock_data = api_client.get_latest_price(symbol)
        if stock_data:
            return jsonify(stock_data)
        else:
            return jsonify({'error': 'Stock not found'}), 404
    except Exception as e:
        logging.error(f"API error for {symbol}: {str(e)}")
        return jsonify({'error': str(e)}), 500



@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
