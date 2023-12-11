import numpy as np

class Polynomial():

    def __init__(self, coeff):
        '''
        Initialize a polynomial with given coefficients.

        Parameters:
        -----------
        coeff : list or np.ndarray
            Coefficients of the polynomial, with the highest degree first.
        '''
        self._coeff = np.array(coeff, dtype=float)
        if np.all(self._coeff == 0):
            raise ValueError('Polynomial cannot have all coefficients as zero.')
        self._coeff = np.trim_zeros(self._coeff, 'f')
        self._roots = None

    @property
    def coeff(self):
        return self._coeff

    def _differentiate(self, n):
        '''
        Calculate the coefficients of the n-th derivative.
        '''
        coeff = self._coeff
        for _ in range(n):
            degree = np.arange(coeff.size, 1, -1) - 1
            coeff = coeff[:-1] * degree
        return coeff

    def derivative(self, n=1):
        '''
        Return the n-th derivative as a new Polynomial object.
        '''
        if n < 0:
            raise ValueError('Derivative order must be non-negative.')
        return Polynomial(self._differentiate(n))

    def eval(self, X):
        '''
        Evaluate the polynomial at given X value(s).
        '''
        return np.polyval(self._coeff, X)

    def evald(self, X, n=1):
        '''
        Evaluate the n-th derivative of the polynomial at given X
        value(s).
        '''
        return np.polyval(self.derivative(n).coeff, X)

    def roots(self):
        '''
        Calculate the roots of the polynomial, if not already done.
        '''
        if self._roots is None:
            self._roots = np.roots(self._coeff)
        return self._roots

    def _get_poly_string(self, coeff):
        '''
        Construct a string representation of a polynomial given its list
        of coefficients.
        '''
        s, fmt = '', ' {0} {1}x^{{{2}}}'
        e = np.arange(coeff.size, 0, -1) - 1

        for c_, e_ in zip(coeff, e):
            if c_ > 0: s += fmt.format('+', np.abs(c_), e_)
            if c_ < 0: s += fmt.format('-', np.abs(c_), e_)

        s = s.replace('x^{0}', '')  # Delete `x^{0}` from the strings
        s = s.replace('x^{1}', 'x') # Replace `x^{1}` with just `x`
        s = s.replace('1.0x', 'x')  # Replace `1x^{n}` with just `x^{n}`

        return s[3:] if coeff[0] > 0 else s[1:]

    def __str__(self):
        '''
        String representation of the polynomial.
        '''
        return self._get_poly_string(self._coeff)

    def __strd__(self, n=1):
        '''
        String representation of an n-th derivative of the polynomial.
        '''
        return self._get_poly_string(self.derivative(n).coeff)