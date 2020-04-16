#!/usr/bin/env python
# coding: utf-8

# # 1. Climate Analysis and Exploration

# #### To begin, use Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database

# ## Dependencies

# In[1]:


from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates


# In[2]:


import numpy as np
import pandas as pd
from pandas.plotting import table
import datetime as dt
import datetime
import scipy.stats as stats


# ## Reflect Tables into SQLAlchemy

# In[3]:


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# In[4]:


engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# In[5]:


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# In[6]:


# We can view all of the classes that automap found
Base.classes.keys()


# In[7]:


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# In[8]:


# Create our session (link) from Python to the DB
session = Session(engine)
dir(session)


# ## Exploratory Climate Analysis

# ### Design a query to retrieve the last 12 months of precipitation data and plot the results

# In[9]:


# Set column info to vars
date = Measurement.date
prcp = Measurement.prcp


# #### Calculate the date 1 year ago from the last data point in the database

# In[10]:


#Displaying the last data point of the measurement data
session.query(Measurement.date).all()[-1]


# In[11]:


last_yr = dt.date(2017,8,23) - dt.timedelta(days=365)
last_yr


# #### Query to retrieve all date and prcp data for a year

# In[12]:


result = session.query(date, prcp).filter(Measurement.date >= last_yr).all()
result


# #### Save the query results as a Pandas DataFrame and set the index to the date column

# In[13]:


#Creating a DF using Pandas
results_df = pd.DataFrame(result, columns=['Date','Precipitation'])

# Converting the Date column into date type
results_df['Date'] = pd.to_datetime(results_df['Date'])

# Setting the index into Date Column
results_df.set_index(results_df['Date'],inplace=True)

# Dropping the repeated column of Date 
results_df = results_df.drop(columns="Date")

# Sorting the DF by date
results_df.sort_values('Date')

#Displaying the results
results_df


# In[14]:


len(results_df)


# #### Use Pandas Plotting with Matplotlib to plot the data

# In[15]:


# Variables to be plotted
xaxis = results_df.index
yaxis = results_df["Precipitation"]

# Formatting the date
date_form = DateFormatter("%Y-%m-%d")

# Plotting the results using the DF plot method
ax = results_df.plot(color='dodgerblue', alpha=0.9, figsize=(10,7), rot=90, linewidth=6)
ax.xaxis.set_major_formatter(date_form)

# Ensure a major tick using (interval=10) 
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=5))
ax.set_xlim([datetime.date(2016,8,23),datetime.date(2017,8,22)])

# Aesthetics for the chart
plt.title("Precipitation Data for 1 year", fontsize = 15)
plt.xlabel("Date", fontsize = 14)
plt.ylabel("Inches", fontsize = 14)


# #### Use Pandas to print the summary statistics for the precipitation data

# In[16]:


results_df.describe()


# In[17]:


# Design a query to show how many stations are available in this dataset?
station_count = session.query(func.count(Station.station)).all()
station_count


# #### What are the most active stations? (i.e. what stations have the most rows)?
#         - List the stations and the counts in descending order.

# In[18]:


stations_list = session.query(Measurement.station,func.count(Measurement.station)).    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
stations_list


# #### Using the station id from the previous query, calculate the lowest temperature recorded, highest temperature recorded, and average temperature of the most active station?

# In[19]:


temp_query = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).    filter(Measurement.station =='USC00519281').all()
temp_query


# #### Choose the station with the highest number of temperature observations
#         - Query the last 12 months of temperature observation data for this station

# In[20]:


highest_temp = session.query(Measurement.date, Measurement.tobs).    filter(Measurement.date >= last_yr).    filter(Measurement.station =='USC00519281').all()

high_tobs_df = pd.DataFrame(highest_temp, columns=['Date', 'TOBS'])
high_tobs_df


#         - Plot the results as a histogram

# In[21]:


# Plotting the results using the DF plot method

high_tobs_df.hist(color='dodgerblue', bins=12, alpha=0.9, figsize=(10,7))

# Aesthetics for the chart
plt.title("Highest TOBS for 1 year", fontsize = 15)
plt.xlabel("Observed Temperatures", fontsize = 14)
plt.ylabel("Frequency", fontsize = 14)


# # Bonus Challenge Assignments:

# ## Temperature Analysis I

