"""Airport schedule."""


def destinations_and_times(flights: list) -> dict:
    """
    Create a dictionary containing destinations with the departure times for this destination today.

    Flights in the list are in the format: "Tallinn,08:00,01h30m,OWL1234"
    Where different parts are separated by comma:
    - destination
    - departure time
    - flight duration
    - flight number

    Result format: {destination1: [time1, time2, ...], destination2: [time1, time2, ...]}.

    The order of departure times and destinations are not important.

    :param flights: given list from database.
    :return: dictionary where keys are destinations and values are lists of departure times.

    flights = [
    "Tallinn,08:00,01h30m,OWL1234",
    "Helsinki,10:35,01h00m,BHM5678",
    "Tallinn,09:00,01h30m,OWL1235",
    ]
    """
    result_dict = {}  # result_dict = {destination: time1, time2}
    for flight in flights:
        flight_data_list = flight.split(",")
        destination = flight_data_list[0]
        time = flight_data_list[1]
        result_dict[destination] = result_dict.get(destination, [])
        result_dict[destination].append(time)
    return result_dict


def sort_dict_values(flight_dict: dict) -> dict:
    """
    Sort flight_dict values in ascending order.

    This function should be applied to the previous function's result to get the departure times ordered.

    Return a flight_dict where all the values are in ascending order.
    The order of the keys is not important.
    """
    final_dict = {key: sorted(value) for key, value in flight_dict.items()}  # {'Tallinn': ['08:00', '06:00'], 'Helsinki': ['10:35']} => {'Tallinn': ['06:00', '08:00'], 'Helsinki': ['10:35']}
    return final_dict


def flights_to_destination(flights: list, destination: str) -> list:
    """
    Return flight times for the given destination.

    People want to know when flights for their chosen destination take off today.
    Using the functions written before, find and return the list of departure times
    (in ascending order) for that destination today.

    If there are no flights to the chosen destination, return empty list.

    :param flights: given list from database (the same as in destinations_and_times).
    :param destination: chosen destination for which we want to know the departure times.
    :return: list of departures (sorted in ascending order) for that destination.
    """
    destination_data_sorted = sort_dict_values(destinations_and_times(flights))  # ['08:00', '09:00']
    if destination in destination_data_sorted:
        return destination_data_sorted[destination]
    else:
        return []


def flights_schedule(flights: list) -> dict:
    """
    Return flight schedule by departure times.

    Create a dictionary containing the flight schedule for the day, where the keys are the departure times
    and the values are tuples which contain the destination and the flight number
    {time1: (destination, flight_number), time2: (destination, flight_number), ...}.

    The order of the keys (departure times) is not important.

    :param flights: given list from database (the same as in destinations_and_times).
    :return: dictionary where the keys are departure times and values are tuples containing the destination and
    flight number.
    """
    result_dict = {}  # result_dict = {time: (destination, flight_number)}  # {'08:00': ('Tallinn', 'OWL1234'), '10:35': ('Helsinki', 'BHM5678'), '09:00': ('Tallinn', 'OWL1235')}
    for flight in flights:
        flight_data_list = flight.split(",")
        destination = flight_data_list[0]
        time = flight_data_list[1]
        flight_number = flight_data_list[3]

        result_dict[time] = (destination, flight_number)
    return result_dict


def destinations_list(schedule: dict) -> list:
    """
    Return a list of unique destinations for the day from the given flight schedule, sorted alphabetically.

    :param schedule: Dictionary containing the flight schedule (the result of flights_schedule function).
    :return: Alphabetically sorted list of unique destinations.
    """
    set_of_unique_destinations = set()
    for time, data in schedule.items():
        destination = data[0]
        set_of_unique_destinations.add(destination)
    destinations_sorted_list = sorted(list(set_of_unique_destinations))  # ['Helsinki', 'Tallinn']
    return destinations_sorted_list


def airlines_operating_today(schedule: dict, airline_names: dict) -> set:
    """
    Return a set of unique airline names that have flights operating today.

    Schedule is the result of the flights_schedule function.
    Airline names are presented as a dictionary where the key is the airline code
    and the value is the corresponding airline name.

    Flight code contains 3 letters and 4 numbers. The 3-letter code indicates the airline code.
    So, the 3-letter code should be taken from the airline_names dictionary (key).

    :param schedule: Dictionary containing the flight schedule (the result of flights_schedule function).
    :param airline_names: Dictionary containing airline codes and corresponding names.
    :return: Set of unique airline names operating today.
    """
    set_of_unique_airline_names = set()  # {'Owlbear Airlines', "Beholder's Majesty Airlines"}
    for time, data in schedule.items():
        flight_number = data[1]  # WOF9393
        airline_code = flight_number[:3]  # WOF
        set_of_unique_airline_names.add(airline_names[airline_code])
    return set_of_unique_airline_names


def destinations_by_airline(schedule: dict, airline_names: dict) -> dict:
    """
    Return a dictionary of destinations by airline names.

    Returns a dictionary where the keys are airline names and the values are sets of unique destinations
    that the airline is flying to today.

    Airline names is in the same format as in airlines_operating_today.
    The 3-letter code from the flight number can be used to find the airline name.

    :param schedule: Dictionary containing the flight schedule (the result of flights_schedule function).
    :param airline_names: Dictionary containing mapping of airline codes to airline names.
    :return: Dictionary of airline names to sets of destinations.
    """
    result_dict = {}  # {'Owlbear Airlines': {'Tallinn', 'Berlin'}, "Beholder's Majesty Airlines": {'Helsinki'}}
    for time, data in schedule.items():
        destination = data[0]
        flight_number = data[1]
        airline_code = flight_number[:3]
        airline_name = airline_names[airline_code]
        result_dict[airline_name] = result_dict.get(airline_name, set())
        result_dict[airline_name].add(destination)
    return result_dict


if __name__ == '__main__':
    flights = [
        "Tallinn,08:00,01h30m,OWL1234",
        "Helsinki,10:35,01h00m,BHM5678",
        "Tallinn,09:00,01h30m,OWL1235",
    ]

    print(destinations_and_times(flights))
    # {'Tallinn': ['08:00', '09:00'], 'Helsinki': ['10:35']}

    flights_dict = {'Tallinn': ['10:00', '09:00'], 'Helsinki': ['10:35']}
    # print(sort_dict_values(flights_dict))
    # {'Tallinn': ['09:00', '10:00'], 'Helsinki': ['10:35']}

    # print(flights_to_destination(flights, "Tallinn"))
    # ['08:00', '09:00']

    # print(flights_schedule(flights))
    # {'08:00': ('Tallinn', 'OWL1234'), '10:35': ('Helsinki', 'BHM5678'), '09:00': ('Tallinn', 'OWL1235')}

    schedule = {'08:00': ('Tallinn', 'OWL1234'), '10:35': ('Helsinki', 'BHM5678'), '09:00': ('Tallinn', 'OWL1235'), '10:00': ('Berlin', 'OWL1234')}
    # print(destinations_list({}))
    # print(destinations_list(schedule))
    # ['Helsinki', 'Tallinn']

    airlines = {"OWL": "Owlbear Airlines", "BHM": "Beholder's Majesty Airlines", "HPL": "Huston People Light"}

    # print(airlines_operating_today(schedule, airlines))
    # {'Owlbear Airlines', "Beholder's Majesty Airlines"}

    # print(destinations_by_airline(schedule, airlines))
    # {'Owlbear Airlines': {'Tallinn'}, "Beholder's Majesty Airlines": {'Helsinki'}}
