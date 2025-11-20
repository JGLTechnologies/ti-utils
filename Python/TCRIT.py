# Use this to find the t critical value

import math

v = 0

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


def t_pdf(x):
    num = gamma((v + 1) / 2.0)
    den = math.sqrt(v * math.pi) * gamma(v / 2.0)
    return num / den * (1.0 + (x * x) / v) ** (-(v + 1) / 2.0)


def t_critical_tail(alpha, tail):
    if tail == 1:
        target = alpha
        low = -10.0
        high = 0.0
        while high - low > 1e-5:
            mid = (low + high) / 2.0
            area = fnInt(t_pdf, -10.0, mid)
            if area < target:
                low = mid
            else:
                high = mid
        return round(high, 3)

    if tail == 2:
        target = 1.0 - alpha
        low = 0.0
        high = 10.0
        while high - low > 1e-5:
            mid = (low + high) / 2.0
            area = fnInt(t_pdf, -mid, mid)
            if area < target:
                low = mid
            else:
                high = mid
        return round((low + high) / 2.0, 3)

    if tail == 3:
        target = 1.0 - alpha
        low = 0.0
        high = 10.0
        while high - low > 1e-5:
            mid = (low + high) / 2.0
            area = fnInt(t_pdf, -10.0, mid)
            if area < target:
                low = mid
            else:
                high = mid
        return round((low + high) / 2.0, 3)


def main():
    global v
    n = float(input("Sample size n: "))
    v = n - 1

    print("Tail type:")
    print("1 = left-tailed")
    print("2 = two-tailed (CI)")
    print("3 = right-tailed")
    tail = int(input("Tail (1/2/3): "))

    alpha_percent = float(input("Significance Level: "))
    alpha = alpha_percent / 100.0

    print(t_critical_tail(alpha, tail))

main()
