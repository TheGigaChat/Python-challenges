"""If you're going to perform recursion, you need to use recursion."""


def loop_reverse(string: str) -> str:
    """
    Reverse a string using a loop or string slicing.

    :param string: input string
    :return: reversed input string
    """
    return string[::-1]


def recursive_reverse(string: str) -> str:
    """
    Reverse a string using recursion.

    Solution must be recursive!

    :param string: input string
    :return: reversed input string
    """
    if not string:
        return ""
    else:
        return string[-1] + recursive_reverse(string[:-1])


def loop_sum(num: int) -> int:
    """
    Calculate the sum of all numbers up to 'num' (including 'num') using a loop.

    :param num: the last number to add to the sum.
    :return: sum of integers from 0 up to given number.
    """
    return sum(range(num + 1))


def recursive_sum(num: int, counter=0) -> int:
    """
    Calculate the sum of all numbers up to 'num' (including 'num') using recursion.

    Solution must be recursive!

    :param num: the last number to add to the sum.
    :param counter: numbers that is used by the sum.
    :return: sum of integers from 0 up to given number.
    """
    if counter > num:
        return 0
    else:
        return counter + recursive_sum(num, counter + 1)


def loop_factorial(num: int) -> int:
    """
    Calculate the factorial of an integer 'num' using a loop.

    :param num: integer from which the factorial should be calculated.
    :return: factorial of given number
    """
    if num < 0:
        return -1

    factorial_numbers = list(range(1, num + 1))
    result = 1
    for n in factorial_numbers:
        result *= n
    return result


def recursive_factorial(num: int) -> int:
    """
    Calculate the factorial of an integer 'num' using recursion.

    Solution must be recursive!

    :param num: integer from which the factorial should be calculated.
    :return: factorial of given number
    """
    if num < 0:
        return -1
    if num <= 1:
        return 1
    else:
        return num * recursive_factorial(num - 1)


def check_palindrome(string: str) -> bool:
    """
    Check if the input 'string' is a palindrome using recursion.

    A palindrome is a word that is spelled exactly the same way when read regularly
    or in reverse. For example, 'radar' is a palindrome.

    Solution must be recursive!

    :param string: string argument
    :return: boolean. True if 'string' is a palindrome, False otherwise
    """
    if len(string) < 2:
        return True
    if string and string[0] == string[-1]:
        return check_palindrome(string[1:-1])
    return False


def check_for_prime(num: int, i=2) -> bool:
    """
    Check if input number 'num' is a prime number using recursion.

    Solution must be recursive!

    :param num: integer to be checked
    :param i: used to check if 'num' is a multiple of some integer.
    :return: boolean. True if 'num' is prime, False otherwise
    """
    if num < 2:
        return False

    if i * i > num:
        return True

    if num % i == 0:
        return False
    else:
        return check_for_prime(num, i + 1)


def replace(input_string: str, char_to_replace: str, new_string: str, i=0) -> str:
    """
    Replace all occurrences of some specific character 'char_to_replace' in string 'input_string' with 'new_string'.

    Argument 'new_string' can be any length, 'char_to_replace' must be of length 1.
    If length of 'char_to_replace' is not equal to 1, return "Length of char_to_replace must be one character!".
    If 'input_string' is an emtpy string, return "".

    Solution must be recursive!

    :param input_string: input string
    :param char_to_replace: character, whose occurences will be replaced
    :param new_string: string of characters that will replace all occurences of 'char_to_replace'
    :param i index to iterate through every character in the input
    :return: input string with all 'char_to_replace' characters replaced with 'new_string'-s
    """
    rules_error = "Length of char_to_replace must be one character!"
    if len(char_to_replace) != 1:
        return rules_error
    if i + 1 > len(input_string):
        return input_string
    if input_string[i] == char_to_replace:
        input_string = input_string[:i] + new_string + input_string[i + 1:]
        return replace(input_string, char_to_replace, new_string, i + len(new_string))
    return replace(input_string, char_to_replace, new_string, i + 1)


def fibonacci(num: int, fib_list=None) -> list | None:
    """
    Return a list of length 'num' of Fibonacci numbers using recursion.

    If 'num' is less than zero, return None.
    If 'num' is less than two return a list of the initial two Fibonacci numbers.
    Harder version: in case 'num' is 0, return []; in case 'num' is 1, return [0]

    Solution must be recursive!

    fibonacci(-1) => None
    fibonacci(0) => [0, 1]   ([] is also accepted)
    fibonacci(1) => [0, 1]   ([0] is also accepted)
    fibonacci(2) => [0, 1]
    fibonacci(9) => [0, 1, 1, 2, 3, 5, 8, 13, 21]

    :param num: integer. The length of the list of Fibonacci numbers to return
    :param fib_list: used to pass the currently computed list on numbers
    :return: list of the first 'num' Fibonacci numbers
    """
    if fib_list is None:  # ask the Artjom why I can't have mutable default value
        fib_list = [0, 1]

    if num < 0:
        return None
    if num <= 2:
        return [0, 1]

    if len(fib_list) < num:
        fib_list.append(fib_list[-2] + fib_list[-1])
        return fibonacci(num, fib_list)
    else:
        return fib_list


