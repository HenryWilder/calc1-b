from typing import Callable

def is_number(ch: str):
    return ch in "0123456789"

def is_lower(ch: str):
    return ch in "abcdefghijklmnopqrstuvwxyz"

def is_upper(ch: str):
    return ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def is_letter(ch: str):
    return is_lower(ch) or is_upper(ch)

class StringStream:
    def __init__(self, src: str):
        self._i = 0
        self._src = src

    def is_valid(self, n: int = 1) -> bool:
        return self._i + n <= len(self._src)

    def peek(self, n: int = 1) -> str | None:
        if self.is_valid(n):
            return self._src[self._i:self._i + n]

    def is_eq(self, test: str) -> bool:
        return self.peek(len(test)) == test

    def is_in(self, test: str | list[str]) -> bool:
        return any([self.is_eq(x) for x in test])

    def skip(self, n: int = 1):
        self._i += n

    def skip_if_eq(self, test: str) -> bool:
        if self.is_eq(test):
            self.skip(len(test))
            return True
        return False

    def take(self, n = 1) -> str:
        result = self.peek(n)
        self.skip(n)
        return result

    def take_while(self, pred: Callable[[str], bool]) -> str:
        i = self._i
        while self.is_valid() and pred(self.peek()): self.skip()
        return self._src[i:self._i]


class Expr:
    INT = "int"
    VAR = "var"
    INF = "infty"
    DNE = "dne"
    NEG = "-"
    ADD = "+"
    MUL = "*"
    DIV = "/"
    POW = "^"

    def __init__(self, tag: str, data):
        self.tag = tag
        self.data: int | str | Expr | tuple[Expr, Expr] | list[Expr] | None = data

    def int(value: int):
        return Expr(Expr.INT, value)

    def var(name: str):
        return Expr(Expr.VAR, name)

    def inf():
        return Expr(Expr.INF, None)

    def dne():
        return Expr(Expr.DNE, None)

    def __neg__(self):
        return Expr(Expr.NEG, self)

    def __add__(self, other: 'Expr'):
        return Expr(Expr.ADD, [(x for x in item.data) if item.tag == Expr.ADD else item for item in list[Expr]([self, other])])

    def __sub__(self, other: 'Expr'):
        return self + (-other)

    def __mul__(self, other: 'Expr'):
        return Expr(Expr.MUL, [(x for x in item.data) if item.tag == Expr.MUL else item for item in list[Expr]([self, other])])

    def __div__(self, other: 'Expr'):
        return Expr(Expr.DIV, (self, other))

    def __pow__(self, other: 'Expr'):
        return Expr(Expr.POW, (self, other))

    def substitute(self, var: str, replacement: 'Expr'):
        if self.tag == Expr.VAR and self.data == var:
            return replacement
        elif self.tag in [Expr.VAR, Expr.INT, Expr.DNE, Expr.INF]:
            return self
        elif self.tag == Expr.NEG:
            assert type(self.data) is Expr
            return -(self.data.substitute(var, replacement))
        elif self.tag in [Expr.ADD, Expr.MUL]:
            assert type(self.data) is list[Expr]
            return Expr(self.tag, [item.substitute(var, replacement) for item in self.data])
        elif self.tag == Expr.DIV:
            assert type(self.data) is tuple[Expr, Expr]
            return Expr(self.tag, tuple(item.substitute(var, replacement) for item in self.data))
        else:
            raise ValueError("Unknown tag: {}".format(self.tag))

    def _tokenize(stream: StringStream):
        tokens: list[Expr] = []
        while stream.is_valid():
            if stream.skip_if_eq(' '):
                pass
            elif stream.skip_if_eq('('):
                sub_tokens = Expr._tokenize(stream)
                tokens.append(sub_tokens) # todo
            elif stream.is_eq(')'):
                break
            elif stream.skip_if_eq("**") or stream.skip_if_eq("^"):
                tokens.append(Expr(Expr.POW, None))
            elif stream.skip_if_eq('*'):
                tokens.append(Expr(Expr.MUL, None))
            elif stream.skip_if_eq('+'):
                tokens.append(Expr(Expr.ADD, None))
            elif stream.skip_if_eq('-'):
                tokens.append(Expr(Expr.NEG, None))
            elif stream.skip_if_eq('/'):
                tokens.append(Expr(Expr.DIV, None))
            elif stream.skip_if_eq("inf"):
                tokens.append(Expr.inf())
            elif stream.skip_if_eq("dne"):
                tokens.append(Expr.dne())
            elif is_number(stream.peek()):
                tokens.append(Expr(Expr.INT, int(stream.take_while(is_number))))
            elif is_letter(stream.peek()):
                v = stream.take()
                if stream.skip_if_eq('_'):
                    v += '_'
                    if stream.skip_if_eq('{'):
                        v += stream.take_while(lambda ch: ch != '}')
                        stream.skip() # }
                    else:
                        v += stream.take()
                v += stream.take_while(lambda ch: ch == '\'')
                tokens.append(Expr(Expr.VAR, v))
        return tokens

    def parse(text: str) -> 'Expr':
        tokens = Expr._tokenize(StringStream(text))
        return tokens[0]

    def _debug_tokens(tokens: list['Expr']):
        return ", ".join(["'{}'[{}]".format(token.tag, token.data) for token in tokens])

    def __str__(self):
        if self.tag == Expr.INT:
            return str(self.data)
        elif self.tag == Expr.VAR:
            return self.data
        elif self.tag == Expr.INF:
            return "∞"
        elif self.tag == Expr.DNE:
            return "DNE"
        elif self.tag == Expr.NEG:
            return "(-{})".format(self.data)
        elif self.tag == Expr.ADD or self.tag == Expr.MUL:
            separator = ('+' if self.tag == Expr.ADD else '*')
            return "({})".format(separator.join([str(item) for item in self.data]))
        elif self.tag == Expr.DIV or self.tag == Expr.POW:
            separator = ('/' if self.tag == Expr.DIV else '^')
            (a, b) = self.data
            return "({}{}{})".format(a, separator, b)
        else:
            return "[err: '{}' not recognized]".format(self.tag)

print(Expr.parse("29932*x_{99}'+633"))
