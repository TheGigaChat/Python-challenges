"""Some cool pyramids."""


def create_simple_pyramid_left(height: int, i=1) -> str:
    """
    Create simple pyramid on the left side.

    *
    **
    ***
    ****

    Use recursion!

    :param height: Pyramid height.
    :param i: Keeping track of current layer.
    :return: Pyramid.
    """
    if i <= height:
        return "*" * i + "\n" + create_simple_pyramid_left(height, i + 1)
    else:
        return ""


def create_simple_pyramid_right(height: int, i=1) -> str:
    """
    Create simple pyramid on the right side.

       *
      **
     ***
    ****

    Use recursion!

    :param height: Pyramid height.
    :param i: Keeping track of current layer.
    :return: Pyramid.
    """
    if i <= height:
        return f"{'*' * i}".rjust(height) + "\n" + create_simple_pyramid_right(height, i + 1)
    else:
        return ""


def create_number_pyramid_left(height: int, i=1, num="1") -> str:
    """
    Create left-aligned number pyramid.

    1
    12
    123
    1234

    Use recursion!

    :param height: Pyramid height.
    :param i: Keeping track of current layer.
    :param num: Keeping track of current layer.
    :return: Pyramid.
    """
    if i <= height:
        return num + "\n" + create_number_pyramid_left(height, i + 1, num + str(i + 1))
    else:
        return ""


def create_number_pyramid_right(height: int, i=1, num="1") -> str:
    """
    Create right-aligned number pyramid.

        1
       21
      321
     4321

    Use recursion!

    :param height: Pyramid height.
    :param i: Keeping track of current layer.
    :return: Pyramid.
    """
    concat_sum = ""
    for n in range(1, height + 1):
        concat_sum += str(n)

    margin_left = len(concat_sum)

    if i <= height:
        return num.rjust(margin_left) + "\n" + create_number_pyramid_right(height, i + 1, str(i + 1) + num)
    else:
        return ""


def create_number_pyramid_left_down(height: int) -> str:
    """
    Create left-aligned number pyramid upside-down.

    4321
    321
    21
    1

    Use recursion!

    :param height: Pyramid height.
    :return: Pyramid.
    """
    concat_sum = ""
    for n in range(1, height + 1):
        concat_sum = str(n) + concat_sum

    if height > 0:
        return concat_sum + "\n" + create_number_pyramid_left_down(height - 1)
    else:
        return ""


def create_number_pyramid_right_down(height: int, i=1) -> str:
    """
    Create right-aligned number pyramid upside-down.

    1234
     123
      12
       1

    Use recursion!

    :param height: Pyramid height.
    :param current: Keeping track of current layer.
    :return: Pyramid.
    """
    margin_coefficient = 0
    concat_sum = ""
    for n in range(1, height + 1):
        concat_sum += str(n)
        if n == height:
            margin_coefficient = len(str(n))

    if height > 0:
        whitespaces = " " * (i - 1)
        if whitespaces == "":
            return concat_sum + create_number_pyramid_right_down(height - 1, i + margin_coefficient)
        else:
            return "\n" + whitespaces + concat_sum + create_number_pyramid_right_down(height - 1, i + margin_coefficient)
    else:
        return ""


def create_regular_pyramid(height: int, i=1) -> str:
    """
    Create regular pyramid.

       *
      ***
     *****
    *******

    Use recursion!

    :param height: Pyramid height.
    :param i: Keeping track of current layer.
    :return: Pyramid.
    """
    if height == 0:
        return ""

    if i <= height:
        width = 1 + 2 * (height - 1)
        multiplier = 1 + 2 * (i - 1)
        stars = '*' * multiplier
        return f"{stars:^{width}}".rstrip() + "\n" + create_regular_pyramid(height, i + 1)
    else:
        return ""


def create_regular_pyramid_upside_down(height: int, i=1, width=0) -> str:
    """
    Create regular pyramid upside down.

    *******
     *****
      ***
       *

    Use recursion!

    :param height: Pyramid height.
    :param i: Keeping track of current layer.
    :param width: Width of the pyramid.
    :return: Pyramid.
    """
    if height == 0:
        return ""

    if i == 1:
        width = 1 + 2 * (height - 1)
    if height > 0:
        multiplier = 1 + 2 * (height - 1)
        stars = '*' * multiplier
        return f"{stars:^{width}}".rstrip() + "\n" + create_regular_pyramid_upside_down(height - 1, i + 1, width)
    else:
        return ""


