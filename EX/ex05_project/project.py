"""Project one."""
import re


def add_country_code(number: str) -> str:
    """Country code."""
    if len(number) > 0:
        if number[0] != "+":
            number = "+372 " + number
    return number


def is_valid(number: str) -> bool:
    """Is valid."""
    pattern = r"[+][\d]+[ ]\d{7,}"
    return bool(re.fullmatch(pattern, number))


def clear_number(number):
    """Clear."""
    number2 = ""
    for i in number:
        if i.isdigit() or i == "+" or i == " ":
            number2 += i
    return number2


def length_of_digits(number):
    """Len."""
    len_of_digits = ''
    for n in number:
        if n.isdigit():
            len_of_digits += n
    return len_of_digits


def help_fun(number):
    """Help with style."""
    country_code = ""
    number_without_country_code = ""

    if number.startswith("+"):
        country_code += "+"

        number_list = number.split()
        for symbol in number_list[0]:
            if symbol.isdigit():
                country_code += symbol

        if len(number_list) > 1:
            for part in number_list[1:]:
                for symbol in part:
                    if symbol.isdigit():
                        number_without_country_code += symbol

    return country_code, number_without_country_code


def remove_unnecessary_chars(number: str) -> str:
    """Remove unnecessary."""
    number = number.strip()  # clear of spaces
    number = clear_number(number)  # remain only numbers, + and " "

    number = re.sub(r'(?<=\+)\s+', '', number)  # cleared from spaces after +

    result = ""
    len_of_digits = length_of_digits(number)

    country_code, number_without_country_code = help_fun(number)

    if len(country_code) <= 1:
        return len_of_digits

    if len(number_without_country_code) == 0:
        result = country_code[1:]
        return result

    if len(country_code) >= 2:
        result = country_code + " " + number_without_country_code
        return result

    return result


def get_last_numbers(numbers: list[str], n: int) -> list[str]:
    """Get numbers."""
    if n <= 0:
        return []
    elif n > len(numbers):
        return numbers
    else:
        return numbers[len(numbers) - n:]


def get_first_correct_number(names: list[str], numbers: list[str], name: str) -> str | None:
    """Get first."""
    name = name.lower()
    names_lower = []
    for n in names:
        names_lower.append(n.lower())

    for index, n in enumerate(names_lower):
        if n == name:
            phone_number = numbers[index]
            if is_valid(phone_number):
                return phone_number
    return None


def correct_numbers(numbers: list[str]) -> list[str]:
    """Correct num."""
    list_of_correct = []
    for num in numbers:
        if is_valid(num):
            list_of_correct.append(num)
        else:
            num = remove_unnecessary_chars(num)
            if is_valid(num):
                list_of_correct.append(num)
            else:
                num = add_country_code(num)
                if is_valid(num):
                    list_of_correct.append(num)
    return list_of_correct


def get_names_of_contacts_with_correct_numbers(names: list[str], numbers: list[str]) -> list[str]:
    """Get names."""
    names_capitalize = []
    for n in names:
        names_capitalize.append(n.title())

    correct_names = []

    for index, num in enumerate(numbers):
        if is_valid(num):
            correct_names.append(names_capitalize[index])
    return correct_names