import typing


class Fp:
    # Galois field. In mathematics, a finite field or Galois field is a field that contains a finite number of elements.
    # As with any field, a finite field is a set on which the operations of multiplication, addition, subtraction and
    # division are defined and satisfy certain basic rules.

    p = 0

    def __init__(self, x: int) -> None:
        self.x = x % self.p

    def __repr__(self) -> str:
        return f'Fp(0x{self.x:064x})'

    def __eq__(self, data: typing.Self) -> bool:
        assert self.p == data.p
        return self.x == data.x

    def __add__(self, data: typing.Self) -> typing.Self:
        assert self.p == data.p
        return self.__class__((self.x + data.x) % self.p)

    def __sub__(self, data: typing.Self) -> typing.Self:
        assert self.p == data.p
        return self.__class__((self.x - data.x) % self.p)

    def __mul__(self, data: typing.Self) -> typing.Self:
        assert self.p == data.p
        return self.__class__((self.x * data.x) % self.p)

    def __truediv__(self, data: typing.Self) -> typing.Self:
        return self * data ** -1

    def __pow__(self, data: int) -> typing.Self:
        return self.__class__(pow(self.x, data, self.p))

    def __pos__(self) -> typing.Self:
        return self

    def __neg__(self) -> typing.Self:
        return self.__class__(self.p - self.x)

    @classmethod
    def nil(cls) -> typing.Self:
        return cls(0)

    @classmethod
    def one(cls) -> typing.Self:
        return cls(1)


if __name__ == '__main__':
    Fp.p = 23
    assert Fp(12) + Fp(20) == Fp(9)
    assert Fp(8) * Fp(9) == Fp(3)
    assert Fp(8) ** -1 == Fp(3)
    Fp.p = 0

# Prime of finite field.
P = 0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffed
# The order n of G.
N = 0x1000000000000000000000000000000014def9dea2f79cd65812631a5cf5d3ed


class Fq(Fp):

    p = P

    def __repr__(self) -> str:
        return f'Fq(0x{self.x:064x})'


class Fr(Fp):

    p = N

    def __repr__(self) -> str:
        return f'Fr(0x{self.x:064x})'


A = -Fq(1)
D = -Fq(121665) / Fq(121666)


class Pt:

    def __init__(self, x: Fq, y: Fq) -> None:
        assert y * y - x * x == Fq(1) + D * x * x * y * y
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f'Pt({self.x}, {self.y})'

    def __eq__(self, data: typing.Self) -> bool:
        return all([
            self.x == data.x,
            self.y == data.y,
        ])

    def __add__(self, data: typing.Self) -> typing.Self:
        # https://datatracker.ietf.org/doc/html/rfc8032#ref-CURVE25519
        # Points on the curve form a group under addition, (x3, y3) = (x1, y1) + (x2, y2), with the formulas
        #           x1 * y2 + x2 * y1                y1 * y2 - a * x1 * x2
        # x3 = --------------------------,   y3 = ---------------------------
        #       1 + d * x1 * x2 * y1 * y2          1 - d * x1 * x2 * y1 * y2
        x1, x2 = self.x, data.x
        y1, y2 = self.y, data.y
        x3 = (x1 * y2 + x2 * y1) / (Fq(1) + D * x1 * x2 * y1 * y2)
        y3 = (y1 * y2 - A * x1 * x2) / (Fq(1) - D * x1 * x2 * y1 * y2)
        return Pt(x3, y3)

    def __sub__(self, data: typing.Self) -> typing.Self:
        return self + data.__neg__()

    def __mul__(self, k: Fr) -> typing.Self:
        # Point multiplication: Double-and-add
        # https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication
        n = k.x
        result = I
        addend = self
        while n:
            b = n & 1
            if b == 1:
                result += addend
            addend = addend + addend
            n = n >> 1
        return result

    def __truediv__(self, k: Fr) -> typing.Self:
        return self.__mul__(k ** -1)

    def __pos__(self) -> typing.Self:
        return self

    def __neg__(self) -> typing.Self:
        return Pt(-self.x, self.y)


# Identity element
I = Pt(
    Fq(0),
    Fq(1),
)
# Generator point
G = Pt(
    Fq(0x216936d3cd6e53fec0a4e231fdd6dc5c692cc7609525a7b2c9562d608f25d51a),
    Fq(0x6666666666666666666666666666666666666666666666666666666666666658),
)

if __name__ == '__main__':
    p = G * Fr(42)
    q = G * Fr(24)
    r = Pt(-p.x, p.y)
    assert p + q == G * Fr(66)
    assert p + p == G * Fr(84)
    assert p - q == G * Fr(18)
    assert r == -p
    assert p + r == I
    assert p + I == p
    assert p * Fr(42) == G * Fr(1764)
