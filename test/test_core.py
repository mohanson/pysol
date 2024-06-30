import sol


def test_addr():
    prikey = sol.core.PriKey(bytearray(int(1).to_bytes(32)))
    pubkey = prikey.pubkey()
    assert pubkey.base58() == '6ASf5EcmmEHTgDJ4X4ZT5vT6iHVJBXPg5AN5YoTCpGWt'
    prikey = sol.core.PriKey(bytearray(int(2).to_bytes(32)))
    pubkey = prikey.pubkey()
    assert pubkey.base58() == '8pM1DN3RiT8vbom5u1sNryaNT1nyL8CTTW3b5PwWXRBH'
