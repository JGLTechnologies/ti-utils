fraction_roots = set()
gcf = 0


def input_to_list(input_str):
    """Convert a comma-separated string to a list of floats."""
    return [float(num) for num in input_str.split(',')]


def factors(n):
    """Return the set of factors of an integer n."""
    return set(x for i in range(1, abs(n) + 1) if n % i == 0 for x in (i, -i))


def rational_roots(coeffs):
    global fraction_roots
    """Find potential rational roots using the Rational Root Theorem."""
    p = factors(int(coeffs[-1]))  # Factors of the constant term
    q = factors(int(coeffs[0]))  # Factors of the leading coefficient
    f_roots = set((px, qx) for px in p for qx in q if qx != 0 and (px, qx))
    fraction_roots.update(f_roots)
    return set(f[0]/f[1] for f in fraction_roots)


def synthetic_division(coeffs, root):
    """Perform synthetic division on the polynomial with the given root."""
    quotient = [coeffs[0]]
    for coeff in coeffs[1:]:
        quotient.append(quotient[-1] * root + coeff)
    remainder = quotient.pop()
    return quotient, remainder


def gcd(a, b):
    """Calculate the Greatest Common Divisor of a and b."""
    while b != 0:
        a, b = b, a % b
    return abs(a)


def reduce(function, iterable, initializer=None):
    """Apply function cumulatively to the items of iterable."""
    it = iter(iterable)
    value = initializer if initializer is not None else next(it)
    for element in it:
        value = function(value, element)
    return value


def calculate_gcf(coeffs):
    """Calculate the greatest common factor of the polynomial coefficients."""
    int_coeffs = [int(c) for c in coeffs if c != 0]
    return reduce(gcd, int_coeffs)


def get_terms(coeffs):
    terms = []
    for i, c in enumerate(coeffs):
        if c != 0:
            terms.append([c, len(coeffs) - i - 1])
    return terms

def get_coeffs(terms):
    degree = [t[1] for t in terms]
    degree.sort()
    degree = degree[-1]
    coeffs = [0]*(degree+1)
    for t in terms:
        coeffs[len(coeffs)-t[1]-1] = t[0]
    return coeffs


def factor_polynomial(coeffs):
    """Factor the polynomial given by coeffs."""
    if len(coeffs) <= 1:
        return [coeffs]

    # Check for x as a factor (if the constant term is 0)
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
        coeffs_1 = get_coeffs([ [group_1[0][0], group_1[0][1]-max_power_1], [group_1[1][0], group_1[1][1]-max_power_1] ])
        gcf_1 = calculate_gcf(coeffs_1)
        group_1 = [g / gcf_1 for g in coeffs_1]

        group_2 = terms[2:4]
        max_power_2 = terms[3][1]
        coeffs_2 = get_coeffs([(group_2[0][0], group_2[0][1] - max_power_2), (group_2[1][0], group_2[1][1] - max_power_2)])
        gcf_2 = calculate_gcf(coeffs_2)
        group_2 = [g / gcf_2 for g in coeffs_2]

        if group_1 == group_2:
            yield get_coeffs([ (gcf_1, max_power_1), (gcf_2, max_power_2) ])
            yield group_1
            return

    # Find a root using the Rational Root Theorem
    roots = rational_roots(coeffs)
    for root in roots:
        quotient, remainder = synthetic_division(coeffs, root)
        if remainder == 0:
            yield [1, -root]
            for factor in factor_polynomial(quotient):
                yield factor
            return


    # If no rational roots are found, return the polynomial as is
    yield coeffs


def format_polynomial(x):
    """Convert a list of coefficients to a polynomial string."""
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


def format_factors(factors):
    """Format the factors into a readable string."""
    global gcf
    formatted_factors = []
    for factor in factors:
        g = calculate_gcf(factor)
        gcf *= g
        factor = [coeff / g for coeff in factor]
        if len(factor) == 2 and factor[0] == 1:
            root = -factor[1]
            for pr in fraction_roots:
                if abs(root - pr[0]/pr[1]) < 1e-6:
                    a = pr[0]
                    b = pr[1]
                    if a < 0 and b < 0:
                        a = abs(a)
                        b = abs(b)
                    elif b < 0:
                        a = -a
                        b = abs(b)
                    formatted_factors.append('(' + format_polynomial([b, -a]) + ')')
                    break
            else:
                formatted_factors.append('(' + format_polynomial(factor) + ')')
        else:
            formatted_factors.append('(' + format_polynomial(factor) + ')')
    return ''.join(formatted_factors)


def main():
    global gcf
    input_str = input("Enter the polynomial: ")
    coeffs = input_to_list(input_str)

    # Calculate the GCF of the coefficients
    gcf = calculate_gcf(coeffs)

    # Divide coefficients by the GCF
    normalized_coeffs = [coeff / gcf for coeff in coeffs]

    # Ensure the leading coefficient is positive
    if normalized_coeffs[0] < 0:
        normalized_coeffs = [-coeff for coeff in normalized_coeffs]
        gcf = -gcf

    # Track original possible roots for formatting
    possible_roots = list(rational_roots(normalized_coeffs))

    # Factor the polynomial
    factors = list(factor_polynomial(normalized_coeffs))

    # Format the factors for display
    formatted_factors = format_factors(factors)

    # Add the GCF to the output
    if gcf != 1:
        formatted_factors = "{}{}".format(gcf, formatted_factors)

    print(formatted_factors)


main()