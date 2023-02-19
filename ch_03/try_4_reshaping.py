import pandas as pd

long_df = pd.read_csv('data/long_data.csv', usecols=['date', 'datatype', 'value']) \
    .rename(columns={'value': 'temp_C'}) \
    .assign(
    date=lambda x: pd.to_datetime(x.date),
    temp_F=lambda x: (x.temp_C / 5 * 9) + 32
)

pivot_df = long_df.pivot(
    index='date', columns='datatype', values=['temp_C', 'temp_F']
)

multi_index_df = long_df.set_index(['date', 'datatype'])
unstacked_df = multi_index_df.unstack()
print(f'unstacked_df.equals(pivot_df): {unstacked_df.equals(pivot_df)}')

extra_data = long_df.append([{
    'datatype': 'TAVG',
    'date': '2018-10-01',
    'temp_C': 10,
    'temp_F': 50
}]).set_index(['date', 'datatype']).sort_index()
unstacked_extra_df = extra_data.unstack(fill_value=-40)

wide_df = pd.read_csv('data/wide_data.csv')
melted_df = wide_df.melt(
    id_vars='date',
    value_vars=['TMAX', 'TMIN', 'TOBS'],
    value_name='temp_C',
    var_name='measurement'
)
indexed_wide_df = wide_df.set_index('date')
stacked_series = indexed_wide_df.stack()
print(f'type(stacked_series): {type(stacked_series)}')

stacked_df = stacked_series.to_frame('values')
print(stacked_df.index.names)
stacked_df.index.set_names(['data', 'datatype'], inplace=True)

print('done')
