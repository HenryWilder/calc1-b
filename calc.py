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
        for item in list[Expr]([this, other]):
            if item.tag == Expr.ADD:
                terms.extend(item.data)
            else:
                terms.append(item)
        return Expr(Expr.ADD, terms)

    def __sub__(this, other):
        return this + (-other)

    def __mul__(this, other):
        factors = []
        for x in list[Expr]([this, other]):
            if x.tag == Expr.MUL:
                factors.extend(x.data)
            else:
                factors.append(x)
        return Expr(Expr.MUL, factors)

    def __div__(this, other):
        return Expr(Expr.DIV, (this, other))

    def __pow__(this, other):
        return Expr(Expr.POW, (this, other))

    def substitute(this, var: str, replacement):
        if this.tag == Expr.VAR:
            return replacement
        if this.tag == Expr.INT or this.tag == Expr.DNE or this.tag == Expr.INF:
            return this
        elif this.tag == Expr.NEG:
            inner: Expr = this.data
            return -(inner.substitute(var, replacement))
        elif this.tag == Expr.ADD:
            terms: list[Expr] = this.data
            return Expr(Expr.ADD, [term.substitute(var, replacement) for term in terms])
        elif this.tag == Expr.MUL:
            terms: list[Expr] = this.data
            return Expr(Expr.MUL, [term.substitute(var, replacement) for term in terms])
        elif this.tag == Expr.DIV:
            (p, q): tuple[Expr, Expr] = this.data
            return p.substitute(var, replacement) / q.substitute(var, replacement)
        elif this.tag == Expr.POW:
            (b, p): tuple[Expr, Expr] = this.data
            return b.substitute(var, replacement) ** p.substitute(var, replacement)
        else:
            raise ValueError("Unknown tag: {}".format(this.tag))

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
        elif this.tag == Expr.ADD:
            return "({})".format("+".join([str(term) for term in this.data]))
        elif this.tag == Expr.MUL:
            return "({})".format("*".join([str(factor) for factor in this.data]))
        elif this.tag == Expr.DIV:
            (p, q) = this.data
            return "({}/{})".format(p, q)
        elif this.tag == Expr.POW:
            (b, p) = this.data
            return "({}^{})".format(b, p)
        else:
            return "[err: '{}' not recognized]".format(this.tag)

print(Expr.var("x")+Expr.int(3)+Expr.int(7)-Expr.inf())
print(Expr.var("x")**Expr.int(3))
