"""Exam0."""
from typing import Optional
import functools


def find_capital_letters(s: str) -> str:
    """
    Return only capital letters from the string.

    #1

    If there are no capital letters, return empty string.
    The string contains only latin letters (a-z and A-Z).
    The letters should be in the same order as they appear in the input string.

    find_capital_letters("ABC") => "ABC"
    find_capital_letters("abc") => ""
    find_capital_letters("aAbBc") => "AB"
    """
    return_string = ""

    for letter in s:
        if letter.isupper():
            return_string += letter

    return return_string


def close_far(a: int, b: int, c: int) -> bool:
    """
    Return if one value is "close" and other is "far".

    #2

    Given three ints, a b c, return true if one of b or c is "close" (differing from a by at most 1),
    while the other is "far", differing from both other values by 2 or more.

    close_far(1, 2, 10) => True
    close_far(1, 2, 3) => False
    close_far(4, 1, 3) => True
    """
    if abs(b - a) <= 1 and abs(c - a) >= 2 and abs(c - b) >= 2:
        return True
    if abs(c - a) <= 1 and abs(b - a) >= 2 and abs(b - c) >= 2:
        return True
    return False


# print(close_far(-5, -1, -100))


def get_names_from_results(results_string: str, min_result: int) -> list:
    """
    Given a string of names and scores, return a list of names where the score is higher than or equal to min_result.

    #3

    Results are separated by comma (,). Result contains a score and optionally a name.
    Score is integer, name can have several names separated by single space.
    Name part can also contain numbers and other symbols (except for comma).
    Return only the names which have the score higher or equal than min_result.
    The order of the result should be the same as in input string.

    get_names_from_results("ago 123,peeter 11", 0) => ["ago", "peeter"]
    get_names_from_results("ago 123,peeter 11,33", 10) => ["ago", "peeter"]  # 33 does not have the name
    get_names_from_results("ago 123,peeter 11", 100) => ["ago"]
    get_names_from_results("ago 123,peeter 11,kitty11!! 33", 11) => ["ago", "peeter", "kitty11!!"]
    get_names_from_results("ago 123,peeter 11,kusti riin 14", 12) => ["ago", "kusti riin"]
    """
    final_list = []

    def toggle_name_score(name_or_score) -> str:
        """Toggle name and score."""
        if name_or_score == "name":
            return "score"
        else:
            return "name"

    input_data_split = results_string.split(",")
    for person in input_data_split:
        person_reversed = person[::-1].strip()
        score_reversed = ""
        name_reversed = ""
        current_toggle = "score"
        for symbol in person_reversed:
            if current_toggle == "score":
                if symbol != " ":
                    score_reversed += symbol
                else:
                    current_toggle = toggle_name_score(current_toggle)
            else:
                name_reversed += symbol
        if score_reversed and int(score_reversed[::-1]) >= min_result and name_reversed:
            name = name_reversed[::-1]
            final_list.append(name)

    return final_list


# print(get_names_from_results("adkfj4#@8 122,22,222,q 222", 12))


def tic_tac_toe(game: list) -> int:
    """
    Find the game winner.

    The 3x3 table is represented as a list of 3 rows, each row has 3 elements (ints).
    The value can be 1 (player 1), 2 (player 2) or 0 (empty).
    The winner is the player who gets 3 of her pieces in a row, column or diagonal.
    """
    # Check rows and columns
    for i in range(3):
        if game[i][0] == game[i][1] == game[i][2] and game[i][0] != 0:
            return game[i][0]  # Row winner
        if game[0][i] == game[1][i] == game[2][i] and game[0][i] != 0:
            return game[0][i]  # Column winner

    # Check diagonals
    if game[0][0] == game[1][1] == game[2][2] and game[0][0] != 0:
        return game[0][0]  # Main diagonal winner
    if game[0][2] == game[1][1] == game[2][0] and game[0][2] != 0:
        return game[0][2]  # Anti-diagonal winner

    # No winner
    return 0


# print(tic_tac_toe([[0, 0, 0], [1, 1, 1], [0, 0, 0]]))


