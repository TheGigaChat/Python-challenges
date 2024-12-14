"""Vehicle rental. Project III."""
import enum


class Type(enum.Enum):
    """
    Type of vehicle.

    DO NOT CHANGE.
    """

    SPORTSCAR = 'SPORTSCAR'
    CONVERTIBLE = 'CONVERTIBLE'
    VAN = 'VAN'
    OTHER = 'OTHER'


def get_price(vehicle) -> int:
    """
    Return the price of the vehicle based on its type.

    :param vehicle: A vehicle object (either Car or Motorcycle) with type.

    Motorcycle - 100

    OTHER - 50
    VAN - 100
    CONVERTIBLE - 150
    SPORTSCAR - 200

    :return: Price of the vehicle based on its type.
    """
    if isinstance(vehicle, Motorcycle):
        return 100
    elif isinstance(vehicle, Car):
        if vehicle.type_of_car == Type.OTHER:
            return 50
        elif vehicle.type_of_car == Type.CONVERTIBLE:
            return 150
        elif vehicle.type_of_car == Type.VAN:
            return 100
        elif vehicle.type_of_car == Type.SPORTSCAR:
            return 200
    return 0


class Car:
    """Car class representing a vehicle of type Car."""

    def __init__(self, make: str, model: str, year: int, type_of_car: Type) -> None:
        """
        Construct new car.

        :param make: Manufacturer of the car.
        :param model: Model of the car.
        :param year: Year the car was manufactured.
        :param type_of_car: Type of the car (an instance of Type enum).
        :raises ValueError: If type_of_car is not an instance of Type enum.
        """
        self.make = make
        self.model = model
        self.year = year
        self.type_of_car = None
        if type_of_car and isinstance(type_of_car, Type):
            self.type_of_car = type_of_car
        else:
            raise ValueError('Type of car cannot be None.')

        self.price = get_price(self)
        self.times_rented = 0

    def __repr__(self) -> str:
        """
        Return string representation of car.

        return: 'Car(make, model, year, type_of_car)'
        """
        return f"Car({self.make}, {self.model}, {self.year}, {self.type_of_car})"

    def __hash__(self) -> int:
        """
        Return hash representation of car.

        return: hash(make, model, year, type_of_car)
        """
        return hash((self.make, self.model, self.year, self.type_of_car))

    def __eq__(self, other):
        """Check equality based on make, model, year, and type_of_car."""
        if isinstance(other, Car):
            return (self.make, self.model, self.year, self.type_of_car) == \
                (other.make, other.model, other.year, other.type_of_car)
        return False

    def get_price(self) -> int:
        """:return: price of the vehicle."""
        return self.price


class Motorcycle:
    """Motorcycle."""

    def __init__(self, make: str, model: str, year: int) -> None:
        """
        Construct new motorcycle.

        :param make: Manufacturer of the motorcycle.
        :param model: Model of the motorcycle.
        :param year: Year the motorcycle was manufactured.
        """
        self.make = make
        self.model = model
        self.year = year
        self.price = get_price(self)
        self.times_rented = 0

    def __repr__(self) -> str:
        """
        Return tring representation of Motorcycle.

        return: 'Motorcycle(make, model, year)'
        """
        return f"Motorcycle({self.make}, {self.model}, {self.year})"

    def __hash__(self) -> int:
        """
        Hash representation of Motorcycle.

        return: hash(make, model, year)
        """
        return hash((self.make, self.model, self.year))

    def __eq__(self, other):
        """Check equality based on make, model, and year."""
        if isinstance(other, Motorcycle):
            return (self.make, self.model, self.year) == \
                (other.make, other.model, other.year)
        return False

    def get_price(self) -> int:
        """:return: price of the vehicle."""
        return self.price


