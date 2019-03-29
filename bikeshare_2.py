import time
import datetime
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
    print('   __o')
    print(' _`\\<,_')
    print('(*)/ (*)   Hello! Let\'s explore some US bikeshare data!')
    print('-'*55)
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Specify a city to analyze (Chicago, New York or Washington): ").lower()
        if city not in ('chicago', 'new york', 'washington'):
            print("Not an appropriate city. Please try again.")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Specify a month to analyze (all, January, February, ... June): ").lower()
        if month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
            print("Not an appropriate month. Please try again.")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Specify a day of week to analyze (all, Monday, Tuesday, ... Sunday): ").lower()
        if day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            print("Not an appropriate day of week. Please try again.")
            continue
        else:
            break

    print('-'*55)
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
    # The month as January=1, December=12.
    df['month'] = df['Start Time'].dt.month
    # The day of the week with Monday=0, Sunday=6.
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df.month == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df.day_of_week == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    popular_month_int = df['month'].mode().values
    # use the index of the months list to get the corresponding month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    popular_month_str = []

    for i in range(len(popular_month_int)):
        value = popular_month_int[i]
        popular_month_str.append(months[value - 1])

    print('Most Popular Month:', popular_month_str)

    # display the most common day of week
    popular_day = df['day_of_week'].mode().values
    print('Most Popular Day of Week:', popular_day)

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most popular hour
    popular_hour = df['hour'].mode().values
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*55)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode().values
    print('Most Commonly Used Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode().values
    print('Most Commonly Used End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['Combination'] = df['Start Station'] + ' - ' + df['End Station']
    popular_combination = df['Combination'].mode().values
    print('Most Frequent Combination of Start and End Station:', popular_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*55)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', datetime.timedelta(seconds=int(total_travel_time)))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Average Trip Duration:', datetime.timedelta(seconds=int(mean_travel_time)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*55)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of user types:\n', user_types, sep='')

    # Display counts of gender
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        print('\nCounts of gender:\n', genders, sep='')
    else:
        print('\nGender data not available.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        recent_year = int(df['Birth Year'].max())
        common_year = df['Birth Year'].mode().apply(lambda x: int(x))
        print('\nOldest year of birth:', earliest_year)
        print('Youngest year of birth:', recent_year)
        print('Most common year of birth:', common_year.values)
    else:
        print('\nBirth year data not available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*55)

def display_raw_data(df):
    """Display 5 rows of data from the data set until the user answers no."""

    iloc = 0 # This is the first location we will display

    while True:
        raw_data = input('\nWould you like to view individual trip data? Enter yes or no.\n')

        if raw_data.lower() not in ('yes', 'no'):
            print("Sorry, I didn't understand your answer. Please try again.")
            continue
        elif raw_data.lower() != 'yes':
            break
        else:
            print(df[iloc:iloc+5])
            iloc +=5

def main():
    while True:
        city, month, day = get_filters()
        print('Filter', city, month, day, sep=' -> ')
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