def rainbows(field: str) -> int:
    """
    Count rainbows recursively.

    :param field: string to search rainbows from
    :return: number of valid rainbows in the string
    """
    field = field.lower()

    # Define the rainbow patterns
    forward_rainbow = "rainbow"
    backward_rainbow = "wobniar"

    # Base case: If the field is shorter than a rainbow, return 0
    if len(field) < len(forward_rainbow):
        return 0

    # Check if the beginning of the string matches a forward or backward rainbow
    if field.startswith(forward_rainbow) or field.startswith(backward_rainbow):
        # Remove the matched rainbow and recurse
        return 1 + rainbows(field[len(forward_rainbow):])

    # Recurse by removing the first character and checking the rest of the string
    return rainbows(field[1:])


# print(rainbows("rraaiinnbbooww"))


def longest_substring(text: str, all_combinations=None) -> str:
    """
    Find the longest substring.

    #6

    Substring may not contain any character twice.
    CAPS and lower case chars are the same (a == A)
    In output, the case (whether lower- or uppercase) should remain.
    If multiple substrings have same length, choose first one.

    aaa -> a
    abc -> abc
    abccba -> abc
    babcdEFghij -> abcdEFghij
    abBcd => Bcd
    '' -> ''
    """
    if all_combinations is None:
        all_combinations = []

    combination = ""
    for symbol in text:
        if symbol.upper() not in combination and symbol.lower() not in combination:
            combination += symbol
        else:
            all_combinations.append(combination)
            return longest_substring(text[1::], all_combinations)

    all_combinations.append(combination)
    all_combinations.reverse()
    longest_combination = functools.reduce(lambda comb1, comb2: comb1 if len(comb1) > len(comb2) else comb2, all_combinations)
    return longest_combination


# print(longest_substring("Aab"))


class Student:
    """Student class."""

    def __init__(self, name: str, average_grade: float, credit_points: int):
        """Initialize student."""
        self.credit_points = credit_points
        self.average_grade = average_grade
        self.name = name

    def __repr__(self) -> str:
        """Return a string representation of the Student object."""
        return f'My name is {self.name}, I have average grade {self.average_grade} and I passed {self.credit_points} EAPs.'


def create_student(name: str, grades: list, credit_points: int) -> Student:
    """
    Create a new student where average grade is the average of the grades in the list.

    Round the average grade up to three decimal places.
    If the list of grades is empty, the average grade will be 0.
    """
    if grades:
        average_grade = round(sum(grades) / len(grades), 3)
    else:
        average_grade = 0
    return Student(name, average_grade, credit_points)


def get_top_student_with_credit_points(students: list, min_credit_points: int) -> Student | None:
    """
    Return the student with the highest average grade who has enough credit points.

    If there are no students with enough credit points, return None.
    If several students have the same average score, return the first.
    """
    sorted_students = list(filter(lambda st: st.credit_points >= min_credit_points, students))

    if sorted_students:
        best_student = functools.reduce(lambda st1, st2: st1 if st1.average_grade > st2.average_grade else st2, sorted_students[::-1])
        if best_student.credit_points >= min_credit_points:
            return best_student
    return None


def add_result_to_student(student: Student, grades_count: int, new_grade: int, credit_points) -> Student:
    """
    Update student average grade and credit points by adding a new grade (result).

    As the student object does not have grades count information, it is provided in this function.
    average grade = sum of grades / count of grades

    With the formula above, we can deduct:
    sum of grades = average grade * count of grades

    The student has the average grade, function parameters give the count of grades.
    If the sum of grades is known, a new grade can be added and a new average can be calculated.
    The new average grade must be rounded to three decimal places.
    Given credits points should be added to old credit points.

    Example1:
        current average (from student object) = 4
        grades_count (from parameter) = 2
        so, the sum is 2 * 4 = 8
        new grade (from parameter) = 5
        new average = (8 + 5) / 3 = 4.333
        The student object has to be updated with the new average

    Example2:
        current average = 0
        grades_count = 0
        calculated sum = 0 * 0 = 0
        new grade = 4
        new average = 4 / 1 = 4

    Return the modified student object.
    """
    current_average = student.average_grade
    sum_of_grades = current_average * grades_count
    new_average_grade = round((sum_of_grades + new_grade) / (grades_count + 1), 3)

    student.average_grade = new_average_grade
    student.credit_points += credit_points
    return student


def get_ordered_students(students: list) -> list:
    """
    Return a new sorted list of students by (down).

    credit points (higher first), average_grade (higher first), name (a to z).
    """
    return list(sorted(students, key=lambda st: (-st.credit_points, -st.average_grade, st.name)))


