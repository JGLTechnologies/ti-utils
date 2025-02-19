from UTILS import *
from UTILS_2 import *

gcf = 0
monomial_factors = 0


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

    # Perfect square trinomial
    if len([c for c in coeffs if c != 0]) == 3:
        terms = get_terms(coeffs)
        if (
            terms[0][1] == 2 * terms[1][1]
            and terms[2][1] == 0
            and terms[0][0] > 0
            and terms[2][0] > 0
            and is_int(terms[0][0] ** 0.5)
            and is_int(terms[2][0] ** 0.5)
            and abs(terms[1][0]) == 2 * terms[0][0] ** 0.5 * terms[2][0] ** 0.5
        ):
            power = int(terms[0][1] / 2)
            sign = -1 if terms[1][0] < 0 else 1
            a = terms[0][0] ** 0.5
            b = terms[2][0] ** 0.5
            for factor in factor_polynomial(get_coeffs([(a, power), (sign * b, 0)])):
                yield factor
            for factor in factor_polynomial(get_coeffs([(a, power), (sign * b, 0)])):
                yield factor
            return

    # Difference of 2 squares
    if len([c for c in coeffs if c != 0]) == 2:
        terms = get_terms(coeffs)
        if (
            terms[0][1] % 2 == 0
            and terms[1][1] % 2 == 0
            and is_int(abs(terms[0][0]) ** 0.5)
            and is_int(abs(terms[1][0]) ** 0.5)
            and terms[1][0] < 0
        ):
            a = terms[0][0] ** 0.5
            b = abs(terms[1][0]) ** 0.5
            power_a = int(terms[0][1] / 2)
            power_b = int(terms[1][1] / 2)
            for factor in factor_polynomial(get_coeffs([(a, power_a), (b, power_b)])):
                yield factor
            for factor in factor_polynomial(get_coeffs([(a, power_a), (-b, power_b)])):
                yield factor
            return

    # Factor by grouping if there are 4 terms
    if len([c for c in coeffs if c != 0]) == 4:
        terms = get_terms(coeffs)
        group_1 = terms[0:2]
        max_power_1 = terms[1][1]
        coeffs_1 = get_coeffs(
            [
                (group_1[0][0], group_1[0][1] - max_power_1),
                (group_1[1][0], group_1[1][1] - max_power_1),
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
                get_coeffs([(gcf_1, max_power_1), (gcf_2, max_power_2)])
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
