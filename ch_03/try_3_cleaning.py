import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import StrMethodFormatter

wide_df = pd.read_csv('data/wide_data.csv', parse_dates=['date'])
long_df = pd.read_csv(
    'data/long_data.csv', parse_dates=['date'], usecols=['date', 'datatype', 'value']
)[['date', 'datatype', 'value']]

wide_df.plot(
    x='date', y=['TMAX', 'TMIN', 'TOBS'],
    figsize=(15, 5), title='Temperature in NYV in October 2018'
).set_ylabel('Temerature in Celsius')
# plt.show()

sns.set(rc={'figure.figsize': (15, 5)}, style='dark')
ax = sns.lineplot(data=long_df, x='date', y='value', hue='datatype')
ax.set_ylabel('Temperature in Celsius')
ax.set_title('Temperature in NYC in October 2018')
# plt.show()

sns.set(
    rc={'figure.figsize': (20, 10)},
    style='dark',
)
g = sns.FacetGrid(long_df, col='datatype', height=10)
g = g.map(plt.plot, 'date', 'value')
g.set_titles(size=25)
g.set_xticklabels(rotation=45)
# plt.show()

df = pd.read_csv('data/nyc_temperatures.csv')
df.rename(columns={
    'value': 'temp_C',
    'attibutes': 'flags'
}, inplace=True
)
# df.loc[:, 'date'] = pd.to_datetime(df.date)
eastern = pd.read_csv('data/nyc_temperatures.csv', index_col='date', parse_dates=True).tz_localize('EST')
hongkong = eastern.tz_convert('HongKong')

new_df = df.assign(
    date=pd.to_datetime(df.date),
    temp_F=(df.temp_C * 9 / 5) + 32
)

df = df.assign(
    date=lambda x: pd.to_datetime(x.date),
    temp_C_whoel=df.temp_C.astype('int'),
    temp_F=(df.temp_C * 9 / 5) + 32,
    temp_F_whoel=lambda x: x.temp_F.astype('int'),
    station=df.station.astype('category'),
    datatype=df.datatype.astype('category'),
)

sp = pd.read_csv('data/sp500.csv', index_col='date', parse_dates=True).drop(columns=['adj_close'])
sp = sp.assign(day_of_week=lambda x: x.index.day_name())

bitcoin = pd.read_csv('data/bitcoin.csv', index_col='date', parse_dates=True).drop(columns=['market_cap'])

portfolio = pd.concat([sp, bitcoin], sort=False).groupby('date').sum()
portfolio = portfolio.assign(day_of_week=lambda x: x.index.day_name())

# need to reindex the sp using the bitcoin index
sp = sp.reindex(bitcoin.index, method='ffill').assign(
    day_of_week=lambda x: x.index.day_name(),
    volume=lambda x: x.volume.fillna(0),
    close=lambda x: x.close.fillna(method='ffill'),
    open=lambda x: np.where(x.open.isnull(), x.close, x.open),
    high=lambda x: np.where(x.high.isnull(), x.close, x.high),
    low=lambda x: np.where(x.low.isnull(), x.close, x.low),
)
fix_portfolio = sp + bitcoin

# plot the closing price from Q4 2017 through Q2 2018
ax = portfolio['2017-Q4':'2018-Q2'].plot(
    y='close', figsize=(15, 5), legend=False,
    title='Bitcoin + S&P 500 value without accounting for different indices'
)

# formatting
ax.set_ylabel('price')
ax.yaxis.set_major_formatter(StrMethodFormatter('${x:,.0f}'))
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)

# show the plot
plt.show()
print('done')
