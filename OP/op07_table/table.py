"""Create table from the given string."""
import re


def create_table():
    """Create table."""


def normalize():
    """Add missing 0's to the minutes and remove extra 0's from hours and take offset into account."""


def get_formatted_time(time_list: list[tuple[int, int, int]]) -> list[str]:  # [(10, 53, 3)] -> ["10:53 AM"]
    """Format 24 hour time to the 12 hour time."""
    hours = time_list[0][0]
    minutes = time_list[0][1]
    if hours <= 12:
        return [str(hours) + ":" + str(minutes) + " AM"]
    else:
        return [str(hours - 12) + ":" + str(minutes) + " PM"]


def create_table_string(text: str) -> str:
    """
    Create table string from the given logs.

    There are a total of five categories you need to find the items for.
    Here are the rules for finding them:

    1. Time
    - Hour can be one or two characters long (1, 01, and 11)
    - Minute can be one or two characters long (2, 02, 22)
    - UTC offset ranges from -12 to 12
    - Times in the text are formatted in 24-hour time format (https://en.wikipedia.org/wiki/24-hour_clock)
    - Minimum time is 00:00 (0:00 and 0,00 and 00-0 are also valid)
    - Maximum time is 23:59
    - Hour and minute can be separated by any non-numeric character (01:11, 1.2, 6;5 and 1a4 are valid while 12345 is not)
    2. Username starts after "usr:" and contains letters, numbers and underscores ("_")
    3. Error code is a non-negative number up to 3 digits and comes after a case-insensitive form of "error "
    4. IPv4 address is good enough if it's a group of four 1- to 3-digit numbers separated by dots
    5. Endpoint starts with a slash ("/") and contains letters, numbers and "&/=?-_%"

    Each table row consists of a category name and items belonging to that category.
    Categories are named and ordered as follows: "time", "user", "error", "ipv4" and "endpoint".

    The category name and its items are separated by a vertical bar ("|").
    The length between the category name and separator is one whitespace (" ") for the longest category name in the table.
    The length between the separator and items is one whitespace.
    Items for each category are unique and are separated by a comma and a whitespace (", ") and must be sorted in ascending order.
    Times in the table are formatted in 12-hour time format (https://en.wikipedia.org/wiki/12-hour_clock), like "1:12 PM"
    and "12:00 AM".
    Times in the table should be displayed in UTC(https://et.wikipedia.org/wiki/UTC) time.
    If no items were found, return an empty string.
    """
    time = get_formatted_time(get_times(text))
    user = get_usernames(text)
    error = get_errors(text)
    ipv4 = get_addresses(text)
    endpoint = get_endpoints(text)
    data_dict = {
        "time": time,
        "user": user,
        "error": error,
        "ipv4": ipv4,
        "endpoint": endpoint
    }

    longest_name = max([len(k) for k, v in data_dict.items() if v], default=0)

    print(longest_name)


def check_time(text: str) -> list[bool]:
    result_bool_list = []
    pattern_times = r"\[[\S]+ [\S]+\]"
    times_list = re.findall(pattern_times, text)

    for time in times_list:
        pattern_hours = r"(?:\[)(\d{1,2})"
        hours_list = re.findall(pattern_hours, time)
        if hours_list and int(hours_list[0]) >= 24:
            hours_list = None

        pattern_minutes = r"(?:\[\d{1,2}\D)(\d{1,2})"
        minutes_list = re.findall(pattern_minutes, time)
        if minutes_list and int(minutes_list[0]) >= 60:
            minutes_list = None

        pattern_utc_offset = r"(?:UTC)([+-]\d{1,2})"
        utc_offset_list = re.findall(pattern_utc_offset, time)
        if utc_offset_list and not (-12 <= int(utc_offset_list[0]) <= 12):
            utc_offset_list = None

        if hours_list and minutes_list and utc_offset_list:
            result_bool_list.append(True)
        else:
            result_bool_list.append(False)

    return result_bool_list


