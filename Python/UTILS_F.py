def is_int(x):
    if isinstance(x, int):
        return True
    return int(str(x).split(".")[1]) == 0


def get_frac(decimal, max_denominator=1000000):
    # Handle sign of the decimal
    is_negative = decimal < 0
    decimal = abs(decimal)

    # Split the integer and fractional parts
    integer_part = int(decimal)
    fractional_part = decimal - integer_part

    if fractional_part == 0:
        return -integer_part if is_negative else integer_part, 1

    # Initialize continued fraction variables
    num1, denom1 = 1, 0
    num2, denom2 = integer_part, 1

    while True:
        fractional_part = 1 / fractional_part
        next_term = int(fractional_part)
        fractional_part -= next_term

        # Calculate next numerator and denominator
        num_next = next_term * num2 + num1
        denom_next = next_term * denom2 + denom1

        if denom_next > max_denominator:
            # Adjust to stay within max_denominator
            scale = (max_denominator - denom1) // denom2
            num_next = num1 + scale * num2
            denom_next = denom1 + scale * denom2
            break

        num1, denom1 = num2, denom2
        num2, denom2 = num_next, denom_next

        if fractional_part == 0:
            break

    numerator = num_next
    denominator = denom_next
    if is_negative:
        numerator = -numerator

    return numerator, denominator


def get_factors(n):
    if n == 0:
        return set()
    n = abs(n)
    factors = set()
    for i in range(1, int(n ** 0.5) + 1):
        if n % i == 0:
            factors.add(i)
            factors.add(-i)
            factors.add(n // i)
            factors.add(-(n // i))
    return factors


def rational_roots(coeffs):
    p = get_factors(int(coeffs[-1]))  # Factors of the constant term
    q = get_factors(int(coeffs[0]))  # Factors of the leading coefficient
    roots = set(px / qx for px in p for qx in q if qx != 0)
    return roots


def get_gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return abs(a)


def reduce(function, iterable, initializer=None):
    it = iter(iterable)
    value = initializer if initializer is not None else next(it)
    for element in it:
        value = function(value, element)
    return value


def calculate_gcf(coeffs):
    int_coeffs = [int(c) for c in coeffs if c != 0]
    return reduce(get_gcd, int_coeffs)
