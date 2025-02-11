from UTILS import *

def main():
    polys = []
    number = 0
    while True:
        p = input("polynomial #"+str(number+1)+": ")
        if p == "":
            if number < 2:
                print("You must enter at least 2 polynomials.")
                continue
            break
        try:
            polys.append(input_to_list(p))
            number += 1
        except ValueError:
            print("Invalid input")
            continue

    result = [1]
    for p in polys:
        result = multiply_poly(result, p)
    print(format_polynomial(result))

main()
