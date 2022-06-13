import time

USER_PRIORITY_WEIGHT = 10000
CHECKED_COUNTER_WEIGHT = 3
HOURS_LEFT_WEIGHT = 1
ONE_SECOND_IN_MILLIS = 1000
ONE_HOUR_IN_MILLIS = 3600000

def calculate_weighted_priority(user_priority, times_checked, event_date_timestamp):
    current_timestamp = time.time() * ONE_SECOND_IN_MILLIS
    if (current_timestamp > event_date_timestamp):
        return (user_priority - 1) * USER_PRIORITY_WEIGHT
    else:
        user_priority_weight = user_priority * USER_PRIORITY_WEIGHT
        times_checked_weight = times_checked * CHECKED_COUNTER_WEIGHT
        time_left_weight = (event_date_timestamp - current_timestamp) // ONE_HOUR_IN_MILLIS
        return user_priority_weight - times_checked_weight - time_left_weight