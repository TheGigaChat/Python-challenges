"""Create table from the given string."""
import re


def get_times(text: str) -> list[tuple[int, int, int]]:
    """
    Get times from text using a unified pattern that captures hours, minutes, and UTC offset together.

    :param text: text to search for the times
    :return: list of tuples containing the time and offset
    """
    # Unified regex pattern to capture hours, minutes, and UTC offset
    pattern_time = r"\[(0?\d|1\d|2[0-3])\D(0?\d|[1-5]\d) UTC([-+]\d[0-2]|[-+]\d)(?!\d)\]?"

    matches = re.findall(pattern_time, text)

    result_list = [(int(hours), int(minutes), int(utc_offset)) for hours, minutes, utc_offset in matches]

    return result_list


def get_formatted_time(time_list: list[tuple[int, int, int]]) -> list[str]:  # [(10, 53, 3)] -> ["7:53 AM"]
    """Format 24 hour time to the 12 hour time."""
    final_list = []
    # print(time_list)
    for i, time in enumerate(time_list):
        hours = time_list[i][0]
        minutes = time_list[i][1]
        utc_shift = time_list[i][2]

        hours = hours - abs(utc_shift)
        if hours < 0:
            hours += 24

        if hours == 0:
            final_list.append(f"{hours + 12:02}:{minutes:02} AM")
        elif hours < 12:
            final_list.append(f"{hours:01}:{minutes:02} AM")
        elif hours == 12:
            final_list.append(f"{hours:01}:{minutes:02} PM")
        else:
            final_list.append(f"{hours - 12:01}:{minutes:02} PM")
    # print(final_list)
    return final_list


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
    table = ""
    time = get_formatted_time(get_times(text))
    time.sort()
    user = get_usernames(text)
    user.sort()
    error = get_errors(text)
    error.sort()
    ipv4 = get_addresses(text)
    ipv4.sort()
    endpoint = get_endpoints(text)
    endpoint.sort()
    data_dict = {}

    if time:
        data_dict["time"] = time
    if user:
        data_dict["user"] = user
    if error:
        data_dict["error"] = error
    if ipv4:
        data_dict["ipv4"] = ipv4
    if endpoint:
        data_dict["endpoint"] = endpoint

    longest_name = max([len(k) for k, v in data_dict.items() if v], default=0)

    # print(data_dict)
    for k, value_list in data_dict.items():
        v = ""
        for value in value_list:
            if str(value) not in v:
                v += str(value) + ", "
        v = v[:-2]

        table += f"{k:<{longest_name + 1}}| {v}\n"

    # print(table)
    return table


if __name__ == '__main__':
    logs = """
            [14?36 UTC+9] /tere eRRoR 418 192.168.0.255
            [8B48 UTC-6] usr:kasutaja
            [02:53 UTC+5] usr:96NC9yqb /aA?Y4pK
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
    # print(get_times(logs1))  # -> []
    # print(get_times("[2.53 UTC+5] [2.53 UTC-5]"))  # -> [(10, 53, 3)]
    # print(get_times("[1:43 UTC+0]"))  # -> [(1, 43, 0)]
    # print(get_times("[14A3 UTC-4] [15:3 UTC-4]"))  # -> [(14, 3, -4), (15, 3, -4)]
    # print(get_times("[14A3 UTC-4] [24:3 UTC-4]"))  # -> [(14, 3, -4)]
    # print(get_times("[14A3 UTC-4] [23:66 UTC-4]"))  # -> [(14, 3, -4)]
    # print(get_times("[[15:03 UTC+0 [10:25 UTC+8"))  # -> []

    # print(get_formatted_time(get_times("[00:59 UTC+0 [11:0 UTC+0 [12:15 UTC+0 [00:00 UTC+0 [0:00 UTC+0")))
    # print(create_table_string("[15:03 UTC+0 [10:25 UTC+8"))