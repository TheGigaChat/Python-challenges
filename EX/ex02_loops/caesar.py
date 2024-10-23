"""Caesar cipher."""

import re
import string

# global init
alphabet_array = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z'
]


def create_new_index(old_index: int, shift: int) -> int:
    """Create new index in the range od the alphabet."""
    new_index = old_index + shift

    while new_index >= len(alphabet_array):
        new_index -= len(alphabet_array)

    return new_index


def encode(message: str, shift: int) -> str:
    """
    Encode a message using a Caesar cipher.

    Presume the message is already lowercase.
    For each letter of the message, shift it forward in the alphabet by shift amount.
    If the character isn't a letter, keep it the same.

    For example, shift = 3 then a => d, b => e, z => c (see explanation below)

    Shift:    0 1 2 3
    Alphabet:       A B C D E F G H I J
    Result:   A B C D E F G H I J

    Examples:
    1. encode('i like turtles', 6) == 'o roqk zaxzrky'
    2. encode('example', 1) == 'fybnqmf'
    3. encode('the quick brown fox jumps over the lazy dog.', 7) == 'aol xbpjr iyvdu mve qbtwz vcly aol shgf kvn.'

    :param message: message to be encoded
    :param shift: shift for encoding
    :return: encoded message
    """
    # init
    pattern_for_lower_letters = "[a-z]"
    new_message_array = []
    new_message = ""

    # logic
    for letter in message:
        if re.search(pattern_for_lower_letters, letter):  # symbol is letter
            old_index = alphabet_array.index(letter)
            new_index = create_new_index(old_index, shift)
            new_message_array.append(alphabet_array[new_index])
        else:
            new_message_array.append(letter)

    # result
    for letter in new_message_array:
        new_message += letter
    return new_message


if __name__ == '__main__':
    print(encode("i like turtles", 6))  # -> o roqk zaxzrky
    print(encode("o roqk zaxzrky", 20))  # -> i like turtles
    print(encode("example", 1))  # -> fybnqmf
    print(encode("don't change", 0))  # -> don't change
    print(encode('the quick brown fox jumps over the lazy dog.', 7))  # -> aol xbpjr iyvdu mve qbtwz vcly aol shgf kvn.
