import sol


def test_g():
    q = sol.ed25519.G * sol.ed25519.Fr(1)
    assert q.x.x == 0x0000000000000000000000000000000000000000000000000000000000000009
    q = sol.ed25519.G * sol.ed25519.Fr(2)
    assert q.x.x == 0x20d342d51873f1b7d9750c687d1571148f3f5ced1e350b5c5cae469cdd684efb
    q = sol.ed25519.G * sol.ed25519.Fr(3)
    assert q.x.x == 0x1c12bc1a6d57abe645534d91c21bba64f8824e67621c0859c00a03affb713c12
    q = sol.ed25519.G * sol.ed25519.Fr(4)
    assert q.x.x == 0x79ce98b7e0689d7de7d1d074a15b315ffe1805dfcd5d2a230fee85e4550013ef
    q = sol.ed25519.G * sol.ed25519.Fr(100000)
    assert q.x.x == 0x17f504b31019532d583f9873406aa6ff3046cfc66167b556ce800f569b2316a7
