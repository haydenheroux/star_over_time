import datetime

"""
Load file and store each line in a list
"""
def load_data(filename):
    lines = list()  # Create a new list to store the lines of the file
    with open(filename) as data_file:

        # Store each line of the file in the new list
        for line in data_file:
            lines.append(line)

    return lines


"""
Get row of data which has been cleaned by:
 - Getting row
 - Breaking into values by comma
 - Removing the header and newline
"""
def get_row(rows, row_index):
    # Get row from the list of rows
    row = rows[row_index]

    # Break into values by the comma
    values = row.split(',')

    # Remove the header from row
    values = values[1:]

    # Remove the newline in the last value
    values[-1] = values[-1].replace('\n', '')

    return values


"""
Create a pair with a date and a star
"""
def create_pair(date, star):
    date = date

    # Create a datetime.date object from the date if it has not been converted already
    if date is not None and isinstance(date, str):
        # Split date string by slashes
        units = date.split('/')

        # Assign units to their value
        year = int(units[2])
        month = int(units[0])
        day = int(units[1])

        # Create a new date object from these units
        date = datetime.date(year, month, day)

    star = int(star)
    return (date, star)


"""
Change all pairs from having a date to a weekday
"""
def convert_dates_to_weekdays(pairs):
    pairs_as_weekday = list()
    for index in range(len(pairs)):
        this_pair = pairs[index]

        # Convert the date to a weekday
        date = this_pair[0]
        date_as_weekday = date.weekday()

        # Create a duplicate pair but with a weekday instead of a date
        star = this_pair[1]
        pairs_as_weekday.append(create_pair(date_as_weekday, star))
    return pairs_as_weekday


"""
Compute the star differences for all data points """
def compute_star_differences(pairs):

    num_of_data_points = len(pairs)

    differences = list()
    for index in range(num_of_data_points):
        # Handle the special case for when there was no previous data point
        previous_value = create_pair(None, 0)
        if index >= 1:
            previous_value = pairs[index-1]
        this_pair = pairs[index]

        # Compute the star difference between the two data points
        previous_star = previous_value[1]
        this_star = this_pair[1]
        star_difference = this_star - previous_star

        # Get the date for this value
        this_date = this_pair[0]

        # Create a new pair representing the change in star on this date
        differences.append(create_pair(this_date, star_difference))

    return differences


def compute_largest_change_in_star(differences):

    num_of_data_points = len(differences)

    # There should never be a date with None, so if this appears there is an error!
    # There will always be a change in star larger than -1 since there are no negatives
    maximum_so_far = create_pair(None, -1)

    for index in range(1, num_of_data_points):

        this_pair = differences[index]

        this_star_difference = this_pair[1]
        maximum_star_difference = maximum_so_far[1]

        # Only update the maximum if the maximum star difference has been exceeded by a new data point
        if this_star_difference > maximum_star_difference:
            maximum_so_far = this_pair

    return maximum_so_far


def compute_total_differences_by_weekday(differences_as_weekday):
    weekday_totals = [0, 0, 0, 0, 0, 0, 0]
    for index in range(len(differences_as_weekday)):
        this_pair = differences_as_weekday[index]
        weekday = this_pair[0]
        star = this_pair[1]

        weekday_totals[weekday] += star
    return weekday_totals


"""
Convert a weekday integer (0-6) to the name of the weekday as a string.
"""
def weekday_to_string(weekday):
    if weekday == 0:
        return "Monday"
    elif weekday == 1:
        return "Tuesday"
    elif weekday == 2:
        return "Wednesday"
    elif weekday == 3:
        return "Thursday"
    elif weekday == 4:
        return "Friday"
    elif weekday == 5:
        return "Saturday"
    else:  # weekday == 6
        return "Sunday"


if __name__ == "__main__":
    rows = load_data("star_over_time.csv")

    dates = get_row(rows, 0)
    stars = get_row(rows, 1)

    # Create date and star pairs
    pairs = list()
    for index in range(len(dates)):
        date = dates[index]
        star = stars[index]
        pairs.append(create_pair(date, star))

    pairs_as_weekday = convert_dates_to_weekdays(pairs)

    # differences = compute_star_differences(pairs)
    differences_as_weekday = compute_star_differences(pairs_as_weekday)

    weekday_totals = compute_total_differences_by_weekday(differences_as_weekday)

    # Print the weekday totals
    # Note that the index is in the same range as the weekday (0-6)
    # In this case we can use the index as the weekday and vice versa
    print("=== WEEKDAY -> STARS GAINED  ===")
    for index in range(len(weekday_totals)):
        # Turn the weekday into a string so the user can understand the output
        weekday_str = weekday_to_string(index)
        # Get the total for that weekday
        total = weekday_totals[index]

        output = f"{weekday_str}: {total}"
        print(output)

    # Print the date with the largest change in star
    # print(compute_largest_change_in_star(differences))
    # print(compute_largest_change_in_star(differences_as_weekday))
