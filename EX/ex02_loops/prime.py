"""Prime number identifier."""


def is_prime_number(number: int) -> bool:
    """
    Check if the number is a prime number.

    Prime number is a natural number which is only divisible by 1 and itself. 0 and 1 are not prime numbers.

    Conditions:
    1. If number is a prime number then return boolean True
    2. If number is not a prime number then return boolean False

    :param number: the number to check.
    :return: boolean True if number is a prime number or False if number is not a prime number.
    """
    # init
    list_of_divisions = []

    # mail logic
    for i in range(1, number + 1):
        if number % i == 0:
            list_of_divisions.append(1)

    # result
    return len(list_of_divisions) == 2


if __name__ == '__main__':
    print(is_prime_number(2))  # -> True
    print(is_prime_number(89))  # -> True
    print(is_prime_number(23))  # -> True
    print(is_prime_number(4))  # -> False
    print(is_prime_number(7))  # -> True
    print(is_prime_number(88))  # -> False
