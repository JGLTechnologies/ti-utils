# Use this to find the z critical value

import math

v = c = 0

def fnInt(f, a, b, tol=1e-5, max_depth=20):
    if b < a:
        return -fnInt(f, b, a, tol, max_depth)

    def simpson(f, a, b):
        m = 0.5 * (a + b)
        fa = f(a)
        fm = f(m)
        fb = f(b)
        return (b - a) * (fa + 4.0 * fm + fb) / 6.0

    def adaptive(f, a, b, S, fa, fm, fb, tol, depth):
        if depth <= 0:
            return S

        m = 0.5 * (a + b)
        lm = 0.5 * (a + m)
        rm = 0.5 * (m + b)

        flm = f(lm)
        frm = f(rm)

        S_left  = (m - a) * (fa  + 4.0 * flm + fm) / 6.0
        S_right = (b - m) * (fm  + 4.0 * frm + fb) / 6.0

        S2 = S_left + S_right

        if abs(S2 - S) <= 15.0 * tol:
            return S2 + (S2 - S) / 15.0
        else:
            left  = adaptive(f, a, m, S_left,  fa,  flm, fm, 0.5 * tol, depth - 1)
            right = adaptive(f, m, b, S_right, fm,  frm, fb, 0.5 * tol, depth - 1)
            return left + right

    m = 0.5 * (a + b)
    fa = f(a)
    fm = f(m)
    fb = f(b)
    S = (b - a) * (fa + 4.0 * fm + fb) / 6.0

    return adaptive(f, a, b, S, fa, fm, fb, tol, max_depth)

import math

p = [
    0.99999999999980993,
    676.5203681218851,
    -1259.1392167224028,
    771.32342877765313,
    -176.61502916214059,
    12.507343278686905,
    -0.13857109526572012,
    9.9843695780195716e-6,
    1.5056327351493116e-7
]

def gamma(x):
    if x < 0.5:
        return math.pi / (math.sin(math.pi * x) * gamma(1 - x))

    x -= 1
    y = p[0]
    for i in range(1, len(p)):
        y += p[i] / (x + i)

    g = 7
    t = x + g + 0.5
    return math.sqrt(2 * math.pi) * (t ** (x + 0.5)) * math.exp(-t) * y

def normal_pdf(x):
    return (1/math.sqrt(2*math.pi)) * math.exp(-0.5 * x*x)

def z_critical_tail(alpha, tail):
    if tail == 1:
        target = alpha
        low = -5.0
        high = 0.0
        while high - low > 1e-5:
            mid = (low + high) / 2
            area = fnInt(normal_pdf, -10, mid)
            if area < target:
                low = mid
            else:
                high = mid
        return round(high, 3)

    if tail == 2:
        target = 1 - alpha
        low = 0.0
        high = 5.0
        while high - low > 1e-5:
            mid = (low + high) / 2
            area = fnInt(normal_pdf, -mid, mid)
            if area < target:
                low = mid
            else:
                high = mid
        return round((low + high) / 2, 3)

    if tail == 3:
        target = 1 - alpha
        low = 0.0
        high = 5.0
        while high - low > 1e-5:
            mid = (low + high) / 2
            area = fnInt(normal_pdf, -10, mid)
            if area < target:
                low = mid
            else:
                high = mid
        return round((low + high) / 2, 3)

def main():
    print("Choose tail type:")
    print("1 = left-tailed")
    print("2 = two-tailed")
    print("3 = right-tailed")

    tail = int(input("Tail (1/2/3): "))
    alpha = float(input("Significance Level: "))

    print(z_critical_tail(alpha, tail))

main()
