# Mathematical Laws

## Arithmetic
$$
\begin{align}
a + b &= b + a \\[1em]
a - b &= -b + a \\[1em]
a \cdot b &= b \cdot a \\[1em]
(a + b) + c &= a + (b + c) = a + b + c \\[1em]
a - (b + c) &= a - b - c \\[1em]
(a \cdot b) \cdot c &= a \cdot (b \cdot c) = a \cdot b \cdot c \\[1em]
a \cdot (b + c) &= a \cdot b + a \cdot c \\[1em]
\end{align}
$$

## Boolean
$$
\def\lnand{\barwedge}
\def\lnor{\:\overline{\vee}\:}
\def\lxor{\veebar}
\def\lxnor{\:\underline{\wedge}\:}
\def\true{1} % \top or 1
\def\false{0} % \bot or 0
\begin{align}
\lnot &= \text{NOT} \\[1em]
\land &= \text{AND} \\[1em]
\lnand &= \text{NAND} \\[1em]
\lor &= \text{OR} \\[1em]
\lnor &= \text{NOR} \\[1em]
\lxor &= \text{XOR} \\[1em]
\lxnor &= \text{XNOR} \\[1em]
% using only NOT and OR
a \lor b &= a \lor b \\[1em]
a \lnor b &= \lnot(a \lor b) \\[1em]
a \land b &= \lnot(\lnot a \lor \lnot b) \\[1em]
a \lnand b &= \lnot a \lor \lnot b \\[1em]
a \lxor b &= \lnot(\lnot (a \lor b) \lor \lnot(\lnot a \lor \lnot b)) \\[1em]
a \lxnor b &= \lnot(a \lor b) \lor \lnot (\lnot a \lor \lnot b) \\[1em]
% commutative
a \lor b &= b \lor a \\[1em]
a \lnor b &= b \lnor a \\[1em]
a \land b &= b \land a \\[1em]
a \lnand b &= b \lnand a \\[1em]
a \lxor b &= b \lxor a \\[1em]
a \lxnor b &= b \lxnor a \\[1em]
% associative
(a \land b) \land c &= a \land (b \land c) = a \land b \land c \\[1em]
(a \lor b) \lor c &= a \lor (b \lor c) = a \lor b \lor c \\[1em]
% negation
\lnot(\lnot x) &= x \\[1em]
\lnot(a \land b) &= (\lnot a \lor \lnot b) \\[1em]
\lnot(a \lor b) &= (\lnot a \land \lnot b) \\[1em]
(a \land b) \lor (a \land c) &= a \land (b \lor c) \\[1em]
(a \lor b) \land (a \lor c) &= a \lor (b \land c) \\[1em]
x \land x &= x \\[1em]
x \lor x &= x \\[1em]
x \land \true &= x \\[1em]
x \lor \false &= x \\[1em]
x \land \false &= \false \\[1em]
x \lor \true &= \true \\[1em]
\end{align}
$$

## Trig
$$
\begin{align}
\sin\theta &= \frac{y}{r} = \frac{1}{\csc\theta} \\[1em]
\cos\theta &= \frac{x}{r} = \frac{1}{\sec\theta} \\[1em]
\tan\theta &= \frac{y}{x} = \frac{1}{\cot\theta} = \frac{\sin\theta}{\cos\theta} \\[1em]
\csc\theta &= \frac{r}{y} = \frac{1}{\sin\theta} \\[1em]
\sec\theta &= \frac{r}{x} = \frac{1}{\cos\theta} \\[1em]
\cot\theta &= \frac{x}{y} = \frac{1}{\tan\theta} = \frac{\cos\theta}{\sin\theta} \\[1em]
\cos^2\theta+\sin^2\theta &= 1 \\[1em]
\sin^2\theta &= 1 - \cos^2 \theta \\[1em]
\sin\theta &= \pm\sqrt{1 - \cos^2 \theta} \\[1em]
\cos^2\theta &= 1 - \sin^2 \theta \\[1em]
\cos\theta &= \pm\sqrt{1 - \sin^2 \theta} \\[1em]
\sin(\alpha \pm \beta) &= \sin\alpha\cdot\cos\beta \pm \cos\alpha\cdot\sin\beta \\[1em]
\cos(\alpha \pm \beta) &= \cos\alpha\cdot\cos\beta \mp \sin\alpha\cdot\sin\beta \\[1em]
\tan(\alpha \pm \beta) &= \frac{\tan\alpha \pm \tan\beta}{1 \mp \tan\alpha\cdot\tan\beta} \\[1em]
\sin(2\theta) &= 2\sin\theta\cdot\cos\theta \\[1em]
\cos(2\theta) &= \cos^2\theta - \sin^2\theta \\[1em]
\tan(2\theta) &= \frac{2\tan\theta}{1 - \tan^2\theta} \\[1em]
\end{align}
$$

