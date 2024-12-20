<h2>
Python
</h2>

There are 2 Python programs provided by ti-utils.

FACTOR.py: Factors polynomials

POLYDIV.py: Does polynomial long division

UTILS.py doesn't do anything by itself, but it needs to be downloaded for Python programs to work.

UTILS_F.py doesn't do anything by itself, but it needs to be downloaded for Factor.py to work.


<h3>
FACTOR.py
</h3>

Factor.py works by first taking out a gcf. Then it is checked to see if a monomial
can be factored out. The program then checks for special cases such as a perfect square trinomial, 
difference of two squares, and grouping. Then it uses the Rational Root Theorem to determine
possible roots. Then long division is used to determine which are real roots of the polynomial.
This process finds all the linear factors and factors them out of the original polynomial.
After it has been factored completely, the factors are then put through a formatting function which
removes any gcf that could still be in a factor. It then turns the factors, which are currently lists of
coefficients into a nice readable string.

Polynomials are inputted as a list of coefficients.

1,2,1 = x^2 + 2x + 1

2, 0, 3 = 2x^2 + 3

1,0,1,0 = x^3 + x

<h3>
POLYDIV.py
</h3>

POLYDIV.py works by dividing the leading term of the polynomial 
by that of the divisor and then multiplying the result by the divisor. That result
is then subtracted from the polynomial. This process is repeated until 
the polynomial can not be divided any 
further. Polynomials are stored as lists of coefficients similar to Factor.py.

<h3>
EXPAND.py & FOIL.py
</h3>

EXPAND.py takes a polynomial and raises it to a power. FOIL.py takes two polynomials and multiplies them.
Polynomials are inputted as a list of coefficients similar to the other programs above.
UTILS.py is needed for both of these programs.

<h3>
Ti-Basic Programs
</h3>

ti-utils provides some nice programs for Algebra, Trig, and Physics. 
The Python app is not needed to run these programs.



