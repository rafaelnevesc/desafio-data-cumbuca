from nycflights13 import flights, airlines, planes, airports, weather
import pandas as pd
import matplotlib.pyplot as plt

# 1) Mean and standard deviation in the last 30 days

# Transforming time_hour into datetime
flights['time_hour'] = pd.to_datetime(flights['time_hour'])

# Removing rows without delay
flights_with_delay = flights.query('dep_delay > 0').copy()

# Applying time_hour as index
flights_with_delay.set_index('time_hour', inplace=True)
flights_with_delay.sort_index(inplace=True)

# Applying rolling
roll = flights_with_delay['dep_delay'].rolling(pd.Timedelta(30, 'days'))

mean_dep_time = roll.mean()
std_dep_time = roll.std()

plt.plot(mean_dep_time)
plt.plot(std_dep_time)

plt.show()

# 2) Find the % of flights with more than 5 minutes of delay
#    per airline per month. What's the worst month for Delta Airlines?

pct_five_min_delay = (
    flights
    .assign(more_than_five=flights['dep_delay'] > 5)
    .groupby(['carrier', 'year', 'month'])
    ['more_than_five']
    .mean()
)

pct_five_min_delay = pct_five_min_delay.reset_index()

pct_five_min_delay = pct_five_min_delay.merge(airlines)

pct_five_min_delay.query(
    "name == 'Delta Air Lines Inc.'").sort_values('more_than_five', ascending=False)

# Delta Airline's worst month was July

# 3) For each manufacturer, how many airplanes are operated and how many flights
#    were made? Which manufacturer has least flights?

manu_flights = (
    flights[['tailnum']]
    .dropna()
    .merge(planes[['tailnum', 'manufacturer']],
           how='right')
)

resp = manu_flights.groupby('manufacturer').agg(
    count_flights=('manufacturer', 'size'),
    count_airplanes=('tailnum', pd.Series.nunique)
)

manu_flights.value_counts(['manufacturer', 'tailnum'])

resp.loc[resp['count_flights'] == resp['count_flights'].min()]

# 4) Which airline has flown the most with airbus airplanes

(
    flights[['carrier', 'tailnum']]
    .merge(planes[['tailnum', 'manufacturer']])
    .merge(airlines)
    .query("manufacturer == 'AIRBUS'")
    .value_counts(['name', 'manufacturer'])
    .reset_index()
    .sort_values('count', ascending=False)
    .iloc[0]
)

# JetBlue Airways

# 5) How many flights arrived in each airport in NY between 6pm and 10pm March 3

lower = pd.Timestamp(year=2013, month=3, day=3, hour=18)
upper = pd.Timestamp(year=2013, month=3, day=3, hour=22)

vec = (flights['month'] == 3) & (flights['day'] == 3) & (
    (flights['arr_time'] > 1800) & (flights['arr_time'] < 2200)
)
(
    flights.loc[vec, ['dest']]
    .merge(
        airports[['faa', 'name']],
        left_on='dest',
        right_on='faa'
    )
    .value_counts('name')
)
