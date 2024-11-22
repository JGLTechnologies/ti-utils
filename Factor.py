from math import gcd
from functools import reduce


def input_to_list(input_str):
    """Convert a comma-separated string to a list of floats."""
    return [float(num) for num in input_str.split(',')]


def rational_roots(coeffs):
    """Find potential rational roots using the Rational Root Theorem."""

    def factors(n):
        return set(x for i in range(1, abs(n) + 1) if n % i == 0 for x in (i, -i))

    p = factors(int(coeffs[-1]))  # Factors of the constant term
    q = factors(int(coeffs[0]))  # Factors of the leading coefficient
    potential_roots = set(px / qx for px in p for qx in q if qx != 0)
    return potential_roots


def synthetic_division(coeffs, root):
    """Perform synthetic division on the polynomial with the given root."""
    quotient = [coeffs[0]]
    for coeff in coeffs[1:]:
        quotient.append(quotient[-1] * root + coeff)
    remainder = quotient.pop()
    return quotient, remainder


def factor_polynomial(coeffs):
    """Factor the polynomial given by coeffs."""
    if len(coeffs) <= 2:
        return [coeffs]

    # Find a root using the Rational Root Theorem
    roots = rational_roots(coeffs)
    for root in roots:
        quotient, remainder = synthetic_division(coeffs, root)
        if remainder == 0:
            return [[1, -root]] + factor_polynomial(quotient)

    # If no rational roots are found, return the polynomial as is
    return [coeffs]


def format_factors(factors):
    """Format the factors into a readable string."""
    formatted_factors = []
    for factor in factors:
        formatted_factors.append('(' + format_polynomial(factor) + ')')
    return ''.join(formatted_factors)


def format_polynomial(x):
    if len(x) == 0:
        return "0"
    if len(x) == 1:
        return str(x[0]) if x[0] != 0 else "0"
    str_result = ""
    for i in range(len(x) - 1):
        if x[i] == 0:
            continue
        if i == 0:
            if len(x) - i - 1 == 1:
                if x[i] == 1:
                    str_result += "x"
                elif x[i] == -1:
                    str_result += "-x"
                else:
                    str_result += str(x[i]) + "x"
            else:
                if x[i] == 1:
                    str_result += "x^" + str(len(x) - i - 1)
                elif x[i] == -1:
                    str_result += "-x^" + str(len(x) - i - 1)
                else:
                    str_result += str(x[i]) + "x^" + str(len(x) - i - 1)
        else:
            if len(x) - i - 1 == 1:
                if x[i] == 1:
                    str_result += " + x"
                elif x[i] == -1:
                    str_result += " - x"
                else:
                    str_result += (" + " if x[i] > 0 else " - ") + str(abs(x[i])) + "x"
            else:
                if x[i] == 1:
                    str_result += " + x^" + str(len(x) - i - 1)
                elif x[i] == -1:
                    str_result += " - x^" + str(len(x) - i - 1)
                else:
                    str_result += (" + " if x[i] > 0 else " - ") + str(abs(x[i])) + "x^" + str(len(x) - i - 1)
    if x[-1] != 0:
        str_result += (" + " if x[-1] > 0 else " - ") + str(abs(x[-1]))
    return str_result


def calculate_gcf(coeffs):
    """Calculate the greatest common factor of the polynomial coefficients."""
    int_coeffs = [int(c) for c in coeffs]
    return reduce(gcd, int_coeffs)


def main():
    input_str = input("Enter the polynomial coefficients (comma-separated): ")
    coeffs = input_to_list(input_str)

    # Calculate the GCF of the coefficients
    gcf = calculate_gcf(coeffs)

    # Divide coefficients by the GCF
    normalized_coeffs = [coeff / gcf for coeff in coeffs]

    # Ensure the leading coefficient is positive
    if normalized_coeffs[0] < 0:
        normalized_coeffs = [-coeff for coeff in normalized_coeffs]
        gcf = -gcf

    # Factor the polynomial
    factors = factor_polynomial(normalized_coeffs)

    # Format the factors for display
    formatted_factors = format_factors(factors)

    # Add the GCF to the output
    if gcf != 1:
        formatted_factors = "{}{}".format(gcf, formatted_factors)

    print(formatted_factors)


main()
