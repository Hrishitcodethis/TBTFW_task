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
df=pd.read_csv('/Users/hrishityelchuri/TBTFW_task/TBTFW_task/data/JIOFIN.NS.csv')

# %%
df.info()

# %%
df

# %% [markdown]
# The dataset contains 1 null value

# %%
df[df.isnull().any(axis=1)]

# %% [markdown]
# We can fill this by getting real time value from yfinance

# %%
# Fetch JIOFIN.NS stock data from Yahoo Finance
start_date = '2023-08-21'
end_date = '2024-02-17'
jf = yf.download('JIOFIN.NS', start=start_date, end=end_date)
jf.reset_index(inplace=True)

# %%
df=jf.copy()

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

# %% [markdown]
# There are no buy or sell positions here because our signals work for 500 day MA, which is null here

# %%



