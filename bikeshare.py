import time
import pandas as pd
import numpy as np
import calendar as cal
import json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january','february','march', 'april', 'may','june','none']

DAYS = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','none']

LINE_BREAK = '-'*40

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    prompt = "Would you like to city data for Chicago, New York or Washington? \n"
    invalid_input_prompt = "Invalid city name. Please enter Chicago, New York or Washington only \n"

    city = validate_input(prompt, invalid_input_prompt,CITY_DATA)
                
    # get user input for month (all, january, february, ... , june) and add while loop
    prompt = "Which month would you like to filter the data by. Enter January, February, March, April, May or June . Enter none for no filter \n"
    invalid_input_prompt = "Invalid month. Please enter January, February, March, April, May or June . Enter none for no filter \n"
    
    month = validate_input(prompt, invalid_input_prompt,MONTHS)
     
    # get user input for day of week (all, monday, tuesday, ... sunday)
    prompt = "Which day would you like to filter data by .Please enter Sunday, Monday, Tuesday, Wednesday, Thursday, Friday or Saturday . Enter none for no filter \n"
    invalid_input_prompt = "Invalid day. Please enter Sunday, Monday, Tuesday, Wednesday, Thursday, Friday or Saturday . Enter none for no filter \n"
    
    day = validate_input(prompt, invalid_input_prompt, DAYS)
    
    return city, month, day

def validate_input(prompt, invalid_input_prompt, valid_inputs):
    """
    validates input(city, month, day) entered by the user till it is valid

    Args:
        (str) prompt - message to prompt user to enter which data - city, month or day
        (str) invalid_input_prompt - message to show upon wrong input
        (str) valid_inputs - list or dictionary of correct values to check the input entered
    Returns:
        (str) entry - input that is valid 
    """
    
    accepted_input_str = " Filtering by : {}. "
    error_message = "Invalid input \n"
    entry = input(prompt).lower()
    while True:
        try:            
            if entry not in valid_inputs:
                entry = input(invalid_input_prompt).lower()
                continue
            else:
                print(accepted_input_str.format(entry))
                break
        except:
            print(error_message)
    return entry
    

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
    # get filename from city and CITY_DATA dictionary
    filename = CITY_DATA[city]
    
    # load data file into data frame
    df = pd.read_csv(filename)
    
    none = 'none'
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filter by month if applicable
    if month != none:
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    
    # filter by day of week if applicable
    if day != none:
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df

def show_most_popular(entity,value,frequency):
    print("Most popular {} is {} occurring {} number of times.".format(entity,value,frequency))

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].value_counts().idxmax()
    popular_month_name = cal.month_name[popular_month]
    popular_month_count = len(df[df['month'] == popular_month])
    show_most_popular("month",popular_month_name, popular_month_count)
    

    # display the most common day of week
    popular_dow = df['day_of_week'].value_counts().idxmax()
    popular_dow_count = len(df[df['day_of_week'] == popular_dow])
    show_most_popular("day of the week",popular_dow, popular_dow_count)

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].value_counts().idxmax()   
    popular_hour_count = len(df[df['hour'] == popular_hour])
    show_most_popular("hour",popular_hour, popular_hour_count)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print(LINE_BREAK)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()
    start_station_count = len(df[df['Start Station'] == popular_start_station])
    show_most_popular("start station",popular_start_station, start_station_count)

    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()
    end_station_count = len(df[df['End Station'] == popular_end_station])
    show_most_popular("end station",popular_end_station, end_station_count)

    # display most frequent combination of start station and end station trip
    df['route'] = df['Start Station']+" to " + df['End Station']
    popular_route = df['route'].value_counts().idxmax()
    route_count = len(df[df['route'] == popular_route])
    show_most_popular("route",popular_route, route_count)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(LINE_BREAK)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time_hours = df['Trip Duration'].sum() / 3600
    print("Total travel time is {} hour(s)".format(total_travel_time_hours))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Average travel time is {} second(s)".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(LINE_BREAK)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    gender_str = "Gender"
    birth_year_Str = 'Birth Year'
    
    # Display counts of user types
    user_data = df['User Type'].value_counts().to_string()
    print(" User types and their frequencies : \n {} \n".format(user_data))

    # Display counts of gender
    if gender_str in df:
        gender_data = df[gender_str].value_counts().to_string()
        print("Gender and their frequencies : \n {} \n".format(gender_data))
    else:
        print("No gender data available")

    # Display earliest, most recent, and most common year of birth
    if birth_year_Str in df:
        
        earliest_birth_year = df[birth_year_Str].min()
        print("Earliest Birth Year is {}.\n".format(earliest_birth_year))
        
        recent_birth_year = df[birth_year_Str].max()
        print("Most recent Birth Year is {}.\n".format(recent_birth_year))
        
        common_year = df[birth_year_Str].value_counts().idxmax()
        common_year_count = len(df[df[birth_year_Str] == common_year])
        print("Most common birth year is {} occurring {} number of times.\n".format(common_year,common_year_count))
        
    else:
        print("No birth year data present")
        

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(LINE_BREAK)
    
def print_chunks(df, position, size):
    """ Print certain number of rows of the data frame from a specific position
        INPUT:
         df - data frame to print rows from
         position - first row number to print
         size - number of rows to be printed
    """
    for i in range(position, position+size):
        if i < len(df):
            df_json = df.iloc[i].to_json(orient='index')
            parsed = json.loads(df_json)
            print(json.dumps(parsed, indent=1))
    
def show_raw_data(df):
    """ Prompts user to show raw data
    """
   

    show_raw = input('\nWould you like to view raw data? Enter yes or no.\n').lower()
    if show_raw == 'no':
        return
    elif show_raw == 'yes':
        position = 0
        size = 5
        print_chunks(df, position, size)
            
        while True:
            show_raw = input("Would you like to see 5 more records? Enter yes or no. \n: ").lower()
            if show_raw == "yes":
                # Display 5 more lines
                position += 5
                print_chunks(df, position, size)
            elif show_raw == "no":
                return
            else:
                print("Invalid answer")
    return
    

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