def create_diamond(height: int, i=1, width=0, pyramid="") -> str:
    """
    Create diamond.

       *
      ***
     *****
    *******
    *******
     *****
      ***
       *

    Use recursion!

    :param height: Height of half of the diamond.
    :param i: Keeping track of current layer.
    :param width: Width of the pyramid.
    :param pyramid: The result of each iteration.
    :return: Diamond.
    """
    if height == 0:
        return pyramid

    if height > 0:
        if i == 1:
            width = 1 + 2 * (height - 1)

        multiplier = 1 + 2 * (height - 1)
        stars = '*' * multiplier
        pyramid = f"{stars:^{width}}".rstrip() + "\n" + pyramid + f"{stars:^{width}}".rstrip() + "\n"

        return create_diamond(height - 1, i + 1, width, pyramid)


def create_empty_pyramid(height: int, i=1, pyramid="") -> str:
    """
    Create empty pyramid.

       *
      * *
     *   *
    *******

    Use recursion!

    :param height: Pyramid height.
    :param i: Keeping track of current layer.
    :param pyramid: The result of each iteration.
    :return: Pyramid.
    """
    if height == 0:
        return ""

    if i <= height:
        width = 1 + 2 * (height - 1)
        multiplier = 1 + 2 * (i - 1)

        if multiplier == 1 or multiplier == width:
            stars = '*' * multiplier
        else:
            stars = '*' + ' ' * (multiplier - 2) + '*'

        pyramid += f"{stars:^{width}}".rstrip() + "\n"
        return create_empty_pyramid(height, i + 1, pyramid)
    else:
        return pyramid


# if __name__ == '__main__':
    # print("\ncreate_simple_pyramid_left:")
    # print("expected:\n*\n**\n***\n****")
    # print(f"\ngot:\n{create_simple_pyramid_left(4)}")
    #
    # print("\ncreate_simple_pyramid_right:")
    # print("expected:\n   *\n  **\n ***\n****")
    # print(f"\ngot:\n{create_simple_pyramid_right(4)}")
    #
    # print("\ncreate_number_pyramid_left:")
    # print("expected:\n1\n12\n123\n1234")
    # print(f"\ngot:\n{create_number_pyramid_left(4)}")
    #
    # print("\ncreate_number_pyramid_right:")
    # print("expected:\n   1\n  21\n 321\n4321")
    # print(f"\ngot:\n{create_number_pyramid_right(4)}")
    #
    # print("\ncreate_number_pyramid_right_bigger_pyramid:")
    # print("expected:\n          1\n         21\n        321\n"
    #       "       4321\n      54321\n     654321\n    7654321\n"
    #       "   87654321\n  987654321\n 10987654321\n1110987654321")
    # print("Or expected:\n            1\n           21\n          321\n"
    #       "         4321\n        54321\n       654321\n      7654321\n"
    #       "     87654321\n    987654321\n  10987654321\n1110987654321")
    # print(f"\ngot:\n{create_number_pyramid_right(11)}")
    #
    # print("\ncreate_number_pyramid_left_down:")
    # print("expected:\n4321\n321\n21\n1")
    # print(f"\ngot:\n{create_number_pyramid_left_down(4)}")
    #
    # print("\ncreate_number_pyramid_right_down:")
    # print("expected:\n1234\n 123\n  12\n   1")
    # print(f"\ngot:\n{create_number_pyramid_right_down(4)}")
    #
    # print("\ncreate_number_pyramid_right_down_bigger_pyramid:")
    # print("expected:\n1234567891011\n 12345678910\n  123456789\n"
    #       "   12345678\n    1234567\n     123456\n      12345\n"
    #       "       1234\n        123\n         12\n          1")
    # print("Or expected:\n1234567891011\n  12345678910\n    123456789\n"
    #       "     12345678\n      1234567\n       123456\n        12345\n"
    #       "         1234\n          123\n           12\n            1")
    # print(f"\ngot:\n{create_number_pyramid_right_down(11)}")

    # print("\ncreate_regular_pyramid:")
    # print("expected:\n   *\n  ***\n *****\n*******")
    # print(f"\ngot:\n{create_regular_pyramid(4)}")

    # print("\ncreate_regular_pyramid_upside_down:")
    # print("expected:\n*******\n *****\n  ***\n   *")
    # print(f"\ngot:\n{create_regular_pyramid_upside_down(4)}")

    # print("\ncreate_diamond:")
    # print("expected:\n   *\n  ***\n *****\n*******\n*******\n *****\n  ***\n   *")
    # print(f"\ngot:\n{create_diamond(4)}")

    # print("\ncreate_empty_pyramid:")
    # print("expected:\n   *\n  * *\n *   *\n*******")
    # print(f"\ngot:\n{create_empty_pyramid(4)}")
