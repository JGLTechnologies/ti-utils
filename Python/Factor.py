from UTILS import *

gcf = 0
monomial_factors = 0


def get_factors(n):
    if n == 0:
        return set()
    n = abs(n)
    factors = set()
    for i in range(1, int(n**0.5) + 1):
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


def factor_polynomial(coeffs):
    global monomial_factors
    if len(coeffs) <= 1:
        return [coeffs]

    # Check for monomial factor
    while coeffs[-1] == 0 and len(coeffs) > 1:
        coeffs = coeffs[:-1]
        monomial_factors += 1
    if len(coeffs) <= 1:
        return

    # Factor by grouping if there are 4 terms
    if len([c for c in coeffs if c != 0]) == 4:
        terms = get_terms(coeffs)

        group_1 = terms[0:2]
        max_power_1 = terms[1][1]
        coeffs_1 = get_coeffs(
            [
                [group_1[0][0], group_1[0][1] - max_power_1],
                [group_1[1][0], group_1[1][1] - max_power_1],
            ]
        )
        gcf_1 = calculate_gcf(coeffs_1)
        if coeffs_1[0] < 0:
            gcf_1 *= -1
        group_1 = [g / gcf_1 for g in coeffs_1]

        group_2 = terms[2:4]
        max_power_2 = terms[3][1]
        coeffs_2 = get_coeffs(
            [
                (group_2[0][0], group_2[0][1] - max_power_2),
                (group_2[1][0], group_2[1][1] - max_power_2),
            ]
        )
        gcf_2 = calculate_gcf(coeffs_2)
        if coeffs_2[0] < 0:
            gcf_2 *= -1
        group_2 = [g / gcf_2 for g in coeffs_2]

        if group_1 == group_2:
            for factor in factor_polynomial(
                get_coeffs([[gcf_1, max_power_1], [gcf_2, max_power_2]])
            ):
                yield factor
            for factor in factor_polynomial(group_1):
                yield factor
            return

    # Use Rational Root Theorem and long division to find linear factors
    roots = rational_roots(coeffs)
    for root in roots:
        a, b = get_frac(root)
        quotient, remainder = divide(coeffs, [b, -a])
        if len(remainder) == 0:
            yield [1, -root]
            for factor in factor_polynomial(quotient):
                yield factor
            return

    yield coeffs


def format_factors(factors):
    global gcf
    formatted_factors = []
    for factor in factors:
        # Check for any remaining gcf
        g = calculate_gcf(factor)
        gcf *= g
        factor = [coeff / g for coeff in factor]
        if len(factor) == 2 and factor[0] == 1:
            root = -factor[1]
            a, b = get_frac(root)
            if a < 0 and b < 0:
                a = abs(a)
                b = abs(b)
            elif b < 0:
                a = -a
                b = abs(b)
            formatted_factors.append("(" + format_polynomial([b, -a]) + ")")
        else:
            formatted_factors.append("(" + format_polynomial(factor) + ")")
    return "".join(formatted_factors)


def main():
    global gcf
    input_str = input("Enter the polynomial: ")
    try:
        coeffs = input_to_list(input_str)
    except ValueError:
        print("Invalid input")
        main()
        return
    t = get_terms(coeffs)
    if len(t) > 0 and t[0][1] == 0:
        print(t[0][0])
        return
    elif coeffs[0] == 0:
        print(0.0)
        return
    gcf = calculate_gcf(coeffs)
    # Factor out gcf
    normalized_coeffs = [coeff / gcf for coeff in coeffs]
    # Make leading coefficient positive
    if normalized_coeffs[0] < 0:
        normalized_coeffs = [-coeff for coeff in normalized_coeffs]
        gcf = -gcf
    factors = list(factor_polynomial(normalized_coeffs))
    if monomial_factors > 0:
        factors = [get_coeffs([(1, monomial_factors)])] + factors
    formatted_factors = format_factors(factors)
    if gcf != 1:
        formatted_factors = "{}{}".format(gcf, formatted_factors)
    print(formatted_factors)


main()
