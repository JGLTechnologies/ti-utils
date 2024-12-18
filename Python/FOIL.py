from UTILS import *

def main():
    pol1 = input("First polynomial: ")
    try:
        pol1 = input_to_list(pol1)
    except ValueError:
        print("Invalid input")
        main()
        return
    pol2 = input("Second polynomial: ")
    try:
        pol2 = input_to_list(pol2)
    except ValueError:
        print("Invalid input")
        main()
        return
    result = multiply_poly(pol1, pol2)
    print(format_polynomial(result))


main()
