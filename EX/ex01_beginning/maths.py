"""EX01 Maths."""

# Task 1
a = int(input("Enter the value of a: "))
b = int(input("Enter the value of b: "))
c = int(input("Enter the value of c: "))
d = int(input("Enter the value of d: "))

# Multiplication logic
b *= 2
c *= 3
d *= 4

# Average value
result = float((a + b + c + d) / 4)
print(result)

# Task 2
x = int(input("Enter the value of x: "))
y = int(input("Enter the value of y: "))
u = int(input("Enter the value of u: "))
t = int(input("Enter the value of t: "))

# Fraction math logic
denominator = y * t
numerator1 = x * t
numerator2 = y * u
numerators_sum = numerator1 + numerator2
final_fraction = f"{numerators_sum}/{denominator}"
print(final_fraction)

# Task 3
ects = int(input("Enter the amount of ECTS: "))
weeks = int(input("Enter the number of weeks: "))

if ects == 0:
    print(0)
elif weeks == 0:
    print(-1)
else:
    # Calculation logic
    required_hours = ects * 26
    working_hours_per_week = required_hours // weeks

    # Check how many hours we have
    one_week = 24 * 7
    available_hours = one_week * weeks

    # Check the possibility
    if required_hours <= available_hours:
        print(working_hours_per_week)
    else:
        print(-1)
