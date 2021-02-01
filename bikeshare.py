 # The time() method from the time module returns the time as a floating point number expressed in seconds. This is used to calculate the time efficiency for some functions.
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some data related to bike share systems for three major cities in the United States: Chicago, New York, and Washington!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Which city of these US cities (Chicago, New York, or Washington) would you like to explore its data? \n').lower()
    while city not in(CITY_DATA.keys()):
        print('Invalid entry, could you choose one of the provided city names?')
        city = input('Would you like to explore some data for Chicago, New York, or Washington? \n').lower()

    # get user input for filter type (month, day or both).
    filter = input('Would you like to filter the data by day, month, both, or none? \n').lower()
    while filter not in(['day', 'month', 'both', 'none']):
        print('Invalid entry, could you choose one of the provided filters?')
        filter = input('Would you like to filter the bikeshare data for the chosen city by day, month, both, or none? \n').lower()


    # get user input for month (all, january, february, ... , june)
    # these are the provided months in the dataset
    months = ['january', 'february', 'march', 'april', 'may', 'june','all']
    #filtering the user input to display the message regarding to the filter.
    if filter == 'both' or filter == 'month':
        month = input('Which month? January, February, March, April, May, June, or all? Please type out the full month name. \n').lower()
     # a while loop is used to handle invalid inputs   
        while month not in months:
            print('Invalid entry for the month, please try and enter a valid month name')
            month = input('Which month? January, February, March, April, May, June, or all? Please type out the full month name. \n').lower()
        
    else:
        month = 'all'
        
        

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday','All']
    #filtering the user input to display the message regarding to the filter.
    if filter == 'day' or filter == 'both':
        day = input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all? Please type out the full day name. \n').title()
        # a while loop is used to handle invalid inputs
        while day not in days:
            print('Invalid entry for the day, please try and enter a valid day name')
            day = input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all? \n').title()
        
    else:
        day = 'all'
        
        
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int for each month
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all' and day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\n1) Here are some calculations to explore the most popular times of travel in this city: \n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = df['month'].mode()[0]
    print(f'The most common month is: {months[month-1]}')

    # display the most common day of week
    day = df['day_of_week'].mode()[0]
    print(f'The most common day of week is: {day}')

    # display the most popular start hour by extracting hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print(f'The most popular start hour is: {popular_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n2) Here are some calculations to explore the most popular stations and trip in this city: \n')
    start_time = time.time()

    # display the most popular used start station
    popular_start_station = df['Start Station'].mode()[0]
    print(f'The most popular start station is: {popular_start_station}')

    # display the most popular used end station
    popular_end_station = df['End Station'].mode()[0]
    print(f'\nThe most popular end station is: {popular_end_station}\n')

    # display the most frequent combination of start station and end station trip
    popular_trip = df['Start Station'] + ' to ' + df['End Station']
    print(' ************************ Here is a list for each trip occurred in this city with its count: ************************')
    print('popular trip' + '                                                            '+ 'count')
    print(f'\n{popular_trip.value_counts()}\n')
    print(f'According to the count, the most popular trip is occurred: from {popular_trip.mode()[0]}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
    
def trip_duration_stats(df):
    from datetime import timedelta as td
    """Displays statistics on the total and average trip duration.
    Total and average of trip duration is calculated in two ways:
    1) by using the provided 'Trip Duration' column
    2) by calculating the sum and the mean of the difference between the start time and the end time of the travel as a timedelta
    """

    print('\n3) Here are some calculations to explore the trip duration in this city: \n')
    start_time = time.time()
     
    
    # display total trip duration using 'trip duration' column
    total_trip_duration = df['Trip Duration'].sum()
    print(f'The total of trip duration is: {total_trip_duration}')

    # display total travel time based on the 'End Time' and 'Start Time' of the travel
    total_travel_duration = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).sum()
    days =  total_travel_duration.days
    hours = total_travel_duration.seconds // (3600)
    minutes = total_travel_duration.seconds % (3600) // 60
    seconds = total_travel_duration.seconds % (3600) % 60
    print(f'Total travel time is: {total_travel_duration} with {days} days {hours} hours {minutes} minutes {seconds} seconds')
    
    # display mean trip duration using 'trip duration' column
    avg_trip_duration = df['Trip Duration'].mean()
    print(f'The average of trip duration is: {avg_trip_duration}')

    # display mean travel time based on the 'End Time' and 'Start Time' of the travel
    average_travel_duration = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).mean()
    days =  average_travel_duration.days
    hours = average_travel_duration.seconds // (3600)
    minutes = average_travel_duration.seconds % (3600) // 60
    seconds = average_travel_duration.seconds % (3600) % 60
    print(f'Average travel time is: {average_travel_duration} with {days} days {hours} hours {minutes} minutes {seconds} seconds')
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
    
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\n4) Here are some statistics to get some insights about the bikeshare users in this city: \n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())
    print('\n\n')

    # Display counts of each gender
    if 'Gender' in(df.columns):
        print(df['Gender'].value_counts())
        print('\n\n')


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in(df.columns):
        print(f'The earliest year of birth is: {df["Birth Year"].min()}\nThe most recent year of birth is: {df["Birth Year"].max()}\nThe most comon year of birth is: {df["Birth Year"].mode()[0]}')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
    
    
def display_raw_data(df):
    """Ask the user if she/he wants to display the raw data and each time the user enters 'yes', 5 rows will de displayed"""
    raw_data = input('\nWould you like to display and explore the raw data for this city? If Yes: type out "yes", if No: type out "no". \n')
    if raw_data.lower() == 'yes':
        count = 0
        while True:
            print(df.iloc[count: count+5])
            count += 5
            ask = input('Would you like to display the next 5 rows of the raw data? if Yes: type out "yes", if No: type out "no". \n')
            if ask.lower() != 'yes':
                break
                
                
                
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? if Yes: type out "yes", if No: type out "no". \n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()