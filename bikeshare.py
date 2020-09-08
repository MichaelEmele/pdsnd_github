import time
import pandas as pd
import numpy as np

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
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please select a city you want to look at. Choose between Chicago, New York City and Washington: \n").lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print("Sorry, it seems like you have chosen none of the available cities.")
            continue
        else:
            break
    
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nAt which month you want to look at?\nPlease choose between January, February, March, April, May, June or enter 'all' if you have no preference: ").lower()
        if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print("It seems like you have not selected a valid month.")
            continue
        else:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input ("\nAt which day you want to have a look?\nPlease choose a specific day or enter 'all' if you have no preference: ").lower()
        if day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            print ("Sorry but it seems like you have selected a non-existing day.")
            continue
        else:
            break

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

    # extract month, day of week and hour from Start Time to create new columns
   
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print("The most common month is: ", common_month)

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print("The most common day is: ", common_day)

    # TO DO: display the most common start hour
    common_hour = df['hour'].mode()[0]
    print("The most common hour is: ", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station is: ", common_start)

    # TO DO: display most commonly used end station
    common_end = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station is: ", common_end)

    # TO DO: display most frequent combination of start station and end station trip
    combination_station = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print('\nMost Commonly used combination of start station and end station:\n', combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel = sum(df['Trip Duration'])
    print("Total travel time in hours: ", total_travel/86400)

    # TO DO: display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("Mean travel time in minutes: ", mean_travel/60)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    try:
        user_types = df['User Type'].value_counts()
        print("User Types:\n", user_types)
    except KeyError:
        print("No 'User Type' data available.")
              
    # TO DO: Display counts of gender
    try:
        gender_types = df['Gender'].value_counts()
        print("\nGender:\n", gender_types)
    except KeyError:
        print("No 'Gender' data available.")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        oldest_user = df['Birth Year'].min()
        print("\nThe oldest user was born in: ", int(oldest_user))
    except KeyError:
        print("No 'Birth Year' data available.") 
    try:
        youngest_user = df['Birth Year'].max()
        print("The youngest user was born in: ", int(youngest_user))
    except KeyError:
        print("No 'Birth Year' data available.") 
    try:
        most_common_yob = df['Birth Year'].value_counts().idxmax()
        print("The most common year of birth is: ", int(most_common_yob))
    except KeyError:
        print("No 'Birth Year' data available.") 



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df):
    """Asks user whether he wants to see some lines of raw date from the chosen dataset.
    if yes function shows 5 lines and asks whether the user wants to see more. Continues asking unitl users answers 'no'
    """
    
    displayed_rows = 5
    rows_start = 0
    rows_end = displayed_rows - 1    # using index values for rows
    
   
    
    print("\nWould you like to see some lines of raw data from the current dataset of?")
    while True:
        raw_data = input('(y or n): ')
        if raw_data.lower() == 'y':
                    
            print('\n', df.iloc[rows_start : rows_end + 1])
            rows_start += displayed_rows
            rows_end += displayed_rows
            print('.'*120)
            print('\nWould you like to see the next {} rows?'.format(displayed_rows))
            continue
        else:
            break
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
            
if __name__ == "__main__":
	main()



