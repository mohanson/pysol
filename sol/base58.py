# Copyright (C) 2011 Sam Rushing
# Copyright (C) 2013-2014 The python-bitcoinlib developers
#
# This file is part of python-bitcoinlib.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-bitcoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

# Base58 encoding and decoding

B58_DIGITS = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def encode(b: bytearray) -> str:
    # Encode bytes to a base58-encoded string
    assert isinstance(b, bytearray)
    # Convert big-endian bytes to integer
    n = int.from_bytes(b)
    # Divide that integer into bas58
    res = []
    while n > 0:
        n, r = divmod(n, 58)
        res.append(B58_DIGITS[r])
    res = ''.join(res[::-1])
    # Encode leading zeros as base58 zeros
    czero = 0
    pad = 0
    for c in b:
        if c == czero:
            pad += 1
        else:
            break
    return B58_DIGITS[0] * pad + res


def decode(s: str) -> bytearray:
    # Decode a base58-encoding string, returning bytes.
    if not s:
        return bytearray()
    # Convert the string to an integer
    n = 0
    for c in s:
        n *= 58
        assert c in B58_DIGITS
        digit = B58_DIGITS.index(c)
        n += digit
    # Convert the integer to bytes
    res = bytearray(n.to_bytes(max((n.bit_length() + 7) // 8, 1)))
    # Add padding back.
    pad = 0
    for c in s[:-1]:
        if c == B58_DIGITS[0]:
            pad += 1
        else:
            break
    return bytearray(pad) + res
