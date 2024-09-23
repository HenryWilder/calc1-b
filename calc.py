class Expr:
    def __init__(this, t, v):
        this.t = t
        this.v = v
    
    def int(v): # int
        return Expr("int", v)
    
    def var(v): # str
        return Expr("var", v)

    def inf():
        return Expr("infty", None)

    def dne():
        return Expr("dne", None)

    def __neg__(this):
        return Expr("neg", this)

    def __add__(this, other):
        return Expr("add", [this, other])

    def __sub__(this, other):
        return Expr("add", [this, -other])

    def __mul__(this, other):
        return Expr("mul", [this, other])

    def __div__(this, other):
        return Expr("div", (this, other))

    def __pow__(this, other):
        return Expr("pow", (this, other))

    def __str__(this):
        t,v = this.t,this.v
        if t=="int":
            return str(v)
        elif t=="var":
            return v
        elif t=="infty":
            return "∞"
        elif t=="dne":
            return "DNE"
        elif t=="neg":
            return "(-{})".format(v)
        elif t=="add":
            return "({}+{})".format(v[0],v[1])
        elif t=="mul":
            return "({}*{})".format(v[0],v[1])
        elif t=="div":
            (p,q)=v
            return "({}/{})".format(p,q)
        elif t=="pow":
            (b,p)=v
            return "({}^{})".format(b,p)
        else:
            return "[err]"

print(Expr.var("x")-Expr.inf())
print(Expr.var("x")**Expr.int(3))
