import pandas as pd


def q1():
    faang = pd.DataFrame()
    for ticker in ('aapl', 'amzn', 'fb', 'goog', 'nflx'):
        df = pd.read_csv(f'exercises/{ticker}.csv')
        df.insert(0, 'ticker', ticker.upper())
        faang = pd.concat([faang, df])
    return faang.reset_index(drop=True)


def q2():
    faang = q1()
    faang = faang.assign(
        date=pd.to_datetime(faang.date),
        volume=faang.volume.astype('int')
    ).sort_values(['date', 'ticker'])
    return faang


def q3():
    faang = q2()
    print(faang.nsmallest(7, 'volume'))


def q4():
    faang = q2()
    melt_df = faang.melt(
        id_vars=['date', 'ticker'],
        value_vars=['high', 'low', 'open', 'close', 'volume'],
    )
    return melt_df


def q6():
    df = pd.read_csv('exercises/covid19_cases.csv') \
        .assign(date=lambda x: pd.to_datetime(x.dateRep, dayfirst=True)) \
        .set_index('date').replace('United_States_of_America', 'USA') \
        .replace('United_Kingdom', 'UK') \
        .sort_index()

    required_locations = [
        'Argentina', 'Brazil', 'China', 'Colombia', 'India', 'Italy',
        'Mexico', 'Peru', 'Russia', 'Spain', 'Turkey', 'UK', 'USA'
    ]
    cleaned = df[df.countriesAndTerritories.isin(required_locations)]
    pivot = cleaned.reset_index().pivot('date', 'countriesAndTerritories', 'cases').fillna(0)
    return pivot


def q7():
    total_cases = pd.read_csv('exercises/covid19_total_cases.csv', index_col='index')
    df = total_cases.T
    largest = df.nlargest(20, 'cases').sort_values('cases', ascending=False)
    return largest


if __name__ == '__main__':
    q7()
