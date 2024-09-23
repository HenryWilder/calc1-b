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

    def __init__(this, tag: str, data):
        this.tag = tag
        this.data = data
    
    def int(v: int):
        return Expr(Expr.INT, v)
    
    def var(v: str):
        return Expr(Expr.VAR, v)

    def inf():
        return Expr(Expr.INF, None)

    def dne():
        return Expr(Expr.DNE, None)

    def __neg__(this):
        return Expr(Expr.NEG, this)

    def __add__(this, other):
        terms = []
        for item in [this, other]:
            assert isinstance(item, Expr)
            if item.tag == Expr.ADD:
                terms.extend(item.data)
            else:
                terms.append(item)
        return Expr(Expr.ADD, terms)

    def __sub__(this, other):
        return this + (-other)

    def __mul__(this, other):
        factors = []
        for item in [this, other]:
            assert isinstance(item, Expr)
            if item.tag == Expr.MUL:
                factors.extend(item.data)
            else:
                factors.append(item)
        return Expr(Expr.MUL, factors)

    def __div__(this, other):
        return Expr(Expr.DIV, (this, other))

    def __pow__(this, other):
        return Expr(Expr.POW, (this, other))

    def substitute(this, var: str, replacement):
        if this.tag == Expr.VAR:
            assert isinstance(this.data, str)
            return replacement if this.data == var else this
        if this.tag == Expr.INT or this.tag == Expr.DNE or this.tag == Expr.INF:
            return this
        elif this.tag == Expr.NEG:
            assert isinstance(this.data, Expr)
            inner = this.data
            return -(inner.substitute(var, replacement))
        elif this.tag == Expr.ADD:
            assert type(this.data) is list[Expr]
            terms = this.data
            return Expr(Expr.ADD, [term.substitute(var, replacement) for term in terms])
        elif this.tag == Expr.MUL:
            assert type(this.data) is list[Expr]
            terms = this.data
            return Expr(Expr.MUL, [term.substitute(var, replacement) for term in terms])
        elif this.tag == Expr.DIV:
            assert type(this.data) is tuple[Expr, Expr]
            (p, q) = this.data
            return p.substitute(var, replacement) / q.substitute(var, replacement)
        elif this.tag == Expr.POW:
            assert type(this.data) is tuple[Expr, Expr]
            (b, p) = this.data
            return b.substitute(var, replacement) ** p.substitute(var, replacement)
        else:
            raise ValueError("Unknown tag: {}".format(this.tag))

    def parse(text: str):
        tokens: list[Expr] = []
        i = 0
        while i < len(text):
            ch = text[i]
            if ch == ' ':
                pass
            elif ch == '(' or ch == '[':
                tokens.append(Expr.parse(text[i:]))
            elif ch == ')' or ch == ']':
                break
            elif ch in "+-*/^":
                if ch in "+-/^":
                    op = ch
                elif ch == '*':
                    assert i + 1 < len(text), "'*' should never be the end of an expression"
                    if text[i + 1] == '*':
                        op = '^'
                        i += 1
                    else:
                        op = '*'
                if op == '+':
                    tag = Expr.ADD
                elif op == '-':
                    tag = Expr.NEG
                elif op == '*':
                    tag = Expr.MUL
                elif op == '/':
                    tag = Expr.DIV
                elif op == '^':
                    tag = Expr.POW
                tokens.append(Expr(tag, None))
            elif ch in "0123456789":
                start = i
                while i < len(text) and text[i] in "0123456789":
                    i += 1
                tokens.append(Expr(Expr.INT, int(text[start:i])))
            elif i + 2 < len(text) and text[i:i+2] == "inf":
                tokens.append(Expr.inf())
                i += 2
            elif i + 2 < len(text) and text[i:i+2] == "dne":
                tokens.append(Expr.dne())
                i += 2
            else:
                v = ch
                if i + 1 < len(text) and text[i + 1] == '_':
                    v += '_'
                    i += 1
                    if text[i + 1] == '{':
                        i += 2 # skip {}
                        while text[i] != '}':
                            v += text[i]
                            i += 1
                            assert i < len(text)
                while i + 1 < len(text) and text[i + 1] == '\'':
                    v += '\''
                    i += 1
                tokens.append(Expr(Expr.VAR, v))
            i += 1

        print(", ".join([str(token) for token in tokens]))

        i = len(tokens) - 1
        while i >= 0:
            tkn = tokens[i]
            if tkn.tag == Expr.NEG and tkn.data is None:
                if tokens[i + 1].tag is 
                i = len(tokens) - 1
            i -= 1

        print(", ".join([str(token) for token in tokens]))
        # assert len(tokens) == 1
        # return tokens[0]

    def debug_str(this):
        if type(this.data) is Expr:
            data_debug = this.data.debug_str()
        elif type(this.data) is list[Expr]:
            data_debug = ", ".join([item.debug_str() for item in this.data])
        elif type(this.data) is tuple[Expr, Expr]:
            (a, b) = this.data
            data_debug = a.debug_str() + ", " + b.debug_str()
        return "'{}'[{}]".format(this.tag, data_debug)
    
    def __str__(this):
        if this.tag == Expr.INT:
            return str(this.data)
        elif this.tag == Expr.VAR:
            return this.data
        elif this.tag == Expr.INF:
            return "∞"
        elif this.tag == Expr.DNE:
            return "DNE"
        elif this.tag == Expr.NEG:
            return "(-{})".format(this.data)
        elif this.tag == Expr.ADD or this.tag == Expr.MUL:
            separator = ("+" if this.tag == Expr.ADD else "*")
            return "({})".format(separator.join([str(item) for item in this.data]))
        elif this.tag == Expr.DIV or this.tag == Expr.POW:
            separator = ("/" if this.tag == Expr.DIV else "^")
            (a, b) = this.data
            return "({}{}{})".format(a, separator, b)
        else:
            return "[err: '{}' not recognized]".format(this.tag)

Expr.parse("29932*x_{99}'+633")
