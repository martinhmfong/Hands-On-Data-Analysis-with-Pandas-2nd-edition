import numpy as np
import pandas as pd

df = pd.read_csv('data/dirty_data.csv')
contain_nulls = df[
    df.SNOW.isna() | df.SNWD.isna() | df.SNOW.isna() | df.TOBS.isna() | df.WESF.isna() | df.inclement_weather.isna()
    ]


def get_inf_counts(df: pd.DataFrame):
    return {col: df[df[col].isin([np.inf, -np.inf])].shape[0] for col in df.columns}


print(get_inf_counts(df))

df['date'] = pd.to_datetime(df.date)
station_qm_wesf = df[df.station == '?'].drop_duplicates('date').set_index('date').WESF
df.sort_values('station', ascending=False, inplace=True)

df_deduped = df.drop_duplicates('date')
df_deduped = df_deduped.drop(columns='station').set_index('date').sort_index()
df_deduped = df_deduped.assign(
    WESF=lambda x: x.WESF.combine_first(station_qm_wesf)
)
print('done')
