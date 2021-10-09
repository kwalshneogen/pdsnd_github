import time
import pandas as pd
import numpy as np
import datetime


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Enter the name of a city: Chicago, New York City or Washington ').lower()
        if city in (CITY_DATA.keys()):
            print('You have chosen: ', city)
            break
        else:
            print('That is not a valid city.')

    # Get user input for month (all, january, february, ... , june)
    while True:
        month_inputs = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
        month = input('Enter the month you are interested in: january, february, march, april, may, june or all ').lower()
        if month in month_inputs:
            print('You have chosen: ', month)
            break
        else:
            print('That is not a valid month.')


    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_inputs = ['all','monday','tuesday','wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = input('Enter the day of the week you are interested in: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all ').lower()
        if day in day_inputs:
            print('You have chosen: ', day)
            break
        else:
            print('That is not a valid day.')

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

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
       months = ['january', 'february', 'march', 'april', 'may', 'june']
       month = months.index(month) + 1
       df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = df['month'].mode()[0]
    months = {1: 'January',
              2: 'February',
              3: 'March',
              4: 'Apil',
              5: 'May',
              6: 'June'}

    print('The most common month of bikeshare usage is ', months[common_month])

    # Display the most common day of week
    common_day = df['day_of_week'].mode()[0]

    print('The most common day of the week for bikeshare useage is ', common_day)
    # Display the most common start hour
    common_hour = df['hour'].mode()[0]

    print('The most common hour for bikeshare usage is ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_stat = df['Start Station'].mode()[0]
    print('The most commonly used Start Station is ', common_start_stat)

    # Display most commonly used end station
    common_end_stat = df['End Station'].mode()[0]
    print('The most commonly used End Station is ', common_end_stat)


    # Display most frequent combination of start station and end station trip
    station_comb = df['Start Station'] + df['End Station']
    freq_comb = station_comb.mode()[0]
    print('The most frequent combination of start station and end station is ', freq_comb)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    trip_duration = df['Trip Duration'].sum()
    print('The total travel time is {}'.format(str(datetime.timedelta(seconds=int(trip_duration)))))

    # TO DO: display mean travel time
    trip_mean = df['Trip Duration'].mean()
    print('The mean travel time is {}'.format(str(datetime.timedelta(seconds=int(trip_mean)))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The number of bikesare rides per user type is listed below.\n', user_types)

    # Display counts of gender
    try:
        gender_type = df['Gender'].value_counts()
        print('The number of bikesare rides per gender is listed below.\n', gender_type)

    except KeyError:
        print('There is no Gender data for the city Washington')


    # Display earliest, most recent, and most common year of birth
    try:
        earliest_YOB = df['Birth Year'].min().astype(int)
        latest_YOB = df['Birth Year'].max().astype(int)
        common_YOB = df['Birth Year'].mode()[0].astype(int)
        print('Year of Birth Stats\n The earliest YOB is {},\n'.format(earliest_YOB), 'The most recent YOB is {},\n'.format(latest_YOB), 'The most common YOB is {},\n'.format(common_YOB))
    except KeyError:
        print('There is no Birth Year data for the city Washington')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Gives user option to view raw data in 5 rows at a time"""
    display_row = 0
    raw_data = input("Would you like to see raw data, yes or no?").lower()
    pd.set_option('display.max_columns',200)

    while True:
        if raw_data == 'no':
            break

        elif raw_data == 'yes':
            print(df.iloc[display_row: display_row +5])
            display_row += 5
            raw_data = input('Would you list to see next 5 rows of raw data, yes or no?').lower()
        else:
            raw_data = input('Your input it invalid. Please enter yes or no').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