def x_sum_loop(nums: list, x: int) -> int:
    """
    Given list 'nums' and a number called 'x' iteratively return sum of every x'th number in the list 'nums'.

    In this task "indexing" starts from 1, so if 'x' = 2 and 'nums' = [2, 3, 4, -9], the output should be -6 (3 + -9).
    'X' can also be negative, in that case indexing starts from the end of 'nums', see examples below.
    If 'x' is 0, the sum should be 0 as well.

    :param nums: list of integers
    :param x: number indicating every which num to add to sum
    :return: sum of every x'th number in the list
    """
    result_sum = 0

    if x == 0:
        return 0
    if x < 0:
        nums.reverse()
        x = abs(x)

    for i, num in enumerate(nums):
        if (i + 1) % x == 0:
            result_sum += num

    return result_sum


def x_sum_recursion(nums: list, x: int, multiplier=1) -> int:
    """
    Given list 'nums' and a number called 'x' recursively return sum of every x'th number in 'nums'.

    In this task "indexing" starts from 1, so if 'x' = 2 and 'nums' = [2, 3, 4, -9], the output should be -6 (3 + -9).
    'X' can also be negative, in that case indexing starts from the end of 'nums', see examples below.
    If 'x' is 0, the sum should be 0 as well.

    Solution must be recursive!

    :param nums: list of integers
    :param x: number indicating every which num to add to sum
    :param multiplier: number to help iterate through every x value
    :return: sum of every x'th number in the list
    """
    if x == 0:
        return 0
    if x > 0:
        index = multiplier * x - 1
        if index < len(nums):
            return nums[index] + x_sum_recursion(nums, x, multiplier + 1)
        else:
            return 0
    else:
        index = multiplier * x
        if abs(index) <= len(nums):
            return nums[index] + x_sum_recursion(nums, x, multiplier + 1)
        else:
            return 0


def sum_squares(nested_list: list | int) -> int:
    """
    Write a function that sums squares of numbers in 'nested_list' using recursion.

    'nested_list' may contain additional lists.

    Solution must be recursive!

    :param nested_list: list of lists of lists of lists of lists ... and ints
    :return: sum of squares
    """
    total = 0
    for element in nested_list:
        if type(element) is list:
            total += sum_squares(element)
        else:
            total += element ** 2
    return total


def sum_squares_no_loop(nested_list: list | int) -> int:
    """
    Write a function that sums squares of numbers in 'nested_list' using recursion.

    'nested_list' may contain additional lists.

    Solution must be recursive!

    :param nested_list: list of lists of lists of lists of lists ... and ints
    :return: sum of squares
    """
    if not nested_list:
        return 0

    first_arg, *rest = nested_list
    if type(first_arg) is list:
        return sum_squares_no_loop(first_arg) + sum_squares_no_loop(rest)
    else:
        return first_arg ** 2 + sum_squares_no_loop(rest)


