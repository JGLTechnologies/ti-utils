from UTILS import *


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