class Client:
    """Client class representing a client of the rental service."""

    def __init__(self, name: str, budget: int = 0) -> None:
        """
        Construct new Client.

        :param name: The name of the client.
        :param budget: The initial budget for the client.
        bookings: A list of vehicles that the client has booked.
        """
        self.name = name
        self.budget = budget
        self.costs = 0
        self.cars_booked = []

    def get_pure_balance(self):
        """Get remaining budget."""
        return self.budget

    def book_vehicle(self, vehicle: Car | Motorcycle, date: str, vehicle_rental) -> bool:
        """
        Book a vehicle for a specific date.

        :param vehicle: The vehicle to be booked.
        :param date: The date for the booking.
        :param vehicle_rental: The rental service from which the vehicle is being booked.
        :return: True if the booking is successful, otherwise False.
        """
        if date is not None:
            if vehicle_rental.rent_vehicle(vehicle, date, self):
                self.budget -= vehicle.price
                self.costs += vehicle.price
                self.cars_booked.append(vehicle)
                return True
            else:
                return False

    def total_spent(self) -> int:
        """
        Calculate and return the total amount spent by the client.

        :return: The total amount of money the client has spent on successful bookings.
        """
        return self.costs

    def get_bookings(self) -> list[Car | Motorcycle]:
        """:return: List of all the vehicles client has booked."""
        return self.cars_booked


