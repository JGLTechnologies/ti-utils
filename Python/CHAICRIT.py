# Use this to find the chai square critical values

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

def chi_pdf(x):
    if x <= 0:
        return 0.0
    k = v
    coeff = 1.0 / ((2.0 ** (k / 2.0)) * gamma(k / 2.0))
    return coeff * (x ** (k / 2.0 - 1.0)) * math.exp(-x / 2.0)

def chi_cdf(x):
    return fnInt(chi_pdf, 0.0, x)

def chi_quantile(target):
    lo = 0.0
    hi = max(10.0, v * 3.0)
    for _ in range(40):
        mid = (lo + hi) / 2.0
        if chi_cdf(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0

def chi_critical_tail(alpha, tail):
    if tail == 1:
        crit = chi_quantile(alpha)
        return round(crit, 3)

    if tail == 3:
        crit = chi_quantile(1.0 - alpha)
        return round(crit, 3)

    if tail == 2:
        left = chi_quantile(alpha / 2.0)
        right = chi_quantile(1.0 - alpha / 2.0)
        return round(left, 3), round(right, 3)

def main():
    global v
    n = float(input("Sample size n: "))
    v = n - 1

    print("Tail type:")
    print("1 = left-tailed")
    print("2 = two-tailed")
    print("3 = right-tailed")
    tail = int(input("Tail (1/2/3): "))

    alpha = float(input("Significance Level: "))

    result = chi_critical_tail(alpha, tail)
    if tail == 2:
        critL, critR = result
        print("critL =", critL)
        print("critR =", critR)
    else:
        print(result)

main()
