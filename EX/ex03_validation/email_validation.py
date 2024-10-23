"""Email validation."""


def has_at_symbol(email: str) -> bool:
    """Find @ sign in the email."""
    return "@" in email


def is_valid_username(email: str) -> bool:
    """Check the username from the email."""
    # Check if email contains @ sign
    if not has_at_symbol(email):
        return False

    # Split the email by @
    split_email = email.split("@")
    if len(split_email) != 2:
        return False

    username_part = split_email[0]
    username_part_without_dots = username_part.replace(".", "")

    # Check if username contains only allowed characters (letters and dots)
    for symbol in username_part_without_dots:
        if not symbol.isalnum():
            return False
    else:
        return True


def find_domain(email: str) -> str:
    """Find the domain in the email."""
    if not has_at_symbol(email):
        return ""

    split_email = email.split("@")  # return arr
    return split_email[-1]


def is_valid_domain(email: str) -> bool:
    """Check the domain in the email."""
    domain = find_domain(email)

    # split the domain by "." if more than one -> False
    split_domain = domain.split(".")  # return arr
    if len(split_domain) != 2:
        return False

    # if domain has special char -> False
    for part in split_domain:
        if not part.isalpha():
            return False

    # if not 3 <= split_domain[0].length <= 10 -> False
    if not 3 <= len(split_domain[0]) <= 10:
        return False

    # if not 2 <= split_domain[1] <= 5 -> False
    if not 2 <= len(split_domain[1]) <= 5:
        return False
    else:
        return True


def is_valid_email_address(email: str) -> bool:
    """Validate the email."""
    return is_valid_username(email) and is_valid_domain(email)


def create_email_address(domain: str, username: str) -> str:
    """Create a valid email."""
    email = username + "@" + domain

    if is_valid_email_address(email):
        return email
    else:
        return "Cannot create a valid email address using the given parameters!"


if __name__ == '__main__':
    print("Email has the @ symbol:")
    print(has_at_symbol("joonas.kivi@gmail.com"))  # -> True
    print(has_at_symbol("joonas.kivigmail.com"))  # -> False

    print("\nUsername has no special symbols:")
    print(is_valid_username("martalumi@taltech.ee"))  # -> True
    print(is_valid_username("marta.lumi@taltech.ee"))  # -> True
    print(is_valid_username("marta lumi@taltech.ee"))  # -> False
    print(is_valid_username("marta&lumi@taltech.ee"))  # -> False
    print(is_valid_username("marta@lumi@taltech.ee"))  # -> False
    print(is_valid_username("martalu.mit.alt@eche,,.e"))  # -> True
    print(is_valid_username("martalu.mit.....alt@eche,,.e"))  # -> True
    print(is_valid_username("123marta@taltech.ee"))  # -> True

    print("\nFind the email domain name:")
    print(find_domain("karla.karu@saku.ee"))  # -> saku.ee
    print(find_domain("karla.karu@taltech.ee"))  # -> taltech.ee
    print(find_domain("karla.karu@yahoo.com"))  # -> yahoo.com
    print(find_domain("karla@karu@yahoo.com"))  # -> yahoo.com
    print(find_domain("karlakaruyahoo.com"))  # -> ""

    print("\nCheck if the domain is correct:")
    print(is_valid_domain("pihkva.pihvid@ttu.ee"))  # -> True
    print(is_valid_domain("metsatoll@&gmail.com"))  # -> False
    print(is_valid_domain("ewewewew@i.u.i.u.ewww"))  # -> False
    print(is_valid_domain("pannkookm.oos"))  # -> False
    print(is_valid_domain("pannkookm@ofo.cos"))  # -> True

    print("\nIs the email valid:")
    print(is_valid_email_address("DARJA.darja@gmail.com"))  # -> True
    print(is_valid_email_address("DARJA=darjamail.com"))  # -> False

    print("\nCreate your own email address:")
    print(create_email_address("hot.ee", "vana.ema"))  # -> vana.ema@hot.ee
    print(create_email_address("jaani.org", "lennakuurma"))  # -> lennakuurma@jaani.org
    print(create_email_address("koobas.com",
                               "karu&pojad"))  # -> Cannot create a valid email address using the given parameters!
