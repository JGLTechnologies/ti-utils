def input_to_list(input_str):
    return [float(num) for num in input_str.split(",")]


def format_polynomial(x):
    """Format a list of coefficients into a polynomial string"""
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
                    str_result += (
                            (" + " if x[i] > 0 else " - ")
                            + str(abs(x[i]))
                            + "x^"
                            + str(len(x) - i - 1)
                    )
    if x[-1] != 0:
        str_result += (" + " if x[-1] > 0 else " - ") + str(abs(x[-1]))
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
    degree = [t[1] for t in terms]
    degree.sort()
    degree = degree[-1]
    coeffs = [0] * (degree + 1)
    for t in terms:
        coeffs[len(coeffs) - t[1] - 1] = t[0]
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


def mult(coeff, pow, x):
    result = [0] * (len(x) + pow)
    for i in range(len(x)):
        result[i] = x[i] * coeff
    return result


def divide(poly, divisor):
    div_power = len(divisor) - 1
    poly_power = len(poly) - 1
    result = []
    while poly_power >= div_power:
        term = [poly[0] / divisor[0], poly_power - div_power]
        result.append(term)
        sub = mult(term[0], term[1], divisor)
        poly = subtract(poly, sub)
        poly_power = len(poly) - 1
    return get_coeffs(result), poly