class Room:
    """Room."""

    def __init__(self, number: int, price: int, features=None):
        """Initialize room."""
        self.number = number
        self.price = price
        self.is_booked = False
        self.features = []

        if features is not None:
            self.features = features

    def __repr__(self) -> str:
        """Return a string representation of the Room object."""
        return f'The room number {self.number} with a price of {self.price}$ and my features are {self.features}.'

    def add_feature(self, feature: str) -> bool:
        """
        Add a feature to the room.

        Do not add the feature and return False if:
        - the room already has that feature
        - the room is booked.
        Otherwise, add the feature to the room and return True
        """
        if feature in self.features:
            return False

        if self.is_booked:
            return False

        self.features.append(feature)
        return True

    def get_features(self) -> list:
        """Return all the features of the room."""
        return self.features

    def get_price(self) -> int:
        """Return the price."""
        return self.price

    def get_number(self) -> int:
        """Return the room number."""
        return self.number


class Hotel:
    """Hotel."""

    def __init__(self):
        """Initialize hotel."""
        self.rooms = []

    def add_room(self, room: Room) -> bool:
        """
        Add room to hotel.

        If a room with the given number already exists, do not add a room and return False.
        Otherwise add the room to hotel and return True.
        """
        room_numbers = list(map(lambda room: room.number, self.rooms))
        if room.number in room_numbers:
            return False

        self.rooms.append(room)
        return True

    def book_room(self, required_features: list) -> Optional[Room]:
        """
        Book an available room which has the most matching features.

        Find a room which has most of the required features.
        If there are several with the same amount of matching features, return the one with the smallest room number.
        If there is no available rooms, return None
        """
        if not self.get_available_rooms():
            return None

        def filter_by_features(room):
            """Check if the room satisfies all required features."""
            for feature in required_features:
                if feature not in room.features:
                    return False
            return True

        rooms_by_required_features = list(filter(filter_by_features, self.get_available_rooms()))

        if rooms_by_required_features:
            best_room = functools.reduce(lambda rm1, rm2: rm1 if rm1.number < rm2.number else rm2, rooms_by_required_features)
        else:
            best_room = functools.reduce(lambda rm1, rm2: rm1 if rm1.number < rm2.number else rm2, self.get_available_rooms())

        best_room.is_booked = True
        return best_room

    def get_available_rooms(self) -> list:
        """Return a list of available (not booked) rooms."""
        return list(filter(lambda room: not room.is_booked, self.rooms))

    def get_rooms(self) -> list:
        """Return all the rooms (both booked and available)."""
        return self.rooms

    def get_booked_rooms(self) -> list:
        """Return all the booked rooms."""
        return list(filter(lambda room: room.is_booked, self.rooms))

    def get_feature_profits(self) -> dict:
        """
        Return a dict where key is a feature and value is the total price for the booked rooms which have the feature.

        Example:
            room1, price=100, features=a, b, c
            room2, price=200, features=b, c, d
            room3, price=400, features=a, c

        all the rooms are booked
        result:
        {
        'a': 500,
        'b': 300,
        'c': 700,
        'd': 200
        }
        """
        result_dict = {}

        booked_rooms = self.get_booked_rooms()
        for room in booked_rooms:
            for feature in room.features:
                result_dict[feature] = result_dict.get(feature, 0)
                result_dict[feature] += room.price

        return result_dict

    def get_most_profitable_feature(self) -> Optional[str]:
        """
        Return the feature which profits the most.

        Use get_feature_profits() method to get the total price for every feature.
        Return the feature which has the highest value (profit).
        If there are several with the same max value, return the feature which is alphabetically lower (a < z)
        If there are no features booked, return None.
        """
        features_prices = self.get_feature_profits()
        if not features_prices:
            return None

        # Find the feature with the maximum profit, with ties broken alphabetically
        return max(features_prices, key=lambda feature: (features_prices[feature], -ord(feature[0])))


