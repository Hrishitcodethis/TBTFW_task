# TBTFW_task

Trading Signal Logic
Overview
This project implements a trading signal logic based on moving average crossovers. The strategy generates buy and sell signals by analyzing the crossovers of various moving averages over different time periods.

Signal Logic
Buy Signal
Generate a buy signal if there's a crossover of the 50-day and 500-day moving averages.

Sell Signal
Generate a sell signal if there's a crossover of the 20-day and 200-day moving averages.

Closing Positions
Close any existing buy positions if a crossover of the 10-day and 20-day moving averages takes place.
Close any existing sell positions if a crossover of the 5-day and 10-day moving averages takes place.
Implementation Details
The project is implemented in Python.
It utilizes libraries such as pandas for data manipulation and matplotlib for visualization.
Historical price data is required for the analysis.
The program identifies crossover points and generates corresponding signals.
Position management is implemented to close existing positions based on crossover events.

Assumptions:
1. Any leftover buy postions were exited on the latest date to give profit/loss value (potential)
2. Jiofin data set and inr data set had missing values which were filled by real time data and later sent to postgres database
3. If there are shares bought and sell signal occurs. considered as short selling

