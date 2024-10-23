"""Control number."""


def concat_all_numbers(list_of_string_digits: list[str]) -> int:
    """Concat all digits to get the number."""
    number = ""
    for i in range(0, len(list_of_string_digits)):
        number += list_of_string_digits[i]
    return int(number)


def control_number(encrypted_string: str) -> bool:
    """
    Given encrypted string that has a control number in the end of it, return True if correct, else False.

    Calculating the correct control number:
    1. Start the calculation from 0.
    2. Add 1 for every lowercase occurrence.
    3. Add 2 for every uppercase occurrence.
    4. Add 5 for any of the following symbol occurrences: "?!@#".
    Other symbols/letters/digits don't affect the result.

    NB! If for example the number you come up with is 25, you only have to check the last two digits of the string.
    e.g. control_number("?!?!#4525") -> True, because it ends with 25.

    :param encrypted_string: encrypted string
    :return: validation
    """
    # init
    calculation = 0  # num
    special_symbols_array = ["?", "!", "@", "#"]

    # normal_conditions
    for sign in encrypted_string:
        if sign.islower():
            calculation += 1
        elif sign.isupper():
            calculation += 2
        else:
            for special_sign in special_symbols_array:
                if sign == special_sign:
                    calculation += 5

    # number_checking, init
    encrypted_number = 0
    encrypted_digits = []
    len_of_calculation = len(str(calculation))  # doesn't mutate the original data!!! How many digits you will find in the input.

    # number_checking, logic
    for i in range(1, len_of_calculation + 1):  # including last number
        if encrypted_string[-i].isdigit():
            encrypted_digits.insert(0, encrypted_string[-i])  # type str, add to the start of the array

    encrypted_number = concat_all_numbers(encrypted_digits)

    # result
    # calculation = str(calculation)
    # return encrypted_string.endswith(calculation)
    return encrypted_number == calculation


if __name__ == '__main__':
    print(control_number("mE0W5"))  # True
    print(control_number("SomeControlNR?20"))  # False
    print(control_number("False?Nr9"))  # False
    print(control_number("#Hello?!?26"))  # True
    print(control_number("3423982340000000.....///....0"))  # True
    print(control_number("#Shift6"))  # False
    print(control_number(
        '??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!??#!@@!5081750'
    ))
