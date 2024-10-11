import typing
from math import gcd
from itertools import *
from utility import *
from debug import *
# from stringstream import StringStream

class Expr:
    data: object

    def int(value: int):
        return Int(value)

    def var(name: str):
        return Var(name)

    def inf():
        return Inf()

    def dne():
        return DNE()

    def __neg__(self):
        return Neg(self)

    def __add__(self, other: 'Expr'):
        return Add(self, other)

    def __sub__(self, other: 'Expr'):
        return self + (-other)

    def __mul__(self, other: 'Expr'):
        return Mul(self, other)

    def __truediv__(self, other: 'Expr'):
        return Div(self, other)

    def __pow__(self, other: 'Expr'):
        return Pow(self, other)

    def substitute(self, var: str, replacement: 'Expr'):
        """
        Recursively replaces all instances of `Var` `var` in the expression with `replacement`.
        """
        raise TypeError(f"Missing `substitute` override for '{self.tag}'")

    def toggle_sign(self):
        """
        Encloses non-`Neg`, non-`Int` in `Neg`.
        Extracts inner expression from `Neg`.
        Negates `Int` in-place.
        """
        return Neg(self)

    def try_evaluate(self):
        """
        Evaluates all branches that can be converted into constants.
        """
        return self # assumes the expression is atomic if not overridden

    def __str__(self):
        raise TypeError(f"Missing `__str__` override for '{self.tag}'")


class Int(Expr):
    def __init__(self, data: int):
        self.data: int = data

    def substitute(self, var: str, replacement: 'Expr'):
        return self

    def toggle_sign(self):
        return Int(-self.data)

    def __str__(self):
        return str(self.data)


class Var(Expr):
    def __init__(self, data: str):
        self.data: str = data

    def substitute(self, var: str, replacement: 'Expr'):
        return replacement if var == self.data else self

    def __str__(self):
        return f"({self.data})"


class Inf(Expr):
    def __init__(self):
        self.data: None = None

    def substitute(self, var: str, replacement: 'Expr'):
        return self

    def __str__(self):
        return "∞"


class DNE(Expr):
    def __init__(self):
        self.data: None = None

    def substitute(self, var: str, replacement: 'Expr'):
        return self

    def __str__(self):
        return "DNE"


class Neg(Expr):
    def __init__(self, data: 'Expr'):
        self.data: Expr = data

    def substitute(self, var: str, replacement: 'Expr'):
        return Neg(self.data.substitute(var, replacement))

    def toggle_sign(self):
        return self.data

    def try_evaluate(self):
        self.data = self.data.try_evaluate()
        if isinstance(self.data, Neg): # double negative
            return self.data.data
        elif isinstance(self.data, Int): # transfer negation to int
            return self.data.toggle_sign()
        return self

    def __str__(self):
        return f"(-{self.data})"


class Add(Expr):
    def __init__(self, *data: 'Expr'):
        self.data: list[Expr] = [(x for x in item.data) if isinstance(item, Add) else item for item in data]

    def substitute(self, var: str, replacement: 'Expr'):
        return Add(*[item.substitute(var, replacement) for item in self.data])

    def conjugate(self) -> Expr:
        assert len(self.data) == 2, "Must have exactly 2 terms to conjugate"
        # todo
        return self

    def combine_like_to_products():
        """
        Lumps identical terms into products.
        """
        return

    def factor(self) -> Expr:
        """
        Extract the most complex, repeated expression possible.
        """
        # todo
        return self

    def try_evaluate(self):
        self.data = [item.try_evaluate() for item in self.data]
        # all elements in `self.data` are either atomic or contain variables.
        acc = 0; [acc := acc + item.data for item in self.data if isinstance(item, Int)]
        self.data = [*[item for item in self.data if not isinstance(item, Int)], acc]
        return self.data if len(self.data) == 1 else self

    def __str__(self):
        return '(' + '+'.join([str(item) for item in self.data]) + ')'


class Mul(Expr):
    def __init__(self, *data: 'Expr'):
        self.data: list[Expr] = [(x for x in item.data) if isinstance(item, Mul) else item for item in data]

    def substitute(self, var: str, replacement: 'Expr'):
        return Mul(*[item.substitute(var, replacement) for item in self.data])

    def combine_like_to_powers(self):
        """
        Lumps identical factors into powers.
        """
        return Mul([x ** Int(self.data.count(x)) for x in list(set(self.data))])

    def try_evaluate(self):
        self.data = [item.try_evaluate() for item in self.data]
        # all elements in `self.data` are either atomic or contain variables.
        acc = 1; [acc := acc * item.data for item in self.data if isinstance(item, Int)]
        self.data = [*[item for item in self.data if not isinstance(item, Int)], acc]
        return self.data if len(self.data) == 1 else self

    def __str__(self):
        return '(' + '*'.join([str(item) for item in self.data]) + ')'


class Div(Expr):
    def __init__(self, lhs: 'Expr', rhs: 'Expr'):
        self.data: tuple[Expr, Expr] = (lhs, rhs)

    def substitute(self, var: str, replacement: 'Expr'):
        return Div(*[item.substitute(var, replacement) for item in self.data])

    def try_evaluate(self):
        (n, d) = self.data
        n, d = n.try_evaluate(), d.try_evaluate()
        if isinstance(n, Int) and isinstance(d, Int):
            if n.data % d.data == 0:
                return Int(n.data / d.data)
        return Div(n, d)

    def __str__(self):
        (lhs, rhs) = self.data
        return f"({lhs}/{rhs})"


class Pow(Expr):
    def __init__(self, lhs: 'Expr', rhs: 'Expr'):
        self.data: tuple[Expr, Expr] = (lhs, rhs)

    def substitute(self, var: str, replacement: 'Expr'):
        return Pow(*[item.substitute(var, replacement) for item in self.data])

    def try_evaluate(self):
        (n, d) = self.data
        n, d = n.try_evaluate(), d.try_evaluate()
        if isinstance(n, Int) and isinstance(d, Int):
            combined: int | float = n.data ** d.data
            if isinstance(combined, int) or combined.is_integer():
                return Int(int(combined))
        return Pow(n, d)

    def __str__(self):
        (lhs, rhs) = self.data
        return f"({lhs}^{rhs})"
