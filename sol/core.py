import json
import sol.base58
import sol.eddsa
import typing
Self = typing.Self


class PriKey:
    def __init__(self, p: bytearray) -> None:
        assert len(p) == 32
        self.p = p

    def __repr__(self) -> str:
        return self.base58()

    def __eq__(self, other) -> bool:
        return self.p == other.p

    def base58(self) -> str:
        return sol.base58.encode(self.p)

    @staticmethod
    def base58_decode(data: str) -> Self:
        return PriKey(sol.base58.decode(data))

    def hex(self) -> str:
        return self.p.hex()

    @staticmethod
    def hex_decode(data: str) -> Self:
        return PriKey(bytearray.fromhex(data))

    def pubkey(self):
        return PubKey(sol.eddsa.pubkey(self.p))


class PubKey:
    def __init__(self, p: bytearray) -> None:
        assert len(p) == 32
        self.p = p

    def __repr__(self) -> str:
        return self.base58()

    def __eq__(self, other) -> bool:
        return self.p == other.p

    def base58(self) -> str:
        return sol.base58.encode(self.p)

    @staticmethod
    def base58_decode(data: str) -> Self:
        return PriKey(sol.base58.decode(data))

    def hex(self) -> str:
        return self.p.hex()

    @staticmethod
    def hex_decode(data: str) -> Self:
        return PriKey(bytearray.fromhex(data))