if __name__ == '__main__':
    print("\nloop reverse:")
    print(f"expected: \"yeh\", got: \"{loop_reverse('hey')}\"")
    print(f"expected: \"aaa\", got: \"{loop_reverse('aaa')}\"")
    print(f"expected: \"\", got: \"{loop_reverse('')}\"")
    print(f"expected: \"1\", got: \"{loop_reverse('1')}\"")

    print("\nrecursive reverse:")
    print(f"expected: \"yeh\", got: \"{recursive_reverse('hey')}\"")
    print(f"expected: \"aaa\", got: \"{recursive_reverse('aaa')}\"")
    print(f"expected: \"\", got: \"{recursive_reverse('')}\"")
    print(f"expected: \"1\", got: \"{recursive_reverse('1')}\"")

    print("\nloop sum:")
    print(f"expected: 0, got: {loop_sum(0)}")
    print(f"expected: 6, got: {loop_sum(3)}")
    print(f"expected: 15, got: {loop_sum(5)}")

    print("\nrecursive sum:")
    print(f"expected: 0, got: {recursive_sum(0)}")
    print(f"expected: 6, got: {recursive_sum(3)}")
    print(f"expected: 15, got: {recursive_sum(5)}")

    print("\nloop factorial:")
    print(f"expected: 1, got: {loop_factorial(0)}")
    print(f"expected: 120, got: {loop_factorial(5)}")
    print(f"expected: 5040, got: {loop_factorial(7)}")
    print(f"expected: -1, got: {loop_factorial(-1)}")
    print(f"expected: -1, got: {loop_factorial(-100)}")

    print("\nrecursive factorial:")
    print(f"expected: 1, got: {recursive_factorial(0)}")
    print(f"expected: 120, got: {recursive_factorial(5)}")
    print(f"expected: 5040, got: {recursive_factorial(7)}")
    print(f"expected: -1, got: {recursive_factorial(-1)}")
    print(f"expected: -1, got: {recursive_factorial(-5)}")

    print("\ncheck palindrome:")
    print(f"expected: True, got: {check_palindrome('kirik')}")
    print(f"expected: False, got: {check_palindrome('horror')}")
    print(f"expected: True, got: {check_palindrome('0546450')}")
    print(f"expected: True, got: {check_palindrome('-')}")
    print(f"expected: True, got: {check_palindrome('')}")

    print("\ncheck for prime:")
    print(f"expected: False, got: {check_for_prime(20)}")
    print(f"expected: True, got: {check_for_prime(13)}")
    print(f"expected: True, got: {check_for_prime(997)}")
    print(f"expected: True, got: {check_for_prime(2)}")
    print(f"expected: False, got: {check_for_prime(1)}")
    print(f"expected: False, got: {check_for_prime(0)}")
    print(f"expected: True, got: {check_for_prime(17)}")
    print(f"expected: True, got: {check_for_prime(37)}")
    print(f"expected: False, got: {check_for_prime(50)}")
    print(f"expected: True, got: {check_for_prime(97)}")
    print(f"expected: True, got: {check_for_prime(101)}")
    print(f"expected: True, got: {check_for_prime(199)}")

    print("\nreplace:")
    print(f"expected: \"12asndndndnd\", got: \"{replace('12asdddd', 'd', 'nd')}\"")
    print(f"expected: \"Length of char_to_replace must be one character!\", got: \"{replace('', '', '')}\"")
    print(f"expected: \"\", got: \"{replace('', '6', '9')}\"")
    print(f"expected: \"hello world!\", got: \"{replace('hello ', ' ', ' world!')}\"")
    print(f"expected: \"aabitsamEEs\", got: \"{replace('aabitsamees', 'e', 'E')}\"")
    print(f"expected: \"ramgmdOMSTRimgmg123\", got: \"{replace('randOMSTRing123', 'n', 'mgm')}\"")
    print(
        f"expected: \"Length of char_to_replace must be one character!\", got: \"{replace('WhatStringIsThis???', '', 'ii')}\"")
    print(
        f"expected: \"Length of char_to_replace must be one character!\", got: \"{replace('WhatStringIsThis???', 'in', 'i')}\"")

    print("\nfibonacci:")
    print(f"expected: [0, 1, 1, 2, 3, 5, 8, 13, 21], got: {fibonacci(9)}")
    print(f"expected: None, got: {fibonacci(-1)}")
    print(f"expected: [0, 1], got: {fibonacci(0)}")
    print(f"expected: [0, 1], got: {fibonacci(1)}")

    print("\nx sum loop:")
    print(f"expected: 158, got: {x_sum_loop([43, 90, 115, 500], -2)}")
    print(f"expected: 0, got: {x_sum_loop([], 3)}")
    print(f"expected: 11, got: {x_sum_loop([2, 5, 6, 0, 15, 5], 3)}")
    print(f"expected: 0, got: {x_sum_loop([0, 5, 6, -5, -9, 3], 1)}")
    print(f"expected: 0, got: {x_sum_loop([1, 2], -9)}")
    print(f"expected: 0, got: {x_sum_loop([2, 3, 6], 5)}")
    print(f"expected: 15, got: {x_sum_loop([6, 5, 3, 2, 9, 8, 6, 5, 4], 3)}")

    print("\nx sum recursion:")
    print(f"expected: 0, got: {x_sum_recursion([], 3)}")
    print(f"expected: 11, got: {x_sum_recursion([2, 5, 6, 0, 15, 5], 3)}")
    print(f"expected: 0, got: {x_sum_recursion([0, 5, 6, -5, -9, 3], 1)}")
    print(f"expected: 15, got: {x_sum_recursion([6, 5, 3, 2, 9, 8, 6, 5, 4], 3)}")
    print(f"expected: 158, got: {x_sum_recursion([43, 90, 115, 500], -2)}")
    print(f"expected: 0, got: {x_sum_recursion([1, 2], -9)}")
    print(f"expected: 0, got: {x_sum_recursion([2, 3, 6], 5)}")

    print("\nsum squares:")
    print(f"expected: 14, got: {sum_squares([[1, 2], 3])}")
    print(f"expected: 14, got: {sum_squares([1, 2, 3])}")
    print(f"expected: 4, got: {sum_squares([[[[[[[[[2]]]]]]]]])}")
