import hashlib
import pxsol.ed25519

# Edwards-Curve Digital Signature Algorithm (EdDSA)
# See https://datatracker.ietf.org/doc/html/rfc8032#ref-CURVE25519


def hash(data: bytearray) -> bytearray:
    return bytearray(hashlib.sha512(data).digest())


def pt_encode(pt: pxsol.ed25519.Pt) -> bytearray:
    # A curve point (x,y), with coordinates in the range 0 <= x,y < p, is coded as follows. First, encode the
    # y-coordinate as a little-endian string of 32 octets. The most significant bit of the final octet is always zero.
    # To form the encoding of the point, copy the least significant bit of the x-coordinate to the most significant bit
    # of the final octet.
    # See https://datatracker.ietf.org/doc/html/rfc8032#section-5.1.2
    n = pt.y.x | ((pt.x.x & 1) << 255)
    return bytearray(n.to_bytes(32, 'little'))


def pt_decode(pt: bytearray) -> pxsol.ed25519.Pt:
    # Decoding a point, given as a 32-octet string, is a little more complicated.
    # See https://datatracker.ietf.org/doc/html/rfc8032#section-5.1.3
    #
    # First, interpret the string as an integer in little-endian representation. Bit 255 of this number is the least
    # significant bit of the x-coordinate and denote this value x_0. The y-coordinate is recovered simply by clearing
    # this bit. If the resulting value is >= p, decoding fails.
    uint = int.from_bytes(pt, 'little')
    sign = uint >> 255
    yint = uint & ((1 << 255) - 1)
    assert yint < pxsol.ed25519.P
    # To recover the x-coordinate, the curve equation implies x^2 = (y^2 - 1) / (d y^2 + 1) (mod p). The denominator is
    # always non-zero mod p.
    y = pxsol.ed25519.Fq(yint)
    x_x = (y * y - pxsol.ed25519.Fq(1)) / (pxsol.ed25519.D * y * y + pxsol.ed25519.Fq(1))
    # To compute the square root of (u/v), the first step is to compute the candidate root x = (u/v)^((p+3)/8).
    x = x_x ** ((pxsol.ed25519.P + 3) // 8)
    # Again, there are three cases:
    # 1. If v x^2 = u (mod p), x is a square root.
    # 2. If v x^2 = -u (mod p), set x <-- x * 2^((p-1)/4), which is a square root.
    # 3. Otherwise, no square root exists for modulo p, and decoding fails.
    if x*x != x_x:
        x = x * pxsol.ed25519.Fq(2) ** ((pxsol.ed25519.P - 1) // 4)
        assert x*x == x_x
    # Finally, use the x_0 bit to select the right square root. If x = 0, and x_0 = 1, decoding fails. Otherwise, if
    # x_0 != x mod 2, set x <-- p - x.  Return the decoded point (x,y).
    if x == pxsol.ed25519.Fq(0):
        assert not sign
    if x.x & 1 != sign:
        x = -x
    return pxsol.ed25519.Pt(x, y)


def pt_exists(pt: bytearray) -> bool:
    # Tests whether a point is on ed25519 curve.
    uint = int.from_bytes(pt, 'little')
    sign = uint >> 255
    yint = uint & ((1 << 255) - 1)
    if yint >= pxsol.ed25519.P:
        return False
    y = pxsol.ed25519.Fq(yint)
    x_x = (y * y - pxsol.ed25519.Fq(1)) / (pxsol.ed25519.D * y * y + pxsol.ed25519.Fq(1))
    x = x_x ** ((pxsol.ed25519.P + 3) // 8)
    if x*x != x_x:
        x = x * pxsol.ed25519.Fq(2) ** ((pxsol.ed25519.P - 1) // 4)
    if x*x != x_x:
        return False
    if x == pxsol.ed25519.Fq(0) and sign:
        return False
    return True


def pubkey(prikey: bytearray) -> bytearray:
    assert len(prikey) == 32
    h = hash(prikey)
    a = int.from_bytes(h[:32], 'little')
    a &= (1 << 254) - 8
    a |= (1 << 254)
    a = pxsol.ed25519.Fr(a)
    return pt_encode(pxsol.ed25519.G * a)


def sign(prikey: bytearray, m: bytearray) -> bytearray:
    # The inputs to the signing procedure is the private key, a 32-octet string, and a message M of arbitrary size.
    # See https://datatracker.ietf.org/doc/html/rfc8032#section-5.1.6
    assert len(prikey) == 32
    h = hash(prikey)
    a = int.from_bytes(h[:32], 'little')
    a &= (1 << 254) - 8
    a |= (1 << 254)
    a = pxsol.ed25519.Fr(a)
    prefix = h[32:]
    A = pt_encode(pxsol.ed25519.G * a)
    r = pxsol.ed25519.Fr(int.from_bytes(hash(prefix + m), 'little'))
    R = pxsol.ed25519.G * r
    Rs = pt_encode(R)
    h = pxsol.ed25519.Fr(int.from_bytes(hash(Rs + A + m), 'little'))
    s = r + h * a
    return Rs + bytearray(s.x.to_bytes(32, 'little'))


def verify(pubkey: bytearray, m: bytearray, sig: bytearray) -> bool:
    # Verify a signature on a message using public key.
    # See https://datatracker.ietf.org/doc/html/rfc8032#section-5.1.7
    assert len(pubkey) == 32
    assert len(sig) == 64
    A = pt_decode(pubkey)
    Rs = sig[:32]
    R = pt_decode(Rs)
    s = pxsol.ed25519.Fr(int.from_bytes(sig[32:], 'little'))
    h = pxsol.ed25519.Fr(int.from_bytes(hash(Rs + pubkey + m), 'little'))
    sB = pxsol.ed25519.G * s
    hA = A * h
    return sB == R + hA
