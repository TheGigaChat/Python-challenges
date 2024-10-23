"""Flightpath."""


def update_delayed_flight(schedule: dict[str, tuple[str, str]], delayed_flight_number: str, new_departure_time: str) -> \
        dict[str, tuple[str, str]]:
    """
    Update the departure time of a delayed flight in the flight schedule.

    Return a dictionary where the departure time of the specified flight is modified.
    This means that the result dictionary should not contain the old time,
    instead a new departure time points to the specified flight.
    The input schedule cannot be changed.

    :param schedule: Dictionary of flights ({time string: (destination, flight number)})
    :param delayed_flight_number: Flight number of the delayed flight
    :param new_departure_time: New departure time for the delayed flight
    :return: Updated flight schedule with the delayed flight's departure time changed
    """
    new_schedule = {}  # {'06:15': ('Tallinn', 'OWL6754'), '11:35': ('Helsinki', 'BHM2345')} => {'09:00': ('Tallinn', 'OWL6754'), '11:35': ('Helsinki', 'BHM2345')}
    for key, value in schedule.items():
        if delayed_flight_number in value:
            key = new_departure_time
            new_schedule[key] = value
        else:
            new_schedule[key] = value
    return new_schedule


def cancel_flight(schedule: dict[str, tuple[str, str]], cancelled_flight_number: str) -> dict[str, tuple[str, str]]:
    """
    Create a new schedule where the specified flight is cancelled.

    The function cannot modify the existing schedule parameter.
    Instead, create a new dictionary where the cancelled flight is not added.

    :param schedule: Dictionary of flights ({time: (destination, flight number)})
    :param cancelled_flight_number: Flight number of the cancelled flight
    :return: New flight schedule with the cancelled flight removed
    """
    new_schedule = {k: v for k, v in schedule.items() if cancelled_flight_number not in v}  # {'06:15': ('Tallinn', 'OWL6754'), '11:35': ('Helsinki', 'BHM2345')} => {'11:35': ('Helsinki', 'BHM2345')}
    return new_schedule


def busiest_time(schedule: dict[str, tuple[str, str]]) -> list[str]:
    """
    Find the busiest hour(s) at the airport based on the flight schedule.

    The busiest hour(s) is/are determined by counting the number of flights departing in each hour of the day.
    All flights departing with the same hour in their departure time, are counted into the same hour.

    The function returns a list of strings of the busiest hours, sorted in ascending order, such as ["08", "21"].

    :param schedule: Dictionary containing the flight schedule, where keys are departure times
                     in the format "HH:mm" and values are tuples containing destination and flight number.
    :return: List of strings representing the busiest hour(s) in 24-hour format, such as ["08", "21"].
    """
    times_list = [k[:2] for k in schedule.keys()]  # ['04', '06', '06', '07', '08', '11', '11', '19', '20', '22']
    frequency_table = {}  # {'04': 1, '06': 2, '07': 1, '08': 1, '11': 2, '19': 1, '20': 1, '22': 1}
    for time in times_list:
        frequency_table[time] = frequency_table.get(time, 0) + 1

    maximum_frequency = max(frequency_table.values())
    busiest_time_list = [k for k, v in frequency_table.items() if v == maximum_frequency]  # {'04:35': ('Maardu', 'MWL6754'), '06:15': ('Tallinn', 'OWL6754'), '06:30': ('Paris', 'OWL6751')} => ["06"]
    return busiest_time_list


def connecting_flights(schedule: dict[str, tuple[str, str]], arrival: tuple[str, str]) -> list[tuple[str, str]]:
    """
    Find connecting flights based on the provided arrival information and flight schedule.

    The function takes a flight schedule and the arrival time and location of a flight,
    and returns a list of available connecting flights. A connecting flight is considered
    available if its departure time is at least 45 minutes after the arrival time, but less
    than 4 hours after the arrival time. Additionally, a connecting flight must not go back
    to the same place the arriving flight came from.

    :param schedule: Dictionary containing the flight schedule, where keys are departure
                     times in the format "HH:mm" and values are tuples containing
                     destination and flight number. For example:
                     {
                         "14:00": ("Paris", "FL123"),
                         "15:00": ("Berlin", "FL456")
                     }

    :param arrival: Tuple containing the arrival time and the location the flight is
                    arriving from. For example:
                    ("11:05", "Tallinn")

    :return: A list of tuples containing the departure time and destination of the
             available connecting flights, sorted by departure time. For example:
             [
                 ("14:00", "Paris"),
                 ("15:00", "Berlin")
             ]
             If no connecting flights are available, the function returns an empty list.
    """
    result_list = []  # {'04:35': ('Maardu', 'MWL6754'), '06:15': ('Tallinn', 'OWL6754'), '06:30': ('Paris', 'OWL6751'), '07:29': ('London', 'OWL6756'), '08:00': ('New York', 'OWL6759')}, ('04:00', 'Tallinn') => [('06:30', 'Paris'), ('07:29', 'London')]

    for time, value in schedule.items():
        destination = value[0]
        hours = int(time[:2])
        minute = int(time[3:])
        time_in_minutes = minute + hours * 60

        arrival_destination = arrival[1]
        arrival_hours = int(arrival[0][:2])
        arrival_minutes = int(arrival[0][3:])
        arrival_time_in_minutes = arrival_minutes + arrival_hours * 60

        if destination != arrival_destination:
            delta_minutes = time_in_minutes - arrival_time_in_minutes
            if 45 <= delta_minutes < 60 * 4:
                result_list.append((time, destination))
    return result_list