if __name__ == '__main__':
    # Rooms check
    def test_add_feature():
        room = Room(101, 100)
        assert room.add_feature("WiFi") == True  # Add new feature
        assert room.add_feature("WiFi") == False  # Adding duplicate feature
        room.is_booked = True
        assert room.add_feature("Pool") == False  # Cannot add feature to booked room

    test_add_feature()

    def test_get_features():
        room = Room(102, 150)
        room.add_feature("TV")
        room.add_feature("AC")
        assert set(room.get_features()) == {"TV", "AC"}  # Verify all added features

    test_get_features()

    def test_get_price_and_number():
        room = Room(103, 200)
        assert room.get_price() == 200
        assert room.get_number() == 103

    test_get_price_and_number()

    # Hotel check
    def test_add_room():
        hotel = Hotel()
        room1 = Room(101, 100)
        room2 = Room(102, 150)
        assert hotel.add_room(room1) == True  # Room added successfully
        assert hotel.add_room(room1) == False  # Duplicate room
        assert hotel.add_room(room2) == True  # Another room added successfully

    test_add_room()

    def test_book_room():
        hotel = Hotel()
        room1 = Room(101, 100)
        room2 = Room(102, 150)
        room3 = Room(103, 120)
        room1.add_feature("WiFi")
        room1.add_feature("AC")
        room2.add_feature("WiFi")
        room2.add_feature("TV")
        room3.add_feature("Pool")

        hotel.add_room(room1)
        hotel.add_room(room2)
        hotel.add_room(room3)

        # Book based on features
        booked_room = hotel.book_room(["WiFi", "AC"])
        assert booked_room == room1  # Room 1 has the most matching features
        assert room1.is_booked == True  # Room 1 is now booked

        # Try booking again (Room 1 is booked, so Room 2 should be picked)
        booked_room = hotel.book_room(["WiFi"])
        assert booked_room == room2  # Room 2 matches and is available
        assert room2.is_booked == True

    test_book_room()

    def test_get_available_rooms():
        hotel = Hotel()
        room1 = Room(101, 100)
        room2 = Room(102, 150)
        room1.is_booked = True
        hotel.add_room(room1)
        hotel.add_room(room2)
        available_rooms = hotel.get_available_rooms()
        assert available_rooms == [room2]  # Only Room 2 is available

    test_get_available_rooms()


    def test_get_feature_profits():
        hotel = Hotel()
        room1 = Room(101, 100)
        room2 = Room(102, 200)
        room3 = Room(103, 150)
        room1.add_feature("WiFi")
        room1.add_feature("AC")
        room2.add_feature("WiFi")
        room2.add_feature("TV")
        room3.add_feature("Pool")
        room3.add_feature("AC")

        hotel.add_room(room1)
        hotel.add_room(room2)
        hotel.add_room(room3)

        room1.is_booked = True
        room2.is_booked = True
        room3.is_booked = True

        feature_profits = hotel.get_feature_profits()
        expected_profits = {
            "WiFi": 300,  # Room 1 (100) + Room 2 (200)
            "AC": 250,  # Room 1 (100) + Room 3 (150)
            "TV": 200,  # Room 2 (200)
            "Pool": 150,  # Room 3 (150)
        }
        assert feature_profits == expected_profits

    test_get_feature_profits()

    def test_get_most_profitable_feature():
        hotel = Hotel()
        room1 = Room(101, 100)
        room2 = Room(102, 200)
        room1.add_feature("WiFi")
        room2.add_feature("WiFi")
        room2.add_feature("TV")
        hotel.add_room(room1)
        hotel.add_room(room2)
        room1.is_booked = True
        room2.is_booked = True
        assert hotel.get_most_profitable_feature() == "WiFi"  # WiFi profits 300 vs TV profits 200

    test_get_most_profitable_feature()

    # Edge cases
    def test_book_room_no_available_rooms():
        hotel = Hotel()
        room1 = Room(101, 100)
        room1.is_booked = True
        hotel.add_room(room1)
        assert hotel.book_room(["WiFi"]) == None  # No rooms available

    test_book_room_no_available_rooms()

    def test_get_most_profitable_feature_tie():
        hotel = Hotel()
        room1 = Room(101, 100)
        room2 = Room(102, 100)
        room1.add_feature("WiFi")
        room2.add_feature("AC")
        hotel.add_room(room1)
        hotel.add_room(room2)
        room1.is_booked = True
        room2.is_booked = True
        assert hotel.get_most_profitable_feature() == "AC"  # AC and WiFi tie, but AC is alphabetically smaller

    test_get_most_profitable_feature_tie()
