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
})

mainnet = ObjectDict({
    'url': 'https://api.mainnet-beta.solana.com',
})

testnet = ObjectDict({
    'url': 'https://api.devnet.solana.com',
})


current = develop
