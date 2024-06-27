import hashlib
import sol.ed25519

# https://datatracker.ietf.org/doc/html/rfc8032#ref-CURVE25519


def hash(data: bytearray) -> bytearray:
    return bytearray(hashlib.sha512(data).digest())


def pt_encode(pt: sol.ed25519.Pt) -> bytearray:
    n = pt.y.x | ((pt.x.x & 1) << 255)
    return bytearray(n.to_bytes(32, 'little'))


def sign(prikey: bytearray, m: bytearray) -> bytearray:
    assert len(prikey) == 32
    h = hash(prikey)
    a = int.from_bytes(h[:32], 'little')
    a &= (1 << 254) - 8
    a |= (1 << 254)
    a = sol.ed25519.Fr(a)
    prefix = h[32:]
    A = pt_encode(sol.ed25519.G * a)
    r = sol.ed25519.Fr(int.from_bytes(hash(prefix + m), 'little'))
    R = sol.ed25519.G * r
    Rs = pt_encode(R)
    h = sol.ed25519.Fr(int.from_bytes(hash(Rs + A + m), 'little'))
    s = r + h * a
    return Rs + bytearray(s.x.to_bytes(32, 'little'))
