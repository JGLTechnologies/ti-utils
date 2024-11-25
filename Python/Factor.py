from UTILS import *

gcf = 0

def get_frac(decimal):
    max_denominator = 1000000
    integer_part = int(decimal)
    decimal_part = decimal - integer_part

    if decimal_part == 0:
        return integer_part, 1

    a0 = int(decimal_part)
    p0, q0 = 0, 1
    p1, q1 = 1, a0

    # Use a small epsilon value to avoid division by zero due to floating-point precision issues
    epsilon = 1e-10

    while True:
        if abs(decimal_part - a0) < epsilon:
            break

        decimal_part = 1 / (decimal_part - a0)
        a0 = int(decimal_part)
        p2 = a0 * p1 + p0
        q2 = a0 * q1 + q0

        if q2 > max_denominator:
            break

        p0, q0 = p1, q1
        p1, q1 = p2, q2

    numerator = integer_part * q1 + p1
    denominator = q1

    return numerator, denominator


def input_to_list(input_str):
    return [float(num) for num in input_str.split(',')]


def factors(n):
    return set(x for i in range(1, abs(n) + 1) if n % i == 0 for x in (i, -i))


def rational_roots(coeffs):
    p = factors(int(coeffs[-1]))  # Factors of the constant term
    q = factors(int(coeffs[0]))  # Factors of the leading coefficient
    roots = set(px/qx for px in p for qx in q if qx != 0)
    return roots


def gcd(a, b):
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
    return reduce(gcd, int_coeffs)


def factor_polynomial(coeffs):
    if len(coeffs) <= 1:
        return [coeffs]

    # Check for monomial factor
    while coeffs[-1] == 0 and len(coeffs) > 1:
        coeffs = coeffs[:-1]
        yield [1, 0]
    if len(coeffs) <= 1:
        return

    # Factor by grouping if there are 4 terms
    if len([c for c in coeffs if c != 0]) == 4:
        terms = get_terms(coeffs)

        group_1 = terms[0:2]
        max_power_1 = terms[1][1]
        coeffs_1 = get_coeffs([[group_1[0][0], group_1[0][1]-max_power_1], [group_1[1][0], group_1[1][1]-max_power_1]])
        gcf_1 = calculate_gcf(coeffs_1)
        if coeffs_1[0] < 0:
            gcf_1*=-1
        group_1 = [g / gcf_1 for g in coeffs_1]

        group_2 = terms[2:4]
        max_power_2 = terms[3][1]
        coeffs_2 = get_coeffs([(group_2[0][0], group_2[0][1] - max_power_2), (group_2[1][0], group_2[1][1] - max_power_2)])
        gcf_2 = calculate_gcf(coeffs_2)
        if coeffs_2[0] < 0:
            gcf_2*=-1
        group_2 = [g / gcf_2 for g in coeffs_2]

        if group_1 == group_2:
            yield get_coeffs([[gcf_1, max_power_1], [gcf_2, max_power_2]])
            yield group_1
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
            formatted_factors.append('(' + format_polynomial([b, -a]) + ')')
        else:
            formatted_factors.append('(' + format_polynomial(factor) + ')')
    return ''.join(formatted_factors)


def main():
    global gcf
    input_str = input("Enter the polynomial: ")
    coeffs = input_to_list(input_str)
    gcf = calculate_gcf(coeffs)
    # Factor out gcf
    normalized_coeffs = [coeff / gcf for coeff in coeffs]
    # Make leading coefficient positive
    if normalized_coeffs[0] < 0:
        normalized_coeffs = [-coeff for coeff in normalized_coeffs]
        gcf = -gcf
    factors = list(factor_polynomial(normalized_coeffs))
    formatted_factors = format_factors(factors)
    if gcf != 1:
        formatted_factors = "{}{}".format(gcf, formatted_factors)
    print(formatted_factors)


main()