def busiest_hour(schedule: dict[str, tuple[str, str]]) -> list[str]:
    """
    Find the busiest hour-long slot(s) in the schedule.

    One hour slot duration is 60 minutes (or the diff of two times is less than 60).
    So, 15:00 and 16:00 are not in the same slot.

    :param schedule: Dictionary containing the flight schedule, where keys are departure
                     times in the format "HH:mm" and values are tuples containing
                     destination and flight number. For example:
                     {
                         "14:00": ("Paris", "FL123"),
                         "15:00": ("Berlin", "FL456")
                     }

    :return: A list of strings representing the starting time(s) of the busiest hour-long
             slot(s) in ascending order. For example:
             ["08:00", "15:20"]
             If the schedule is empty, returns an empty list.
    """
    frequency_table = {}  # {'04:35': 1, '06:15': 2, '06:30': 2, '07:29': 2, '08:00': 1, '11:30': 2, '11:35': 1, '19:35': 1, '20:35': 1, '22:35': 1}
    for time in schedule.keys():
        hours = int(time[:2])
        minutes = int(time[3:])
        minutes += hours * 60

        for time_again in schedule.keys():
            hours_again = int(time_again[:2])
            minutes_again = int(time_again[3:])
            minutes_again += hours_again * 60
            if minutes <= minutes_again < minutes + 60:
                frequency_table[time] = frequency_table.get(time, 0) + 1

    result_list = [k for k, v in frequency_table.items() if v == max(frequency_table.values())]  # ['06:15', '06:30', '07:29', '11:30']
    return result_list


def most_popular_destination(schedule: dict[str, tuple[str, str]], passenger_count: dict[str, int]) -> str:
    """
    Find the destination where the most passengers are going.

    :param schedule: A dictionary representing the flight schedule.
                     The keys are departure times and the values are tuples
                     containing destination and flight number.
    :param passenger_count: A dictionary with flight numbers as keys and
                            the number of passengers as values.
    :return: A string representing the most popular destination.
    """
    frequency_table = {}
    for time, destination_and_flight_code in schedule.items():
        destination = destination_and_flight_code[0]
        flight_code = destination_and_flight_code[1]
        passenger_num = passenger_count[flight_code]
        frequency_table[destination] = frequency_table.get(destination, 0) + passenger_num

    max_passenger_amount = max(frequency_table, key=frequency_table.get)
    return max_passenger_amount


def least_popular_destination(schedule: dict[str, tuple[str, str]], passenger_count: dict[str, int]) -> str:
    """
    Find the destination where the fewest passengers are going.

    :param schedule: A dictionary representing the flight schedule.
                     The keys are departure times and the values are tuples
                     containing destination and flight number.
    :param passenger_count: A dictionary with flight numbers as keys and
                            the number of passengers as values.
    :return: A string representing the least popular destination.
    """
    frequency_table = {}
    for time, destination_and_flight_code in schedule.items():
        destination = destination_and_flight_code[0]
        flight_code = destination_and_flight_code[1]
        passenger_num = passenger_count[flight_code]
        frequency_table[destination] = frequency_table.get(destination, 0) + passenger_num

    min_passenger_amount = min(frequency_table, key=frequency_table.get)
    return min_passenger_amount


if __name__ == '__main__':
    flight_schedule = {
        "06:15": ("Tallinn", "OWL6754"),
        "11:35": ("Helsinki", "BHM2345")
    }
    # new_flight_schedule = update_delayed_flight(flight_schedule, "OWL6754", "09:00")
    # print(flight_schedule)
    # # {'06:15': ('Tallinn', 'OWL6754'), '11:35': ('Helsinki', 'BHM2345')}
    # print(new_flight_schedule)
    # {'09:00': ('Tallinn', 'OWL6754'), '11:35': ('Helsinki', 'BHM2345')}

    # new_flight_schedule = cancel_flight(flight_schedule, "OWL6754")
    # print(flight_schedule)
    # # {'06:15': ('Tallinn', 'OWL6754'), '11:35': ('Helsinki', 'BHM2345')}
    # print(new_flight_schedule)
    # # {'11:35': ('Helsinki', 'BHM2345')}

    flight_schedule = {
        "04:35": ("Maardu", "MWL6754"),
        "06:15": ("Tallinn", "OWL6754"),
        "06:30": ("Paris", "OWL6751"),
        "07:29": ("London", "OWL6756"),
        "08:00": ("New York", "OWL6759"),
        "11:30": ("Tokyo", "OWL6752"),
        "11:35": ("Helsinki", "BHM2345"),
        "19:35": ("Paris", "BHM2346"),
        "20:35": ("Helsinki", "BHM2347"),
        "22:35": ("Tallinn", "TLN1001"),
    }
    # print(busiest_time()
    # print(busiest_time(flight_schedule))
    # ['06', '11']

    # print(connecting_flights(flight_schedule, ("04:00", "Tallinn")))
    # [('06:30', 'Paris'), ('07:29', 'London')]
    # print(connecting_flights(flight_schedule, ("23:34", "Tallinn")))
    # []

    print(busiest_hour(flight_schedule))
    # ['06:15', '06:30', '07:29', '11:30']
    # 19:35 does not match because 20:35 is not in the same slot

    # flight number: number of passengers
    passenger_counts = {
        "MWL6754": 100,
        "OWL6754": 85,
        "OWL6751": 103,
        "OWL6756": 87,
        "OWL6759": 118,
        "OWL6752": 90,
        "BHM2345": 111,
        "BHM2346": 102,
        "BHM2347": 94,
        "TLN1001": 1
    }
    # print(most_popular_destination(flight_schedule, passenger_counts))
    # # Paris
    #
    # print(least_popular_destination(flight_schedule, passenger_counts))
    # # Tallinn
