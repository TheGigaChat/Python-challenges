"""Entry."""
import re


def parse(row: str) -> tuple:
    """
    Parse string row into a tuple.

    The row has a first name, last name, ID code, phone number, date of birth and address.
    Only ID code is mandatory, other values may not be included.

    They can be found by the following rules:
    - Both the first name and last name begin with a capital letter and are followed by at least one lowercase letter
    - ID code is an 11-digit number
    - Phone number has the same rules applied as in the first part
    - Date of birth is in the form of dd-MM-YYYY
    - Address is everything else that's left

    :param row: given string to find values from
    :return: tuple of values found in given string
    """
    name_pattern = r"^([A-ZÖÜÄÕ][a-zöüõä]+)"
    name = re.match(name_pattern, row)
    if name:
        name = name.group(0)
        row = row.replace(name, "")
        print(name)
    else:
        name = None

    surname_pattern = r"([A-ZÖÜÄÕ][a-zöüõä]+)(?=\d{11})"
    surname = re.match(surname_pattern, row)
    if surname:
        surname = surname.group(0)
        row = row.replace(surname, "")
        print(surname)
    else:
        surname = None

    user_id_pattern = r"(\d{11})"
    user_id = re.search(user_id_pattern, row).group(0)
    row = row.replace(user_id, "")
    print(user_id)

    phone_num_pattern = r"((\+[\d]{3})?(?: )?(\d{7,8}))"
    phone_num = re.search(phone_num_pattern, row)
    if phone_num:
        phone_num = phone_num.group(0)
        row = row.replace(phone_num, "")
        print(phone_num)
    else:
        phone_num = None

    user_birthday_pattern = r"(\d\d-\d\d-\d\d\d\d)"
    user_birthday = re.search(user_birthday_pattern, row)
    if user_birthday:
        user_birthday = user_birthday.group(0)
        row = row.replace(user_birthday, "")
        print(user_birthday)
    else:
        user_birthday = None

    user_address = row
    if user_address:
        print(user_address)
    else:
        user_address = None

    split_data_tuple = (name, surname, user_id, phone_num, user_birthday, user_address)
    return split_data_tuple


if __name__ == '__main__':
    print(parse('PriitPann39712047623+372 5688736402-12-1998Oja 18-2,Pärnumaa,Are'))
    # ('Priit', 'Pann', '39712047623', '+372 56887364', '02-12-1998', 'Oja 18-2,Pärnumaa,Are')
    print()
    print(parse('39712047623+372 5688736402-12-1998Oja 18-2,Pärnumaa,Are'))
    # (None, None, '39712047623', '+372 56887364', '02-12-1998', 'Oja 18-2,Pärnumaa,Are')
    print()
    print(parse('PriitPann3971204762302-12-1998Oja 18-2,Pärnumaa,Are'))
    # ('Priit', 'Pann', '39712047623', None, '02-12-1998', 'Oja 18-2,Pärnumaa,Are')
    print()
    print(parse('PriitPann39712047623+372 56887364Oja 18-2,Pärnumaa,Are'))
    # ('Priit', 'Pann', '39712047623', '+372 56887364', None, 'Oja 18-2,Pärnumaa,Are')
    print()
    print(parse('39712047623'))
    # (None, None, '39712047623', None, None, None)
    print()
    print(parse('Pann39712047623'))
    # (None, Pann, '39712047623', None, None, None) ???
