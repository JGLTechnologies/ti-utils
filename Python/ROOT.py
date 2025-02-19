from UTILS import is_int
from UTILS_2 import get_factors


def is_perfect_root(n, root):
    r = n ** (1 / root)
    if isinstance(r, int) or (isinstance(r, float) and is_int(r)):
        return True
    return False


def root_simplify(n, root):
    imag = n < 0
    n = abs(n)
    ps = is_perfect_root(n, root)
    if ps:
        return str(int(n ** (1 / root)))
    perfect_roots = [f for f in get_factors(n) if is_perfect_root(f, root)]
    if len(perfect_roots) != 0:
        coeff = int(max(perfect_roots) ** (1 / root))
    else:
        coeff = 1
    n //= coeff**root
    coeff = str(coeff)
    if coeff == "1":
        coeff = ""
    if imag:
        coeff += "i"
    if n == 1:
        remainder = ""
    else:
        remainder = "(" + str(n) + ")^(1/" + str(root) + ")"
    return coeff + remainder


def main():
    number = input("Number: ").replace(" ", "")
    try:
        int(number)
    except ValueError:
        print("Number must be an integer.")
        main()
        return
    if str(int(number)) != number:
        print("Number must be an integer.")
        main()
        return
    root = input("Root: ").replace(" ", "")
    try:
        if int(root) < 1:
            print("Invalid root.")
            main()
            return
    except ValueError:
        print("Root must be an integer.")
        main()
        return
    if str(int(root)) != root:
        print("Root must be an integer.")
        main()
        return
    print(root_simplify(int(number), int(root)))


main()