class VehicleRental:
    """Vehicle rental system managing vehicles, rents and budget."""

    def __init__(self) -> None:
        """Construct new VehicleRental."""
        self.vehicles = set()
        self.booked_vehicles = {}
        self.balance = 0
        self.clients = []

    def get_money(self) -> int:
        """
        Return the account balance VehicleRental currently has.

        :return: amount money that rental system has.
        """
        return self.balance

    def get_motorcycles(self) -> list[Motorcycle]:
        """:return: list of motorcycles in rental system."""
        return list(filter(lambda vehicle: isinstance(vehicle, Motorcycle), self.vehicles))

    def get_cars(self) -> list[Car]:
        """:return: list of cars in rental system."""
        return list(filter(lambda vehicle: isinstance(vehicle, Car), self.vehicles))

    def get_vehicle_bookings_dict(self) -> dict[Car | Motorcycle, list[str]]:
        """
        Get a dictionary of vehicles and their booked dates.

        This method returns a dictionary where the keys are vehicle objects (either `Car` or `Motorcycle`)
        and the values are lists of dates when the vehicles have been booked.

        Example:
            {
                Car(Ford, Sierra, 1993, Type.SPORTSCAR): ["23.12.2024", "21.01.2025"],
                Motorcycle(Ducati, Panigale, 2014): ["23.12.2024", "21.01.2025"]
            }

        :return: dictionary with vehicles as keys and lists of booked dates as values.
        """
        vehicles = {}  # all cars like {car: [04.03.2024]}
        for vehicle in self.vehicles:
            if vehicle in self.booked_vehicles.keys():
                vehicles[vehicle] = self.booked_vehicles[vehicle]
            else:
                vehicles[vehicle] = []
        return vehicles

    def get_clients(self) -> list[Client]:
        """:return: list of all clients who have placed a booking in rental."""
        return self.clients

    def add_vehicle(self, vehicle: Car | Motorcycle) -> bool:
        """
        Add a vehicle to the rental system if it is not already present.

        If vehicle with same hash is present it must not be added to the VehicleRental, return False.

        :param vehicle: Vehicle (Car or Motorcycle) to be added.
        :return: True if the vehicle was successfully added, False if it was already present.
        """
        if vehicle not in self.vehicles:
            self.vehicles.add(vehicle)
            return True
        return False

    def is_vehicle_available(self, vehicle: Car | Motorcycle, date: str) -> bool:
        """
        Check if the vehicle is available for rent on the specified date.

        :param vehicle: The vehicle to check availability for.
        :param date: The date to check availability on.
        :return: True if the vehicle is available, otherwise False.
        """
        # if check_date(date):
        if date is not None:
            if vehicle in self.vehicles:
                vehicle_time_list = self.booked_vehicles.get(vehicle, [])
                if date not in vehicle_time_list or vehicle not in self.booked_vehicles:
                    return True
        return False

    def rent_vehicle(self, vehicle: Car | Motorcycle, date: str, client: Client) -> bool:
        """
        Rent a vehicle to a client for a specified date if it is available and the client has sufficient funds.

        If booking the vehicle was successful, increase the budget of the rental. And increase the client costs.

        Vehicle, date and client must not be empty or None.

        :param vehicle: Vehicle to be rented.
        :param date: Date for which the vehicle is being rented.
        :param client: Client who is renting the vehicle.
        :return: True if the rental was successful, otherwise False.
        """
        # check inputs
        if not vehicle or not client or not date:
            return False

        # if not check_date(date):
        #     return False

        if date is None:
            return False

        if not isinstance(client, Client) or not isinstance(vehicle, (Car, Motorcycle)):
            return False

        # vehicle is in the rental
        if vehicle not in self.vehicles:
            return False

        # the client has enough money
        if client.get_pure_balance() < vehicle.price:
            return False

        if not self.is_vehicle_available(vehicle, date):
            return False

        # rent the vehicle and increase the budget
        if vehicle not in self.booked_vehicles:
            self.booked_vehicles[vehicle] = [date]
        else:
            self.booked_vehicles[vehicle].append(date)

        self.balance += vehicle.price

        if client not in self.clients:
            self.clients.append(client)

        vehicle.times_rented += 1

        return True

    def get_most_rented_vehicle(self) -> list[Motorcycle | Car]:
        """
        Return the most rented vehicle(s) from the rental system.

        :return: A list of the most rented vehicles, list could contain only one vehicle. If multiple vehicles have been
         rented the same number of times, all of those are returned. If no vehicle have been rented, return an empty
         list.
        """
        if len(self.booked_vehicles) > 0:
            dict_times_car_have_been_rented = {car: len(v) for car, v in self.booked_vehicles.items()}  # {car: 3}

            most_rented = max(dict_times_car_have_been_rented.values())

            result = []

            for vehicle, times in dict_times_car_have_been_rented.items():
                if times == most_rented:
                    result.append(vehicle)
            return result
        return []

    def find_vehicle_by_make(self, make: str) -> list[Car | Motorcycle]:
        """
        Find vehicles by their manufacturer (make).

        :param make: Manufacturer to search for (case-insensitive).
        :return: A list of vehicles matching the given make.
        """
        return list(filter(lambda vehicle: vehicle.make.lower() == make.lower(), self.vehicles))

    def find_car_by_type(self, type_of_car: Type) -> list[Car]:
        """
        Find cars by their type (e.g., SPORTSCAR, VAN, etc.).

        :param type_of_car: The type of car to search for (an instance of Type enum).
        :return: A list of cars matching the given type.
        """
        return list(filter(lambda vehicle: isinstance(vehicle, Car) and vehicle.type_of_car == type_of_car, self.vehicles))

    def get_best_client(self) -> Client:
        """
        Return the best client who rented the most vehicles.

        If multiple clients have rented the same number of vehicles, return the client who spent the most money.
        :return: The best client object.
        """
        if not self.clients:
            return None

        dict_clients_rented_cars_times = {client: len(client.cars_booked) for client in self.clients}  # {client: 3}

        most_rented = max(dict_clients_rented_cars_times.values())

        result = []

        for client, times in dict_clients_rented_cars_times.items():
            if times == most_rented:
                result.append(client)

        return max(result, key=lambda client: client.costs)

    def get_sorted_vehicles_list(self) -> list[Car | Motorcycle]:
        """
        Return a list of vehicles sorted from most rented to least rented.

        In case of a tie, vehicles are sorted by price from highest to lowest.
        :return: A list of vehicles sorted by popularity and price.
        """
        return list(sorted(self.vehicles, key=lambda vehicle: (-vehicle.times_rented, -vehicle.price)))

    def get_vehicles_by_year_range(self, start_year: int, end_year: int) -> list[Car | Motorcycle]:
        """
        Return a list of vehicles manufactured within a specified year range.

        Will use.
        :param start_year: The start year of the range (inclusive).
        :param end_year: The end year of the range (inclusive).
        :return: A list of vehicles manufactured within the specified year range.
        """
        return list(filter(lambda vehicle: start_year <= vehicle.year <= end_year, self.vehicles))


