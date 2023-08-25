"""Helper functions"""
from datetime import datetime, timedelta

def datetime_to_string(datetime_obj):
    """Converts a datetime object to zulu string.

    :param datetime_obj: a datetime object.
    :returns: a zulu formatted datetime string.
    """

    date_string = datetime.strftime(datetime_obj,'%Y-%m-%dT%H:%M:%SZ')
    return date_string

def datetime_to_playlist_name(datetime_obj):
    """Converts a datetime object to string in the format %b '%y (i.e. Jul '23)

    :param datetime_obj: a datetime object.
    :returns: a datetime string formatted as %b '%y (i.e. Jul '23)
    """

    date_string = datetime.strftime(datetime_obj,"%B '%y")
    return date_string

def string_to_datetime(datetime_string):
    """Converts a zulu string to a datetime object.

    :param datetime_string: a zulu formatted datetime string.
    :returns: a datetime object.
    """

    date_time = datetime.strptime(datetime_string,'%Y-%m-%dT%H:%M:%SZ')
    return date_time

def get_starting_date_from_user():
    """Gets the starting date from the user
    
    :returns: a datetime object X days back from today
    """
    correct_format = False
    days_str = input("How many days back should I check?")
    while not correct_format:
        try:
            days = int(days_str)
        except ValueError:
            days_str = input("Please type a number!")
        else:
            correct_format = True

    return datetime.now() - timedelta(days=days)