## Limits
Let $c$ be a constant and $n \in \N$
then
$$
\begin{align}
\lim_{x \to a}c &= c \\[1em]
\lim_{x \to a}x &= a \\[1em]
\lim_{x \to a}f(x) &= f(a) \\[1em]
\lim_{x \to a}\bigl(f(x) + g(x)\bigr) &= \lim_{x \to a} f(x) + \lim_{x \to a} g(x) \\[1em]
\lim_{x \to a}\bigl(f(x) - g(x)\bigr) &= \lim_{x \to a} f(x) - \lim_{x \to a} g(x) \\[1em]
\lim_{x \to a}\bigl(c \cdot f(x)\bigr) &= c \cdot \lim_{x \to a} f(x) \\[1em]
\lim_{x \to a}\bigl(f(x) \cdot g(x)\bigr) &= \lim_{x \to a} f(x) \cdot \lim_{x \to a} g(x) \\[1em]
\lim_{x \to a}\left(\frac{f(x)}{g(x)}\right) &= \frac{\displaystyle\lim_{x \to a} f(x)}{\displaystyle\lim_{x \to a} g(x)} \iff \lim_{x \to a} g(x) \ne 0 \\[1em]
\lim_{x \to a}{\bigl(f(x)\bigr)}^n &= {\left(\lim_{x \to a} f(x)\right)}^n \\[1em]
\lim_{x \to a}\sqrt[n]{f(x)} &= \sqrt[n]{\lim_{x \to a} f(x)} \\[1em]
\end{align}
$$

## Derivatives
Assume we want $\dfrac{d}{d\bm{x}}$. Let $c$ be a constant, $f$ and $g$ be functions, and $n \in \R$
then,
$$
\begin{align}
c' &= 0 \\[1em]
x' &= 1x^0 = 1 \\[1em]
{(c \cdot f(x))}' &= c \cdot f'(x) \\[1em]
{(f(x) \pm g(x))}' &= f'(x) \pm g'(x) \\[1em]
{(f(x) \cdot g(x))}' &= f'(x) \cdot g(x) + f(x) \cdot g'(x) \\[1em]
{\left(\frac{f(x)}{g(x)}\right)}' &= \frac{f'(x) \cdot g(x) - f(x) \cdot g'(x)}{g^2(x)} \\[1em]
{\left(x^n\right)}' &= n \cdot x^{n-1} \\[1em]
{\left(n^x\right)}' &= n^x \cdot \ln n \\[1em]
{\left(e^x\right)}' &= e^x \\[1em]
{\left(\log_n x\right)}' &= \frac{1}{x \cdot \ln n} \\[1em]
{\left(\ln x\right)}' &= \frac{1}{x} \\[1em]
{(f \circ g)}'(x) &= (f' \circ g)(x) \cdot g'(x) \\[1em]
{\left(y^2\right)}' &= 2y \cdot y' \\[1em]
\sin'x &= \cos x \\[1em]
\cos'x &= -\sin x \\[1em]
\tan'x &= \sec^2 x \\[1em]
\csc'x &= -\csc(x) \cdot \cot(x) \\[1em]
\sec'x &= \sec(x) \cdot \tan(x) \\[1em]
\cot'x &= -\csc^2 x \\[1em]
{\left(\sin^{-1}x\right)}' &= \frac{1}{\sqrt{1-x^2}} \\[1em]
{\left(\cos^{-1}x\right)}' &= \frac{-1}{\sqrt{1-x^2}} \\[1em]
{\left(\tan^{-1}x\right)}' &= \frac{1}{1+x^2} \\[1em]
\end{align}
$$

## Integration
$$
\begin{align}
\end{align}
$$
