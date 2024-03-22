# %%
import pandas as pd
import numpy as np
import yfinance as yf
import mplfinance as mpf

# %%
from sqlalchemy import create_engine

# %%
engine = create_engine('postgresql://postgres:phyinfinite@localhost:5432/tbtfw')

# %%
try:
    connection = engine.connect()
    print("Connected to the database")
except Exception as e:
    print("Unable to connect to the database:", e)

# %%
query = 'SELECT * FROM mara'  # Adjust query based on your table structure
df = pd.read_sql(query, engine)

# %%
df

# %%
df.info()

# %%
df.describe()

# %%
df.shape

# %%
df.duplicated().sum()

# %%
# Fetch MARA stock data from Yahoo Finance
start_date = '2012-05-04'
end_date = '2024-02-17'
mara = yf.download('MARA', start=start_date, end=end_date)
mara.reset_index(inplace=True)

# %%
mara

# %%
# Calculate moving averages for df data
df['50-day MA'] = df['Close'].rolling(window=50).mean()
df['500-day MA'] = df['Close'].rolling(window=500).mean()
df['20-day MA'] = df['Close'].rolling(window=20).mean()
df['200-day MA'] = df['Close'].rolling(window=200).mean()
df['10-day MA'] = df['Close'].rolling(window=10).mean()
df['5-day MA'] = df['Close'].rolling(window=5).mean()

# %%
df

# %%
# Generate buy and sell signals
df['Buy Signal'] = ((df['50-day MA'] > df['500-day MA']) & (df['20-day MA'] > df['200-day MA'])).astype(int)
df['Sell Signal'] = ((df['20-day MA'] < df['200-day MA']) & (df['10-day MA'] < df['5-day MA'])).astype(int)

# %%
# Generate buy and sell signals, and track buy/sell positions (remaining part)
buy_position = False
sell_position = False
positions = []

# %%
for index, row in df.iterrows():
    if row['Buy Signal'] == 1:
        if not buy_position:
            buy_position = True
            positions.append(('Buy', row['Date'], row['Close']))
    elif row['Sell Signal'] == 1:
        if not sell_position:
            sell_position = True
            positions.append(('Sell', row['Date'], row['Close']))
    else:
        if buy_position:
            buy_position = False
            positions.append(('Close Buy', row['Date'], row['Close']))
        if sell_position:
            sell_position = False
            positions.append(('Close Sell', row['Date'], row['Close']))

# %%
# Print the buy/sell positions
print("Buy/Sell Positions:")
for position in positions:
    print(position)

# %%
# Initialize variables
stock_name = 'MARA'  # Assuming the stock name is HDB
trade_history = []

# Check if the last position is a buy position
last_position_is_buy = positions[-1][0] == 'Buy'

# Initialize variables for profit/loss calculation
buy_price = None
sell_price = None

# Iterate through positions to find the last buy and sell prices
for position in reversed(positions):
    if position[0] == 'Buy':
        buy_price = position[2]
    elif position[0] == 'Sell':
        sell_price = position[2]
    # Break the loop if both buy and sell prices are found
    if buy_price is not None and sell_price is not None:
        break

# Calculate final profit/loss based on the last position
if last_position_is_buy:
    # If the last position is a buy position and there are no subsequent sell positions,
    # calculate profit/loss using the latest selling price
    if sell_price is not None:
        final_profit_loss = sell_price - buy_price
    else:
        latest_close_price = df.loc[end_date]['Close']  # Get the close price on end date
        final_profit_loss = latest_close_price - buy_price
else:
    # If the last position is a sell position and there was a previous buy position, calculate profit/loss
    final_profit_loss = sell_price - buy_price

# Append stock name and final profit/loss to trade history
trade_history.append((stock_name, final_profit_loss))

# Print trade history
print("Trade History:", trade_history)


# %%
# Create a DataFrame from the trade history list
trade_df = pd.DataFrame(trade_history, columns=['Stock_Name','Profit/Loss'])

# Store the trade history DataFrame into the database
trade_df.to_sql('trade_history', engine, if_exists='append', index=False)

# %%
# Fetch MARA stock data from Yahoo Finance
start_date = '2023-02-21'
end_date = '2024-02-16'
mara = yf.download('MARA', start=start_date, end=end_date)

# Calculate moving averages for MARA data
mara['50-day MA'] = mara['Close'].rolling(window=50).mean()
mara['500-day MA'] = mara['Close'].rolling(window=500).mean()
mara['20-day MA'] = mara['Close'].rolling(window=20).mean()
mara['200-day MA'] = mara['Close'].rolling(window=200).mean()
mara['10-day MA'] = mara['Close'].rolling(window=10).mean()
mara['5-day MA'] = mara['Close'].rolling(window=5).mean()

# Plot candlestick chart for MARA stock data
mpf.plot(mara, type='candle', style='charles', ylabel='Price', ylabel_lower='Volume', 
         volume=True, mav=(50, 500), figsize=(14, 7), title='MARA Candlestick Chart with Moving Averages')

# Annotate buy/sell positions on the plot
for position in positions:
    date_index = pd.to_datetime(position[1]).date()
    if position[0] in ['Buy', 'Sell'] and date_index in mara.index:
        mpf.plot(mara.loc[date_index], type='scatter', style='o', markersize=100, color='r' if position[0] == 'Buy' else 'g')


# %%



