"""EX01 ATM."""

amount = int(input("Enter a sum: "))

total_banknotes = [1, 5, 10, 20, 50, 100]
# Reverse because it will be easier for our logic
total_banknotes.reverse()

used_banknotes = []


# Banknotes logic with array
# Collect the list of banknotes by recursion function
# the docstring was written by AI

def add_the_highest_banknote(money, iterator):
    """Recursively adds the highest banknotes possible to cover the given amount.

    Args:
        money (int): The amount of money to cover.
        iterator (int): The current index in the total_banknotes list.
    """
    if money <= 0 or iterator >= len(total_banknotes):
        return

    remaining_amount = money
    the_highest_banknote = total_banknotes[iterator]

    # If we can use the_highest_banknote, call the function again with the remaining money and with the same iterator
    if remaining_amount >= the_highest_banknote:
        used_banknotes.append(the_highest_banknote)
        remaining_amount -= the_highest_banknote
        add_the_highest_banknote(remaining_amount, iterator)
    # Change the iterator and call the function again
    else:
        iterator += 1
        add_the_highest_banknote(remaining_amount, iterator)


# Call the function

add_the_highest_banknote(amount, 0)

# Result
banknotes = len(used_banknotes)
print(f"Amount of banknotes needed: {banknotes}")
