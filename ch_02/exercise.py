import pandas as pd
import numpy as np


def exercise():
    df = pd.read_csv('data/parsed.csv')
    # task 1
    jp_mag = df.loc[
        (df['parsed_place'] == 'Japan') & (df['magType'] == 'mb'),
        'mag'
    ]
    print(np.percentile(jp_mag, 95))
    # or
    print(jp_mag.quantile(.95))

    # task2
    indonesia = df.loc[df['parsed_place'] == 'Indonesia']
    print(f"{indonesia['tsunami'].value_counts(normalize=True).loc[1]:.2%}")

    # task3
    nevada = df[df.parsed_place == 'Nevada']
    print(nevada.describe())

    # task4
    df['ring_of_fire'] = df.parsed_place.str.contains(r'|'.join([
        'Alaska', 'Antarctic', 'Bolivia', 'California', 'Canada',
        'Chile', 'Costa Rica', 'Ecuador', 'Fiji', 'Guatemala',
        'Indonesia', 'Japan', 'Kermadec Islands', '^Mexico',
        'New Zealand', 'Peru', 'Philippines', 'Russia',
        'Taiwan', 'Tonga', 'Washington'
    ]))

    # task5
    print(df['ring_of_fire'].value_counts())

    # task6
    print(df[df['ring_of_fire']]['tsunami'].sum())


if __name__ == '__main__':
    exercise()
