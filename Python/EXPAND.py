from UTILS import *

def main():
    pol = input("Enter the polynomial: ")
    try:
        poly = input_to_list(pol)
    except ValueError:
        print("Invalid input")
        main()
        return
    power = input("Enter the power: ")
    try:
        power = int(power)
    except ValueError:
        print("Invalid input")
        main()
        return
    result = poly
    for _ in range(power-1):
        result = multiply_poly(result, poly)
    print(format_polynomial(result))


main()
