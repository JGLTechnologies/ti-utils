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
                    str_result += (" + " if x[i] > 0 else " - ") + str(abs(x[i])) + "x^" + str(len(x) - i - 1)
    if x[-1] != 0:
        str_result += (" + " if x[-1] > 0 else " - ") + str(abs(x[-1]))
    return str_result


def get_terms(coeffs):
    """Turns a list of coefficients into a list of terms in the form of [coeff, pow]"""
    terms = []
    for i in range(len(coeffs)):
        if coeffs[i] != 0:
            terms.append([coeffs[i], len(coeffs) - i - 1])
    return terms


def get_coeffs(terms):
    """Turns a list of terms into a list of coefficients"""
    degree = [t[1] for t in terms]
    degree.sort()
    degree = degree[-1]
    coeffs = [0]*(degree+1)
    for t in terms:
        coeffs[len(coeffs)-t[1]-1] = t[0]
    return coeffs