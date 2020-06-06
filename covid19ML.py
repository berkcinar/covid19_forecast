import requests
import pandas as pd
from datetime import datetime as dt

def get_daily_values():
    end_point = 'https://api.covid19api.com/dayone/country/turkey/status/confirmed'
    daily_confirmed = requests.get(end_point)
    daily_confirmed_json=daily_confirmed.json()
    print(daily_confirmed_json)

    country_df = pd.DataFrame()
    for i in daily_confirmed_json:
        country_df = country_df.append(
            {
                'timeslot': (dt.strptime(str(i.get('Date')), "%Y-%m-%dT%H:%M:%SZ")).strftime("%Y-%m-%d"),
                'daily_total_case': i.get('Cases'),
            }, ignore_index=True)

    print(country_df)
get_daily_values()