if __name__ == '__main__':
    # Creating vehicles
    car1 = Car("Toyota", "Camry", 2020, Type.SPORTSCAR)  # price 200
    car2 = Car("Ford", "Focus", 2018, Type.VAN)  # price 100
    car3 = Car("Honda", "Civic", 2019, Type.CONVERTIBLE)  # price 150
    car4 = Car("Mazda", "3", 2017, Type.OTHER)  # price 50
    motorcycle1 = Motorcycle("Harley-Davidson", "Sportster", 2021)  # price 100
    motorcycle2 = Motorcycle("Yamaha", "MT-07", 2022)  # price 100

    # Vehicle list
    vehicles = [car1, car2, car3, car4, motorcycle1, motorcycle2]

    # Print vehicles
    print("Created vehicles:")
    for vehicle in vehicles:
        print(vehicle, f"Price: {vehicle.get_price()}")

    # Create a rental system
    rental = VehicleRental()

    # Add vehicles to the rental system
    print("\nAdding vehicles to rental system:")
    for vehicle in vehicles:
        print(f"Adding {vehicle}: {rental.add_vehicle(vehicle)}")

    # Attempt to add duplicate vehicle
    print("\nAttempting to add duplicate vehicle:")
    print(f"Adding {car1}: {rental.add_vehicle(car1)}")  # Should return False

    # Check available vehicles
    print("\nAvailable cars:")
    print(rental.get_cars())

    print("\nAvailable motorcycles:")
    print(rental.get_motorcycles())

    # Create clients
    client1 = Client("Alice", 200)
    client2 = Client("Bob", 2000)

    # Booking vehicles
    print("\nBooking vehicles:")
    date1 = "12.12.2024"
    date2 = "12.10.2024"
    print(f"Client {client1.name} books {car2} on {date1}: {rental.rent_vehicle(car2, date1, client1)}")
    print(f"Client {client1.name} books {car2} on {date2}: {rental.rent_vehicle(car2, date2, client1)}")
    print(f"Client {client2.name} books {motorcycle1} on {date1}: {rental.rent_vehicle(motorcycle1, date1, client2)}")
    print(f"Client {client2.name} books {motorcycle1} on {date1}: {rental.rent_vehicle(motorcycle1, date1, client2)}")

    # Attempting to book an already booked vehicle
    print(f"Client {client1.name} books {car1} again on {date1}: {rental.rent_vehicle(car1, date1, client1)}")  # False
    # Client doesn't have enough money
    print(f"Client {client2.name} books {car3} on {date1}: {rental.rent_vehicle(car1, date1, client2)}")  # False
    print(f"Client {client2.name} books {car4} on {date1}: {rental.rent_vehicle(car4, date1, client2)}")  # True

    # Booking on a different date
    date2 = "13.12.2024"
    print(f"Client {client1.name} books {car1} on {date2}: {rental.rent_vehicle(car1, date2, client1)}")

    # Booking from the client side
    print(f"Client {client1.name} books {motorcycle2} in rental on {date1}: {client1.book_vehicle(motorcycle2, date1, rental)}")
    print(f"Client {client1.name} books {car1} in rental on {date1}: {client1.book_vehicle(car1, date1, rental)}")

    # Check rental balance
    print("\nRental system balance:")
    print(rental.get_money())

    # Check bookings
    print("\nVehicle bookings dictionary:")
    print(rental.get_vehicle_bookings_dict())

    # Find vehicles by make
    print("\nFind vehicles by make:")
    print(rental.find_vehicle_by_make("Toyota"))

    # Find cars by type
    print("\nFind cars by type:")
    print(rental.find_car_by_type(Type.SPORTSCAR))

    # Get sorted vehicles list
    print("\nSorted vehicles by popularity and price:")
    print(rental.get_sorted_vehicles_list())

    # Get most rented vehicle
    print("\nMost rented vehicle:")
    print(rental.get_most_rented_vehicle())

    # Get best client
    print("\nBest client:")
    print(rental.get_best_client())

    # Vehicles by year range
    print("\nVehicles by year range 2018-2020:")
    print(rental.get_vehicles_by_year_range(2018, 2020))