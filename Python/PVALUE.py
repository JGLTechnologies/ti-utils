import math

# ------------------------
# Gamma + fnInt integration (same structure as your previous programs)
# ------------------------

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
    return math.sqrt(2 * math.pi) * t**(x + 0.5) * math.exp(-t) * y

def fnInt(f, a, b, tol=1e-5, max_depth=20):
    if b < a:
        return -fnInt(f, b, a, tol, max_depth)

    def simpson(f, a, b):
        m = (a + b) / 2
        return (b - a) * (f(a) + 4*f(m) + f(b)) / 6

    def adaptive(f, a, b, S, fa, fm, fb, tol, depth):
        if depth <= 0:
            return S
        m = (a + b) / 2
        lm = (a + m) / 2
        rm = (m + b) / 2
        flm = f(lm)
        frm = f(rm)
        S_left = (m - a) * (fa + 4*flm + fm) / 6
        S_right = (b - m) * (fm + 4*frm + fb) / 6
        S2 = S_left + S_right
        if abs(S2 - S) <= 15 * tol:
            return S2 + (S2 - S) / 15
        return (adaptive(f, a, m, S_left, fa, flm, fm, tol/2, depth-1) +
                adaptive(f, m, b, S_right, fm, frm, fb, tol/2, depth-1))

    m = (a + b) / 2
    fa, fm, fb = f(a), f(m), f(b)
    S = (b - a) * (fa + 4*fm + fb) / 6
    return adaptive(f, a, b, S, fa, fm, fb, tol, max_depth)


# ------------------------
# PDFs
# ------------------------

def normal_pdf(x):
    return (1 / math.sqrt(2*math.pi)) * math.exp(-0.5 * x*x)

def t_pdf(x, df):
    num = gamma((df + 1)/2)
    den = math.sqrt(df * math.pi) * gamma(df/2)
    return num / den * (1 + (x*x)/df)**(-(df+1)/2)

def chi_pdf(x, df):
    if x <= 0:
        return 0
    return (1 / ((2**(df/2)) * gamma(df/2))) * (x**(df/2 - 1)) * math.exp(-x/2)


# ------------------------
# P-VALUE FUNCTIONS
# ------------------------

def p_value_z(z, tail):
    if tail == 1:   # left
        return fnInt(normal_pdf, -10, z)
    if tail == 3:   # right
        return 1 - fnInt(normal_pdf, -10, z)
    if tail == 2:   # two-tailed
        return 2 * (1 - fnInt(normal_pdf, -10, abs(z)))


def p_value_t(t, df, tail):
    if tail == 1:
        return fnInt(lambda x: t_pdf(x, df), -10, t)
    if tail == 3:
        return 1 - fnInt(lambda x: t_pdf(x, df), -10, t)
    if tail == 2:
        return 2 * (1 - fnInt(lambda x: t_pdf(x, df), -10, abs(t)))


def p_value_chi(chi_value, df, tail):
    if tail == 1:  # left
        return fnInt(lambda x: chi_pdf(x, df), 0, chi_value)
    if tail == 3:  # right
        return 1 - fnInt(lambda x: chi_pdf(x, df), 0, chi_value)
    if tail == 2:  # two-tail (rare for chi-square)
        left = fnInt(lambda x: chi_pdf(x, df), 0, chi_value)
        right = 1 - left
        return 2 * min(left, right)


# ------------------------
# MAIN PROGRAM
# ------------------------

def main():
    print("Distribution: 1 = Z, 2 = T, 3 = Chi-square")
    dist = int(input("Distribution type: "))

    if dist != 1:
        df = float(input("Degrees of freedom: "))

    print("Tail: 1 = left, 2 = two-tailed, 3 = right")
    tail = int(input("Tail type: "))

    stat = float(input("Test statistic value: "))

    if dist == 1:
        p = p_value_z(stat, tail)
    elif dist == 2:
        p = p_value_t(stat, df, tail)
    else:
        p = p_value_chi(stat, df, tail)

    print("p-value =", round(p, 3))

main()
