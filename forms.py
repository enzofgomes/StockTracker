from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class StockSearchForm(FlaskForm):
    """Form for searching stock data with exchange filtering"""
    
    symbol = StringField('Stock Symbol', 
                        validators=[DataRequired(), Length(min=1, max=10)],
                        render_kw={"placeholder": "e.g., AAPL, MSFT, GOOGL"})
    
    data_type = SelectField('Data Type',
                           choices=[
                               ('latest', 'Latest Price'),
                               ('historical', 'Historical Data (30 days)')
                           ],
                           default='latest',
                           validators=[DataRequired()])
    
    exchange = SelectField('Exchange',
                          choices=[
                              ('', 'All Exchanges'),
                              ('XNAS', 'NASDAQ'),
                              ('XNYS', 'NYSE'),
                              ('BATS', 'BATS'),
                              ('PINK', 'Pink Sheets')
                          ],
                          validators=[Optional()])
    
    submit = SubmitField('Get Stock Data')

class QuickSearchForm(FlaskForm):
    """Simple form for quick symbol lookup"""
    symbol = StringField('Symbol', validators=[DataRequired()])
    submit = SubmitField('Search')
