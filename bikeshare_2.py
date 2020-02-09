import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_time_stats(df)
        display_stations_stats(df)
        display_trip_duration_stats(df)
        display_user_stats(df)

        see_raw_data = input('\nWould you like to see the raw data? Enter yes or no.\n')
        if see_raw_data.lower() == 'yes':
            print_lines(df, 299998)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city = get_filter('city', ['Chicago', 'New York', 'Washington'])
    month = get_filter('month', ['all', 'January', 'February', 'March', 'April', 'May', 'June'])
    day = get_filter('day', ['all', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    return city, month, day


def get_filter(filter_name, filter_options):
    print('Select a {0} ({1}):'.format(filter_name, ', '.join(filter_options)))
    while True:
        entered_filter = input()
        if entered_filter.lower().strip(' ') in [option.lower() for option in filter_options]:
            print('-' * 40)
            selected_filter = entered_filter
            break
        else:
            print('The {0} you entered is not correct. '
                  'Remember, the options are {1}. Select one of them:'.format(filter_name, ', '.join(filter_options)))
    return selected_filter


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

    df = pd.read_csv(CITY_DATA.get(city.lower()))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    if month != 'all':
        df = df.loc[df['Start Time'].dt.month_name() == month.capitalize()]
    if day != 'all':
        df = df.loc[df['Start Time'].dt.day_name() == day.capitalize()]

    return df


def display_time_stats(data_frame):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        (dataframe) data_frame - Pandas DataFrame to analyze

    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_count_series = data_frame['Start Time'].dt.month_name().value_counts()
    print('Most common month: ', month_count_series.idxmax())

    # display the most common day of week
    day_count_series = data_frame['Start Time'].dt.day_name().value_counts()
    print('Most common day: ', day_count_series.idxmax())

    # display the most common start hour
    hour_count_series = data_frame['Start Time'].dt.hour.value_counts()
    print('Most common start hour: ', hour_count_series.idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print_separator()


def display_stations_stats(data_frame):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        (dataframe) data_frame - Pandas DataFrame to analyze

    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_count_series = data_frame['Start Station'].value_counts()
    print('Most common start station: ', start_station_count_series.idxmax())

    # display most commonly used end station
    end_station_count_series = data_frame['End Station'].value_counts()
    print('Most common end station: ', end_station_count_series.idxmax())

    # display most frequent combination of start station and end station trip
    data_frame['Start - End'] = data_frame['Start Station'] + ' -> ' + data_frame['End Station']
    start_to_end_station_trip_count_series = data_frame['Start - End'].value_counts()
    print('Most common trip (start -> end): ', start_to_end_station_trip_count_series.idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print_separator()


def display_trip_duration_stats(data_frame):
    """
    Displays statistics on the total and average trip duration.

    Args:
        (dataframe) data_frame - Pandas DataFrame to analyze

    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print('Total travel time: ', data_frame['Trip Duration'].sum())

    print('Mean travel time: ', data_frame['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print_separator()


def display_user_stats(data_frame):
    """
    Displays statistics on bikeshare users.

    Args:
        (dataframe) data_frame - Pandas DataFrame to analyze

    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('By user type:')
    print(data_frame['User Type'].value_counts())
    print('\n')

    # Display counts of gender
    if 'Gender' in data_frame.columns:
        print('By gender:')
        print(data_frame['Gender'].value_counts())
        print('\n')
    else:
        print('No gender stats available')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in data_frame.columns:
        df = data_frame.dropna(subset=['Birth Year'])
        unique_birth_years = df['Birth Year'].unique()
        print('Earliest birth year: ', np.sort(unique_birth_years)[0])
        print('Most recent birth year: ', np.sort(unique_birth_years)[-1])
        print('Most common birth year: ', df['Birth Year'].value_counts().idxmax())
    else:
        print('No birth year stats available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print_separator()


def print_lines(data_frame, number_of_lines_to_display):
    row_number, column_number = data_frame.shape
    loop_number = 1
    while True:
        number_of_start_line = calculate_number_of_start_line(loop_number, number_of_lines_to_display)
        number_of_end_line = calculate_number_of_end_line(loop_number, number_of_lines_to_display, row_number)
        display_lines(data_frame, number_of_end_line, number_of_start_line)
        want_to_see_more = input('\nWant to see more? Enter yes or no.\n')
        if want_to_see_more.lower() != 'yes':
            break
        elif number_of_end_line == row_number - 1:
            print('You have reached the end.')
            break
        else:
            loop_number += 1


def calculate_number_of_start_line(loop_number, number_of_lines_to_display):
    number_of_start_line = loop_number * number_of_lines_to_display - number_of_lines_to_display
    return number_of_start_line


def calculate_number_of_end_line(loop_number, number_of_lines_to_display, row_number):
    number_of_end_line = loop_number * number_of_lines_to_display
    if number_of_end_line > row_number - 1:
        number_of_end_line = row_number - 1
    return number_of_end_line


def display_lines(data_frame, number_of_end_line, number_of_start_line):
    print('Displaying lines {0} -> {1}'.format(number_of_start_line, number_of_end_line))
    print(data_frame[number_of_start_line:number_of_end_line])


def print_separator:
    print('-' * 40)


if __name__ == "__main__":
    main()
