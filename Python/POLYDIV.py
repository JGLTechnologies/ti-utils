from UTILS import format_polynomial

def subtract(x, y):
    result = [0] * len(x)
    for i in range(len(result)):
        if i >= len(y):
            result[len(result) - i - 1] = x[len(x) - i - 1]
        else:
            result[len(result) - i - 1] = x[len(x) - i - 1] - y[len(y) - i - 1]
    z = 0
    for n in result:
        if n == 0:
            z += 1
        else:
            break
    # Get rid of zeros in the front of the list
    return result[z:len(result)]


def mult(coeff, pow, x):
    result = [0] * (len(x) + pow)
    for i in range(len(x)):
        result[i] = x[i] * coeff
    return result


def divide(poly, divisor):
    div_power = len(divisor) - 1
    poly_power = len(poly) - 1
    result = [0] * (poly_power - div_power + 1)
    for i in range(len(result)):
        poly_power = len(poly) - 1
        if poly_power < div_power:
            break
        term = poly[0] / divisor[0]
        result[i] = term
        sub = mult(term, poly_power - div_power, divisor)
        poly = subtract(poly, sub)
    return result, poly


def string_to_float(string_list):
    new_list = []
    for s in string_list:
        new_list.append(float(s))
    return new_list


def main():
    pol = input("Enter the polynomial: ")
    div = input("Enter the divisor: ")
    poly = string_to_float(pol.replace(" ", "").split(","))
    divisor = string_to_float(div.replace(" ", "").split(","))
    result, rem = divide(poly, divisor)
    print(format_polynomial(result))
    print("Remainder: " + format_polynomial(rem))


main()