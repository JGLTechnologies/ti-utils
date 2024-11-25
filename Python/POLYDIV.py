from UTILS import *


def main():
    pol = input("Enter the polynomial: ")
    try:
        poly = input_to_list(pol)
    except ValueError:
        print("Invalid input")
        main()
        return
    div = input("Enter the divisor: ")
    try:
        divisor = input_to_list(div)
    except ValueError:
        print("Invalid input")
        main()
        return
    result, rem = divide(poly, divisor)
    print(format_polynomial(result))
    print("Remainder: " + format_polynomial(rem))


main()
