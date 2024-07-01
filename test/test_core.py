import random
import sol


def test_addr():
    prikey = sol.core.PriKey(bytearray(int(1).to_bytes(32)))
    pubkey = prikey.pubkey()
    assert pubkey.base58_encode() == '6ASf5EcmmEHTgDJ4X4ZT5vT6iHVJBXPg5AN5YoTCpGWt'
    prikey = sol.core.PriKey(bytearray(int(2).to_bytes(32)))
    pubkey = prikey.pubkey()
    assert pubkey.base58_encode() == '8pM1DN3RiT8vbom5u1sNryaNT1nyL8CTTW3b5PwWXRBH'


def test_compact_u16_encode():
    assert sol.core.compact_u16_encode(0x0000), bytearray([0x00])
    assert sol.core.compact_u16_encode(0x007f), bytearray([0x7f])
    assert sol.core.compact_u16_encode(0x0080), bytearray([0x80, 0x01])
    assert sol.core.compact_u16_encode(0x00ff), bytearray([0xff, 0x01])
    assert sol.core.compact_u16_encode(0x0100), bytearray([0x80, 0x02])
    assert sol.core.compact_u16_encode(0x7fff), bytearray([0xff, 0xff, 0x01])
    assert sol.core.compact_u16_encode(0xffff), bytearray([0xff, 0xff, 0x03])


def test_compact_u16_decode():
    assert sol.core.compact_u16_decode(bytearray([0x00])) == 0x0000
    assert sol.core.compact_u16_decode(bytearray([0x7f])) == 0x007f
    assert sol.core.compact_u16_decode(bytearray([0x80, 0x01])) == 0x0080
    assert sol.core.compact_u16_decode(bytearray([0xff, 0x01])) == 0x00ff
    assert sol.core.compact_u16_decode(bytearray([0x80, 0x02])) == 0x0100
    assert sol.core.compact_u16_decode(bytearray([0xff, 0xff, 0x01])) == 0x7fff
    assert sol.core.compact_u16_decode(bytearray([0xff, 0xff, 0x03])) == 0xffff


def test_compact_u16_random():
    for _ in range(8):
        n = random.randint(0, 0xffff)
        assert sol.core.compact_u16_decode(sol.core.compact_u16_encode(n)) == n
