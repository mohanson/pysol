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


class Instruction:
    def __init__(self, program_id_index: int, accounts: typing.List[int], data: bytearray) -> None:
        self.program_id_index = program_id_index
        self.accounts = accounts
        self.data = data

    def serialize(self) -> bytearray:
        r = bytearray()
        r.append(self.program_id_index)
        r.append(len(self.accounts))
        for e in self.accounts:
            r.append(e)
        r.append(len(self.data))
        r.extend(self.data)
        return r


class MessageHeader:
    def __init__(
        self,
        num_required_signatures: int,
        num_readonly_signed_accounts: int,
        num_readonly_unsigned_accounts: int
    ) -> None:
        self.num_required_signatures = num_required_signatures
        self.num_readonly_signed_accounts = num_readonly_signed_accounts
        self.num_readonly_unsigned_accounts = num_readonly_unsigned_accounts

    def serialize(self) -> bytearray:
        return bytearray([
            self.num_required_signatures,
            self.num_readonly_signed_accounts,
            self.num_readonly_unsigned_accounts,
        ])


class Message:
    def __init__(
        self,
        header: MessageHeader,
        account_keys: typing.List[PubKey],
        recent_blockhash: bytearray,
        instructions: typing.List[Instruction]
    ) -> None:
        self.header = header
        self.account_keys = account_keys
        self.recent_blockhash = recent_blockhash
        self.instructions = instructions

    def serialize(self) -> bytearray:
        r = bytearray()
        r.extend(self.header.serialize())
        r.append(len(self.account_keys))
        for e in self.account_keys:
            r.extend(e.p)
        r.extend(self.recent_blockhash)
        r.append(len(self.instructions))
        for e in self.instructions:
            r.extend(e.serialize())
        return r


class Transaction:
    def __init__(self, signatures: typing.List[bytearray], message: Message) -> None:
        self.signatures = signatures
        self.message = message

    def serialize(self) -> bytearray:
        r = bytearray()
        r.append(len(self.signatures))
        for e in self.signatures:
            r.extend(e)
        r.extend(self.message.serialize())
        return r
