"""Phone inventory."""


def list_of_phones(all_phones: str) -> list:
    """
    Return list of phones.

    The input string contains of phone brands and models, separated by comma.
    Both the brand and the model do not contain spaces (both are one word).
    """
    models_and_brands_list = []
    model_and_brand_str = ""
    for i, symbol in enumerate(all_phones):
        last_index = len(all_phones) - 1
        if symbol == "," or i == last_index:
            if i == last_index:
                model_and_brand_str += symbol
            models_and_brands_list.append(model_and_brand_str)
            model_and_brand_str = ""
        else:
            model_and_brand_str += symbol
    return models_and_brands_list


def phone_brands(all_phones: str) -> list:
    """
    Return list of unique phone brands.

    The order of the elements should be the same as in the input string (first appearance).
    """
    if not all_phones:
        return []

    full_brand_list = []
    array_of_phones = list_of_phones(all_phones)

    for element in array_of_phones:
        name_of_brand = element.split(" ")[0]
        if name_of_brand not in full_brand_list:
            full_brand_list.append(name_of_brand)
    return full_brand_list


def phone_models(all_phones: str) -> list:
    """
    Return list of unique phone models.

    The order of the elements should be the same as in the input string (first appearance).
    """
    if not all_phones:
        return []

    full_model_list = []
    array_of_phones = list_of_phones(all_phones)

    for element in array_of_phones:
        name_of_model_list = element.split(" ")[1:]
        name_of_model = " ".join(name_of_model_list)
        if name_of_model not in full_model_list:
            full_model_list.append(name_of_model)
    return full_model_list


def search_by_brand(all_phones: str, brand: str) -> list:
    """
    Search for phones by brand.

    The search is case-insensitive.
    """
    search_list = []
    array_of_phones = list_of_phones(all_phones)
    brand = brand.lower()

    def find_brand(phone_full_name: str) -> str:
        """Find the brand on the phone."""
        brand_name = phone_full_name.split(" ")[0]
        return brand_name

    for phone in array_of_phones:
        phone_brand = find_brand(phone)
        if brand == phone_brand.lower():
            search_list.append(phone)
    return search_list


def search_by_model(all_phones: str, model: str) -> list:
    """
    Search for phones by model.

    The search is case-insensitive.
    """
    found_phones_list = []
    model = model.lower()
    array_of_phones = list_of_phones(all_phones)

    if " " in model:  # more than one word
        return []

    def find_model(phone_full_name: str) -> str:
        """Find the model on the phone."""
        model_name_list = phone_full_name.split(" ")[1:]
        model_name = " ".join(model_name_list)
        return model_name

    for phone in array_of_phones:
        phone_model = find_model(phone)
        split_phone_model_array = phone_model.split(" ")

        for model_part in split_phone_model_array:
            if model_part.lower() == model:  # check the part of the model_name "pro 14 max" -> "pro", "14", "max"
                found_phones_list.append(phone)

    return found_phones_list


if __name__ == '__main__':
    print(list_of_phones("Google Pixel,Honor Magic5,Google Pixel,IPhone 12"))
    # ["Google Pixel', 'Honor Magic5', 'Google Pixel"]

    print(phone_brands("Google Pixel,Honor Magic5,Google Pix,Honor Magic6,IPhone 12,Samsung S10,Honor Magic,IPhone 11"))
    # ['Google', 'Honor', 'IPhone', 'Samsung']
    print(phone_brands("Google Pixel,Google Pixel,Google Pixel,Google Pixel"))
    # ['Google']
    print(phone_brands(""))
    # []

    print(phone_models("IPhone 14,Google Pixel,Honor Magic5,IPhone 14"))
    # ['14', 'Pixel', 'Magic5']
    print(phone_models("IPhone 14 A,Google Pixel B,Honor Magic5,IPhone 14"))
    # ['14 A', 'Pixel B', 'Magic5', '14']
    print(phone_models("LG Optimus Black"))
    # ['Optimus Black']

    print(search_by_brand("Google Pixel,GOOGLE Pixel,GooGle Pixel,GooGLE Pixel2,google Pixel 2022,nongoogle pixel",
                          "google"))
    # ['Google Pixel', 'GOOGLE Pixel', 'GooGle Pixel', 'GooGLE Pixel2', 'google Pixel 2022']

    print(search_by_model("Google Pixel,Google Pixel", "Pixel"))
    # ['Google Pixel']
    print(search_by_model("IPhone 12 Pro,IPhone proX,IPhone 14 pro Max,IPhone 14 pro Max", "pro"))
    # ['IPhone 12 Pro', 'IPhone 14 pro Max']
    print(search_by_model("IPhone proX,IPhone 12 Pro,IPhone 14 pro Max", "1"))  # piece of word
    # []
    print(search_by_model("IPhone proX,IPhone 12 Pro,IPhone 14 pro Max", "IPhone"))  # brand
    # []
    print(search_by_model("IPhone proX,IPhone 12 Pro,IPhone 14 pro Max", "12 Pro"))  # more than one word
    # []
    print(search_by_model("IPhone X,IPhone 12 Pro,IPhone 12 Pro,IPhone 14 pro Max", "Pro"))
    # ['IPhone 12 Pro', 'IPhone 12 Pro', 'IPhone 14 pro Max']
