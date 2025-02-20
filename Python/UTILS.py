def format_number(n):
    s = "{:.5f}".format(n)
    s = s.rstrip("0").rstrip(".")
    return s


def input_to_list(input_str):
    return [float(num) for num in input_str.split(",")]


def multiply_poly(a, b):
    a_terms = get_terms(a)
    b_terms = get_terms(b)
    result = []
    for a_term in a_terms:
        for b_term in b_terms:
            result.append((b_term[0] * a_term[0], b_term[1] + a_term[1]))
    return get_coeffs(result)


def is_int(x):
    if isinstance(x, int):
        return True
    try:
        return int(str(x).split(".")[1]) == 0
    except ValueError:
        return False


def format_polynomial(x):
    """Format a list of coefficients into a polynomial string"""
    if len(x) == 0:
        return "0"
    if len(x) == 1:
        return str(x[0]) if x[0] != 0 else "0"
    str_result = ""
    for i in range(len(x) - 1):
        c = x[i]
        if c == 0:
            continue
        if i == 0:
            if len(x) - i - 1 == 1:
                if c == 1:
                    str_result += "x"
                elif c == -1:
                    str_result += "-x"
                else:
                    str_result += format_number(c) + "x"
            else:
                if c == 1:
                    str_result += "x^" + str(len(x) - i - 1)
                elif c == -1:
                    str_result += "-x^" + str(len(x) - i - 1)
                else:
                    str_result += format_number(c) + "x^" + str(len(x) - i - 1)
        else:
            if len(x) - i - 1 == 1:
                if c == 1:
                    str_result += " + x"
                elif c == -1:
                    str_result += " - x"
                else:
                    str_result += (
                            (" + " if c > 0 else " - ") + format_number(abs(c)) + "x"
                    )
            else:
                if c == 1:
                    str_result += " + x^" + str(len(x) - i - 1)
                elif c == -1:
                    str_result += " - x^" + str(len(x) - i - 1)
                else:
                    str_result += (
                            (" + " if c > 0 else " - ")
                            + format_number(abs(c))
                            + "x^"
                            + str(len(x) - i - 1)
                    )
    c = x[-1]
    if c != 0:
        str_result += (" + " if c > 0 else " - ") + format_number(abs(c))
    return str_result


def get_terms(coeffs):
    """Turns a list of coefficients into a list of terms in the form of [coeff, pow]"""
    terms = []
    for i in range(len(coeffs)):
        if coeffs[i] != 0:
            terms.append((coeffs[i], len(coeffs) - i - 1))
    return terms


def get_coeffs(terms):
    """Turns a list of terms into a list of coefficients"""
    if len(terms) == 0:
        return [0]
    degree = max([t[1] for t in terms])
    coeffs = [0] * (degree + 1)
    for t in terms:
        coeffs[len(coeffs) - t[1] - 1] += t[0]
    return coeffs


def subtract(x, y):
    threshold = 1e-10
    result = [0] * len(x)
    for i in range(len(result)):
        if i >= len(y):
            result[len(result) - i - 1] = x[len(x) - i - 1]
        else:
            result[len(result) - i - 1] = x[len(x) - i - 1] - y[len(y) - i - 1]

    result = [coeff if abs(coeff) > threshold else 0 for coeff in result]

    # Get rid of leading zeros
    z = 0
    for n in result:
        if n == 0:
            z += 1
        else:
            break
    return result[z: len(result)]


def divide(poly, divisor):
    div_power = len(divisor) - 1
    poly_power = len(poly) - 1
    result = []
    while poly_power >= div_power:
        term = [poly[0] / divisor[0], poly_power - div_power]
        result.append(term)
        sub = multiply_poly(get_coeffs([(term[0], term[1])]), divisor)
        poly = subtract(poly, sub)
        poly_power = len(poly) - 1
    return get_coeffs(result), poly
