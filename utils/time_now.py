from datetime import datetime
from datetime import timedelta


def time_passed_since_current_time(minutes):
    """time_passed_since_current_time(int) -> returns time obj

       Returns the number of minutes that has elapsed between
       the current time and the passed in parameter minutes.
    """
    return time_now() - timedelta(minutes=minutes)


def time_now():
    """Returns the current time object"""
    return datetime.utcnow()