def get_times(text: str) -> list[tuple[int, int, int]]:
    """
    Get times from text using the time pattern. No need to sort here.

    The result should be a list of tuples containing the time that's not normalized and UTC offset: (hours, minutes, utc_offset) in that order.

    :param text: text to search for the times
    :return: list of tuples containing the time and offset
    """
    pattern_hours = r"(?:\[)(\d{1,2})"
    hours_list = re.findall(pattern_hours, text)
    proper_time_list = check_time(text)
    print(proper_time_list)
    for proper_time in proper_time_list:
        if hours_list and proper_time:
            hours_list = [int(v) for v in hours_list if int(v) < 24]
            # print(hours_list)

        pattern_minutes = r"(?:\[\d{1,2}\D)(\d{1,2})"
        minutes_list = re.findall(pattern_minutes, text)
        if minutes_list and proper_time:
            minutes_list = [int(v) for v in minutes_list if int(v) < 60]
            # print(minutes_list)

        pattern_utc_offset = r"(?:UTC)([+-]\d{1,2})"
        utc_offset_list = re.findall(pattern_utc_offset, text)
        if utc_offset_list and proper_time:
            utc_offset_list = [int(v) for v in utc_offset_list if -12 <= int(v) <= 12]
            # print(utc_offset_list)

        min_list_len = min(len(hours_list), len(minutes_list), len(utc_offset_list))  # may be too complicated check, but it needed for inputs like: ("[14A3 UTC-4] [24:3 UTC-4]")) -> [(14, 3, -4)]

        result_list = []
        for i in range(min_list_len):
            result_list.append((hours_list[i], minutes_list[i], utc_offset_list[i]))
        # return result_list


def get_usernames(text: str) -> list[str]:
    """Get usernames from text. No need to sort here."""
    pattern_usr = r"(?:usr:)(\w+)"
    usr_list = re.findall(pattern_usr, text)
    return usr_list


def get_errors(text: str) -> list[int]:
    """Get errors from text. No need to sort here."""
    pattern_err = r"(?im)(?:error )(\d{1,3})"
    err_list = re.findall(pattern_err, text)
    err_list = [int(v) for v in err_list]
    return err_list


def get_addresses(text: str) -> list[str]:
    """Get IPv4 addresses from text. No need to sort here."""
    pattern_ip = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    ip_list = re.findall(pattern_ip, text)
    return ip_list


def get_endpoints(text: str) -> list[str]:
    """Get endpoints from text. No need to sort here."""
    pattern_endpoints = r"(/[\w\&/\=\?\-%]+)"
    endpoints_list = re.findall(pattern_endpoints, text)
    return endpoints_list


if __name__ == '__main__':
    logs = """
            [14?36 UTC+9] /tere eRRoR 418 192.168.0.255
            [8B48 UTC-6] usr:kasutaja
            """
    logs1 = """
            [24a48 UTC+0] 776.330.579.818
            [-1b35 UTC-4] errOR 741
            [02:53 UTC+5] usr:96NC9yqb /aA?Y4pK
            [5b05 UTC+5] ERrOr 700 268.495.856.225
            [24-09 UTC+10] usr:uJV5sf82_ eRrOR 844 715.545.485.989
            [04=54 UTC+3] eRROR 452
            [11=57 UTC-6] 15.822.272.473 error 9
            [15=53 UTC+7] /NBYFaC0 468.793.214.681
            [23-7 UTC+12] /1slr8I
            [07.46 UTC+4] usr:B3HIyLm 119.892.677.533
            
            [0:60 UTC+0] bad
            [0?0 UTC+0] ok
            [0.0 UTC+0] also ok
            [0.0 UTC-15] bad
            """
    # print(get_usernames(logs))  # -> [kasutaja]
    # print(get_errors(logs))  # -> [418]
    # print(get_addresses(logs))  # -> [192.168.0.255]
    # print(get_endpoints('/cfepechz /api/orders'))  # -> ['/cfepechz', '/api/orders']
    print(get_times(logs1))  # -> []
    # print(get_times("[10:53 UTC+3]"))  # -> [(10, 53, 3)]
    # print(get_times("[1:43 UTC+0]"))  # -> [(1, 43, 0)]
    # print(get_times("[14A3 UTC-4] [15:3 UTC-4]"))  # -> [(14, 3, -4), (15, 3, -4)]
    # print(get_times("[14A3 UTC-4] [24:3 UTC-4]"))  # -> [(14, 3, -4)]
    # print(get_times("[14A3 UTC-4] [23:66 UTC-4]"))  # -> [(14, 3, -4)]
    print(get_times("[25A3 UTC-10] [23:66 UTC-10]"))  # -> [] will not work, but I don't think that I need to test so complicated inputs for the task !!!!!!!!!!!!!!!!!!!!!!!

    # print(get_formatted_time(get_times("[20:53 UTC+3]")))
    # print(create_table_string(logs))
# time | 5:36 AM, 2:48 PM
# user | kasutaja
# error | 418
# ipv4 | 192.168.0.255
# endpoint | /tere
