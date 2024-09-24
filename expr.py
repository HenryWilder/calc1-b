from utility import *
from debug import *
from stringstream import StringStream

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
        debug("Expr", "__init__", "Initializing from tag {} and data {}", tag, data)
        self.tag = tag
        self.data: int | str | Expr | tuple[Expr, Expr] | list[Expr] | None = data

    def int(value: int):
        debug("Expr", "int", "Initializing int from {}", value)
        return debug_surround(lambda: Expr(Expr.INT, value))

    def var(name: str):
        debug("Expr", "var", "Initializing var from {}", name)
        return debug_surround(lambda: Expr(Expr.VAR, name))

    def inf():
        debug("Expr", "inf", "Initializing infinity")
        return debug_surround(lambda: Expr(Expr.INF, None))

    def dne():
        debug("Expr", "dne", "Initializing DNE")
        return debug_surround(lambda: Expr(Expr.DNE, None))

    def __neg__(self):
        debug("Expr", "dne", "Negating {}", self)
        return debug_surround(lambda: Expr(Expr.NEG, self))

    def __add__(self, other: 'Expr'):
        debug("Expr", "__add__", "Initializing {} add {}", self, other)
        return debug_surround(lambda: Expr(Expr.ADD, [(x for x in item.data) if item.tag == Expr.ADD else item for item in list[Expr]([self, other])]))

    def __sub__(self, other: 'Expr'):
        debug("Expr", "__sub__", "Initializing {} sub {}", self, other)
        return self + (-other)

    def __mul__(self, other: 'Expr'):
        debug("Expr", "__mul__", "Initializing {} mul {}", self, other)
        return debug_surround(lambda: Expr(Expr.MUL, [(x for x in item.data) if item.tag == Expr.MUL else item for item in list[Expr]([self, other])]))

    def __div__(self, other: 'Expr'):
        debug("Expr", "__div__", "Initializing {} div {}", self, other)
        return debug_surround(lambda: Expr(Expr.DIV, (self, other)))

    def __pow__(self, other: 'Expr'):
        debug("Expr", "__pow__", "Initializing {} pow {}", self, other)
        return debug_surround(lambda: Expr(Expr.POW, (self, other)))

    def substitute(self, var: str, replacement: 'Expr'):
        debug("Expr", "substitute", "Substituting {} in {} with {}", var, self, replacement)
        debug_stack_push()
        if self.tag == Expr.VAR and self.data == var:
            result = replacement
        elif self.tag == Expr.VAR or self.tag == Expr.INT or self.tag == Expr.DNE or self.tag == Expr.INF:
            result = self
        elif self.tag == Expr.NEG:
            assert type(self.data) is Expr
            result = -(self.data.substitute(var, replacement))
        elif self.tag in [Expr.ADD, Expr.MUL]:
            assert type(self.data) is list[Expr]
            result = Expr(self.tag, [item.substitute(var, replacement) for item in self.data])
        elif self.tag == Expr.DIV:
            assert type(self.data) is tuple[Expr, Expr]
            result = Expr(self.tag, tuple(item.substitute(var, replacement) for item in self.data))
        else:
            raise ValueError("Unknown tag: {}".format(self.tag))
        debug_stack_pop()
        return result

    def _tokenize(stream: StringStream):
        debug("Expr", "_tokenize", "Tokenizing stream {}", stream.remaining())
        debug_stack_push()
        tokens: list[Expr] = []
        while stream.is_valid():
            if stream.skip_if_eq("inf"):
                tokens.append(Expr.inf())
            elif stream.skip_if_eq("dne"):
                tokens.append(Expr.dne())
            else:
                ch = stream.take()
                if ch == ' ':
                    pass
                elif ch == '(':
                    debug("Expr", "_tokenize", "Pushing layer")
                    debug_stack_push()
                    sub_tokens = Expr._tokenize(stream)
                    tokens.append(sub_tokens) # todo
                elif ch == ')':
                    debug_stack_pop()
                    debug("Expr", "_tokenize", "Popping layer")
                    break
                elif ch == '*':
                    if stream.skip_if_eq('*'):
                        tokens.append(Expr(Expr.POW, None))
                    else:
                        tokens.append(Expr(Expr.MUL, None))
                elif ch == '+':
                    tokens.append(Expr(Expr.ADD, None))
                elif ch == '-':
                    tokens.append(Expr(Expr.NEG, None))
                elif ch == '/':
                    tokens.append(Expr(Expr.DIV, None))
                elif ch == '^':
                    tokens.append(Expr(Expr.POW, None))
                elif is_number(ch):
                    tokens.append(Expr(Expr.INT, int(stream.take_while(is_number))))
                elif is_letter(ch):
                    v = ch
                    if stream.skip_if_eq('_'):
                        v += '_'
                        if stream.skip_if_eq('{'):
                            v += stream.take_while(lambda ch: ch != '}')
                            stream.skip() # }
                        else:
                            v += stream.take()
                    v += stream.take_while(lambda ch: ch == '\'')
                    tokens.append(Expr(Expr.VAR, v))
                else:
                    raise ValueError(f"cannot match {stream.remaining()} to a token")
        debug_stack_pop()
        debug("Expr", "_tokenize", "Returning {}", tokens)
        return tokens

    def parse(text: str) -> 'Expr':
        tokens: list[Expr] = Expr._tokenize(StringStream(text))

        i = 0
        while i + 3 <= len(tokens):
            start, end = i, i + 3
            [lhs, op, rhs] = tokens[start:end]
            if op.data is None and op.tag == Expr.POW:
                tokens = [*tokens[:start], lhs ** rhs, *tokens[end:]]
                i = 0
            else:
                i += 1

        i = 0
        while i + 3 <= len(tokens):
            start, end = i, i + 3
            [lhs, op, rhs] = tokens[start:end]
            if op.data is None and (op.tag == Expr.MUL or op.tag == Expr.DIV):
                tokens = [*tokens[:start], lhs * rhs if op.tag == Expr.MUL else lhs / rhs, *tokens[end:]]
                i = 0
            else:
                i += 1

        i = 0
        while i + 3 <= len(tokens):
            start, end = i, i + 3
            [lhs, op, rhs] = tokens[start:end]
            if op.data is None and op.tag == Expr.ADD:
                tokens = [*tokens[:start], lhs + rhs, *tokens[end:]]
                i = 0
            else:
                i += 1

        return tokens[0]

    def _debug_tokens(tokens: list['Expr']):
        return ", ".join(["'{}'[{}]".format(token.tag, token.data) for token in tokens])

    def __str__(self):
        if self.tag == Expr.INT:
            return str(self.data)
        elif self.tag == Expr.VAR:
            return "({})".format(self.data)
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
