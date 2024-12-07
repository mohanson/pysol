import typing


class ObjectDict(dict):
    def __getattr__(self, name: str) -> typing.Any:
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name: str, value: typing.Any):
        self[name] = value


develop = ObjectDict({
    'url': 'http://127.0.0.1:8899',
    # Solana's base fee is a fixed 5000 lamports (0.000005 SOL) per signature, and most transactions have one signature.
    'base_fee': 5000,
})

mainnet = ObjectDict({
    'url': 'https://api.mainnet-beta.solana.com',
    'base_fee': 5000,
})

testnet = ObjectDict({
    'url': 'https://api.devnet.solana.com',
    'base_fee': 5000,
})


current = develop
