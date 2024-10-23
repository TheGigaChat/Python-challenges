"""Phone inventory vol 2."""


def add_phone_quantity(phone_info: tuple, update: tuple) -> tuple:
    """
    Update tuple, if updated data brand and model exist.

    Given a tuple containing a phone brand, its models, and quantities,
    and an update tuple, return the updated data or empty tuple if brand and/or model doesn't exist.
    """
    brand = phone_info[0]
    model_list = phone_info[1]
    quantity_list = list(phone_info[2])

    update_brand = update[0]
    update_model = update[1]
    update_quantity = update[2]

    final_list_initial = [brand, model_list[:], quantity_list[:]]
    final_list = [brand, model_list, quantity_list]

    if brand == update_brand:
        for index, model in enumerate(model_list):
            if model == update_model:
                quantity_list[index] += update_quantity

    if final_list_initial == final_list:
        final_list = []
    else:
        final_list[2] = tuple(final_list[2])

    final_tuple = tuple(final_list)
    return final_tuple


def highest_quantity_brand(phones: list[tuple]) -> str:
    """
    Find brand with most models.

    Given a tuple containing phone brand data, return the brand with the highest total quantity of models.
    If there is a tie, return the one that appears first in the input list.
    """
    if not phones:
        return ""

    max_quantity = 0
    max_quantity_index = 0
    for i, phone_info_tuple in enumerate(phones):
        quantity_of_models = sum(phone_info_tuple[2])  # => sum((500, 300))
        if quantity_of_models > max_quantity:
            max_quantity = quantity_of_models
            max_quantity_index = i

    brand_name = phones[max_quantity_index][0]
    return brand_name


def phone_list_as_string(phone_list: list) -> str:
    """
    Create a list of phones.

    The input list is in the same format as the result of phone_brand_and_models function.
    The order of the elements in the string is the same as in the list.
    """
    final_string = ""
    for phone in phone_list:
        for element_index, element in enumerate(phone):
            if type(element) is str:
                final_string += element + " "
            else:
                for i, model_part in enumerate(element):
                    final_string += model_part + ","
                    if i != element.index(element[-1]):  # find positive index using negative index
                        final_string += phone[0] + " "  # add brand + " "

    final_string = final_string[:-1]  # clear the last "," symbol
    return final_string


if __name__ == '__main__':
    print(add_phone_quantity(("Apple", ["iPhone 11", "iPhone 12"], (500, 300)),
                             ("Apple", "iPhone 11", 1)))
    # ("Apple", ["iPhone 11", "iPhone 12"], (501, 300))

    print(add_phone_quantity(("Apple", ["iPhone 11", "iPhone 12"], (500, 300)), ("Nokia", "3310", 10)))
    # ()

    print(highest_quantity_brand([("Apple", ["iPhone 11", "iPhone 12"], (500, 300)),
                                  ("Samsung", ["Galaxy S20", "Galaxy S21"], (600, 400)),
                                  ("Google", ["Pixel 4", "Pixel 5"], (200, 100))]))
    # Samsung

    print(highest_quantity_brand([("Apple", ["iPhone 11", "iPhone 12"], (100, 50)),
                                  ("Samsung", ["Galaxy S20", "Galaxy S21"], (110, 40)),
                                  ("Google", ["Pixel 4", "Pixel 5"], (70, 30))]))
    # Apple

    print(phone_list_as_string([['Google', ['Pixel', "Phone"]], ["Samsung", ["Galaxy S23", "3210"]]]))
    # Google Pixel,Google Phone,Samsung Galaxy S23,Samsung 3210
    print(phone_list_as_string([['IPhone', ['11']], ['Google', ['Pixel']]]))
    # IPhone 11,Google Pixel
    print(phone_list_as_string([['HTC', ['one']]]))
    # HTC one