#     - Hawaii is reputed to enjoy mild weather all year. Is there a meaningful difference between the temperature in, for example, June and December?
#     - You may either use SQLAlchemy or pandas's read_csv() to perform this portion.
#     - Identify the average temperature in June at all stations across all available years in the dataset. Do the same for December temperature.
#     - Use the t-test to determine whether the difference in the means, if any, is statistically significant. Will you use a paired t-test, or an unpaired t-test? Why?

# In[22]:


# Let's use panda's read_csv() to carry out this portion

#Reading the stations csv file
hawaii_stations = pd.read_csv('Resources/hawaii_stations.csv')
hawaii_stations


# In[23]:


#Reading the measurements csv file

hawaii_measurements = pd.read_csv('Resources/hawaii_measurements.csv')
hawaii_measurements


# In[24]:


# Identifying the average June and December temperatures and grouping the measurements by station

# June Average Temperatures

av_june_temp = hawaii_measurements[hawaii_measurements['date'].str.slice(start=5, stop=7)=='06'].groupby(hawaii_measurements['station']).mean()
av_june_temp


# In[25]:


# December Average Temperatures
av_dec_temp = hawaii_measurements[hawaii_measurements['date'].str.slice(start=5, stop=7)=='12'].groupby(hawaii_measurements['station']).mean()
av_dec_temp


# In[26]:


stats.ttest_ind(av_june_temp['tobs'], av_dec_temp['tobs'], equal_var=False)


# ### My findings: 
# 
# #### We used unpaired T test since we assumed that the measurments from June and December are independent from each other. The dataset consist of distinct test subjects
# #### The results of the T test (statistic and pvalue) reflect that there is a statistically significant difference between June and December average temperatures. 

# ## Temperature Analysis II

#     - This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' and return the minimum, average, and maximum temperatures for that range of dates

# In[27]:


# calc_temps function
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

# function usage example
print(calc_temps('2012-02-28', '2012-03-05'))


# In[28]:


# Calculating start_date and end_date in the format specified for the the matching dates from the previous year

lst_start_date = dt.date(2017, 1, 1) - dt.timedelta(days=365)
lst_end_date = dt.date(2017, 1, 14) - dt.timedelta(days=365)

print(lst_start_date)
print(lst_end_date)


#     - Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax for your trip using the previous year's data for those same dates.

# In[29]:


# This function will display tmin, tavg and tmax for my trip (same dates)
trip_tobs = calc_temps(lst_start_date.strftime("%Y-%m-%d"), lst_end_date.strftime("%Y-%m-%d"))
trip_tobs


# In[30]:


# Let's display the results:
tmin = trip_tobs[0][0]
tavg = round(trip_tobs[0][1],2)
tmax = trip_tobs[0][2]
print(f'tmin = {tmin}')
print(f'tavg = {tavg}')
print(f'tmax = {tmax}')


#     - Plot the results from your previous query as a bar chart. 
#     - Use "Trip Avg Temp" as your Title
#     - Use the average temperature for the y value
#     - Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr)

# In[31]:


#Defining the peak-topeak value before plotting
yerr=(tmax-tmin)/2

#Plotting with Pyplot following the above instructions
plt.figure(figsize=(3, 6), dpi=70) # Figure size
plt.bar([""],tavg, yerr=(tmax-tmin)/2, color='green', alpha=0.6)

# Aesthetics for the chart
plt.title("Trip Avg Temp", fontsize=16)
plt.xlabel("My Trip", fontsize=14)
plt.ylabel("Temp (F)", fontsize=14)
plt.ylim(0,80)
plt.xlim(-0.6,0.6)

print(f'Peak-to-Peak Value is {yerr} F')


# ## Daily Rainfall Average

#     - Calculate the total amount of rainfall per weather station for your trip dates using the previous year's matching dates
#     - Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation

# In[32]:


# Creating a list with the above details
sel = [Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation, func.sum(Measurement.prcp)]

# Filtersing per weather station and my trip previous year's matching dates and grouping by station name in descending order

results = session.query(*sel).            filter(Measurement.station == Station.station).            filter(Measurement.date >= lst_start_date).            filter(Measurement.date >= lst_end_date).            group_by(Station.name).            order_by(func.sum(Measurement.prcp).desc()).all()
results


#      - Create a query that will calculate the daily normals 
#         (i.e. the averages for tmin, tmax, and tavg for all historic data matching a specific month and day)

