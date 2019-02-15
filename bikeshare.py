import time
import pandas as pd
import numpy as np
import re

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}
          #'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12}

MONTHS_NAMES = {1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june'}
                #7: 'july', 8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'}

DAYS_OF_WEEK = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    #Regular expression to get rid of everyting excep from alphanumerical symbols from input
    #regex = re.compile('[^a-zA-Z]')
    regex = re.compile('[^a-z\s]')
    
    #Initialise input variables with blank string
    city = ''
    month = ''
    day = ''
    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    #Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs    
    while city not in CITY_DATA:
        print('Please enter city (Chicago, New York City or Washington): ')
        city = input().lower()
        city = regex.sub('', city)

    #Get user input for month (all, january, february, ... , june)
    while not ((month in MONTHS) or (month == 'all')):
        print('Please enter month to filter data, or "all" to continue without filtering by month: ')
        month = input().lower()
        month = regex.sub('', month)

    #Get user input for day of week (all, monday, tuesday, ... sunday)
    while not ((day in DAYS_OF_WEEK) or (day == 'all')):
        print('Please enter day of week to filter data, or "all" to continue without filtering by day of week: ')
        day = input().lower()
        day = regex.sub('', day)

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
    df = pd.read_csv(CITY_DATA[city])
    
    #Convert strings to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    #Add extra columns for month and day of week
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name
    
    #Filter by month if necessary
    if month in MONTHS:
        df = df[df['month'] == MONTHS[month]]
    
    #Filter by day of week if necessary
    if day in DAYS_OF_WEEK:
        df = df[df['day'] == day.title()]
        
    #print(df.head())    
    
    user_input = ''
    print('Do you want to see the sample of the data (yes/no)?')
    user_input = input().lower()
    step = 5
    position = 0
    while user_input != 'no':
          print(df[position:position+step])
          print('Do you want to see more of the sample (yes/no)?')
          user_input = input().lower()
          position += step
        
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Display the most common month
    most_common_month = df['month'].mode()[0]
    print('The most common month is {}'.format(MONTHS_NAMES[most_common_month].title()))

    #Display the most common day of week
    most_common_day = df['day'].mode()[0]
    print('The most common day is {}'.format(most_common_day))

    #Display the most common start hour
    most_common_start_hour = df['Start Time'].dt.hour.mode()[0]
    print('The most common start hour is {}'.format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Display most commonly used start station
    print('The most commonly used start station is {}'.format(df['Start Station'].mode()[0]))

    #Display most commonly used end station
    print('The most commonly used end station is {}'.format(df['End Station'].mode()[0]))

    #Display most frequent combination of start station and end station trip
    comb = df.groupby(['Start Station', 'End Station'])['Start Station', 'End Station'].agg({'count': len}).sort_values('count', ascending=False)
    print('The most frequent combination of start station and end station: ')
    print(comb[0:1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Display total travel time
    print('Total travel time is {}'.format((df['End Time'] - df['Start Time']).sum()))

    #Display mean travel time
    print('Mean travel time is {}'.format((df['End Time'] - df['Start Time']).mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    if 'User Type' in df:
        print('User type statistic:')
        print(df["User Type"].value_counts())

    #Display counts of gender
    if 'Gender' in df:
        print('Gender statistic:')
        print(df["Gender"].value_counts())

    #Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print('The earliest year of birth: {:d}'.format(earliest_birth_year))
        print('The most recent year of birth: {:d}'.format(most_recent_birth_year))
        print('The most common year of birth: {:d}'.format(most_common_birth_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