# In[33]:


# Our given function named daily_normals

def daily_normals(date):
    """Daily Normals.
    
    Args:
        date (str): A date string in the format '%m-%d'
        
    Returns:
        A list of tuples containing the daily normals, tmin, tavg, and tmax
    
    """
    
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    return session.query(*sel).filter(func.strftime("%m-%d", Measurement.date) == date).all()

# Example
daily_normals("01-01")


# In[34]:


# Setting the start and end date of the trip
start_date = dt.date(2017, 1, 1)
end_date = dt.date(2017, 1, 14)
lst_start_date = dt.date(2017, 1, 1).strftime("%m-%d")
lst_end_date = dt.date(2017,1, 14).strftime("%m-%d")

print(start_date)
print(end_date)
print(lst_start_date)
print(lst_end_date)


# In[35]:


# Use the start and end date to create a range of dates

results = session.query(Measurement.date).order_by(Measurement.date).           filter(Measurement.date>=start_date).           filter(Measurement.date<=end_date).distinct()
results


# In[36]:


# Stip off the year and save a list of %m-%d strings

my_dates = pd.DataFrame(results.all())
my_dates_df = my_dates.set_index('date')
my_dates_df


# In[37]:


# Converting the format from %Y-%m-%d to %m-%d

month_format = my_dates['date'].str.slice(start=5)
month_format


# In[38]:


# Loop through the list of %m-%d strings and calculate the normals for each date
day_normals=[]

for month in range(len(month_format)):
    day = daily_normals(month_format[month])[0]
    day_normals.append(tuple(day))
day_normals


# In[39]:


# Load the list of daily normals into a Pandas DataFrame and set the index equal to the date.

df = pd.DataFrame(day_normals, columns = ['tmin','tavg', 'tmax'] )
my_df = pd.merge(my_dates, df, left_index=True, right_index=True)
my_df = my_df.set_index('date')
my_df


# In[40]:


# Plot the daily normals as an area plot with `stacked=False`

ax = my_df.plot.area(stacked=False, rot=45)

# Aesthetics for the chart
plt.title("Trip Daily Normals", fontsize=16)
plt.xlabel("My Dates", fontsize=14)
plt.ylabel("Temp (F)", fontsize=14)


# # Script for the Climate App

# ### Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.
# 
# #### - Use Flask to create your routes.

# ### /api/v1.0/precipitation
#     - Convert the query results to a dictionary using date as the key and prcp as the value.
#     - Return the JSON representation of your dictionary.

# In[41]:


# This variable is called from Climate_app
results_dic = dict(result)
results_dic


# ### /api/v1.0/stations
#     - Return a JSON list of stations from the dataset.

# In[42]:


my_stations = session.query(Station.station, Station.name).all()
my_stations_dic = dict(my_stations)
my_stations_dic


# ### /api/v1.0/tobs
#     - Query the dates and temperature observations of the most active station for the last year of data.
#     - Return a JSON list of temperature observations (TOBS) for the previous year.

# In[43]:


values=trip_tobs[0]
keys = ('tmin','tavg','tmax')

my_tobs = dict(zip(keys,values))
my_tobs


# ### Start and End Dates
#     - Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#     - When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#     - When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

# In[44]:


# <start>
start = dt.date(2017, 8, 1)
print(start)


# In[45]:


# /api/v1.0/<start>
# - Return a JSON list of the minimum temperature, the average temperature,
# and the max temperature for a given start or start-end range.
# - When given the start only, calculate TMIN, TAVG, and TMAX for all dates 
# greater than and equal to the start date.

stats_dict={}
start_values = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).        filter(Measurement.date >= start).group_by(Measurement.date).all()

for record in start_values:
        (date, tmin, tavg, tmax) = record
        stats_dict[date] = [{"tmin":tmin, "tavg":round(tavg, 2), "tmax":tmax}]
        
stats_dict


# In[46]:


# /api/v1.0/<start>/<end>
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

end = dt.date(2017, 8, 20)
end_stats_dict={}
end_values = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).        filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()

for record in end_values:
        (date, tmin, tavg, tmax) = record
        end_stats_dict[date] = [{"tmin":tmin, "tavg":round(tavg, 2), "tmax":tmax}]
        
end_stats_dict


# In[ ]:




