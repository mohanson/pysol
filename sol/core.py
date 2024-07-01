import io
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


def compact_u16_encode(n: int) -> bytearray:
    # Same as u16, but serialized with 1 to 3 bytes. If the value is above 0x7f, the top bit is set and the remaining
    # value is stored in the next bytes. Each byte follows the same pattern until the 3rd byte. The 3rd byte, if
    # needed, uses all 8 bits to store the last byte of the original value.
    assert n >= 0
    assert n <= 0xffff
    if n <= 0x7f:
        return bytearray([n])
    if n <= 0x3fff:
        a = n & 0x7f | 0x80
        b = n >> 7
        return bytearray([a, b])
    if n <= 0xffff:
        a = n & 0x7f | 0x80
        n = n >> 7
        b = n & 0x7f | 0x80
        c = n >> 7
        return bytearray([a, b, c])
    raise Exception


def compact_u16_decode(data: bytearray) -> int:
    return compact_u16_decode_reader(io.BytesIO(data))


def compact_u16_decode_reader(reader: typing.BinaryIO) -> int:
    c = reader.read(1)[0]
    if c <= 0x7f:
        return c
    n = c & 0x7f
    c = reader.read(1)[0]
    m = c & 0x7f
    n += m << 7
    if c <= 0x7f:
        return n
    c = reader.read(1)[0]
    n += c << 14
    return n


class Instruction:
    def __init__(self, program_id_index: int, accounts: typing.List[int], data: bytearray) -> None:
        self.program_id_index = program_id_index
        self.accounts = accounts
        self.data = data

    def serialize(self) -> bytearray:
        r = bytearray()
        r.append(self.program_id_index)
        r.extend(compact_u16_encode(len(self.accounts)))
        for e in self.accounts:
            r.append(e)
        r.extend(compact_u16_encode(len(self.data)))
        r.extend(self.data)
        return r

    @staticmethod
    def serialize_decode(data: bytearray) -> Self:
        return Instruction.serialize_decode_reader(io.BytesIO(data))

    @staticmethod
    def serialize_decode_reader(reader: io.BytesIO) -> Self:
        i = Instruction(0, [], bytearray())
        i.program_id_index = int(reader.read(1)[0])
        for _ in range(compact_u16_decode_reader(reader)):
            i.accounts.append(int(reader.read(1)[0]))
        i.data = bytearray(reader.read(compact_u16_decode_reader(reader)))
        return i


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

    @staticmethod
    def serialize_decode(data: bytearray) -> Self:
        assert len(data) == 3
        return MessageHeader(data[0], data[1], data[2])

    @staticmethod
    def serialize_decode_reader(reader: io.BytesIO) -> Self:
        return MessageHeader.serialize_decode(bytearray(reader.read(3)))


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
        r.extend(compact_u16_encode(len(self.account_keys)))
        for e in self.account_keys:
            r.extend(e.p)
        r.extend(self.recent_blockhash)
        r.extend(compact_u16_encode(len(self.instructions)))
        for e in self.instructions:
            r.extend(e.serialize())
        return r

    @staticmethod
    def serialize_decode(data: bytearray) -> Self:
        return Message.serialize_decode_reader(io.BytesIO(data))

    @staticmethod
    def serialize_decode_reader(reader: io.BytesIO) -> Self:
        m = Message(MessageHeader.serialize_decode_reader(reader), [], bytearray(), [])
        for _ in range(compact_u16_decode_reader(reader)):
            m.account_keys.append(PubKey(bytearray(reader.read(32))))
        m.recent_blockhash = bytearray(reader.read(32))
        for _ in range(compact_u16_decode_reader(reader)):
            m. instructions.append(Instruction.serialize_decode_reader(reader))
        return m


class Transaction:
    def __init__(self, signatures: typing.List[bytearray], message: Message) -> None:
        self.signatures = signatures
        self.message = message

    def serialize(self) -> bytearray:
        r = bytearray()
        r.extend(compact_u16_encode(len(self.signatures)))
        for e in self.signatures:
            r.extend(e)
        r.extend(self.message.serialize())
        return r

    @staticmethod
    def serialize_decode(data: bytearray) -> Self:
        return Transaction.serialize_decode_reader(io.BytesIO(data))

    @staticmethod
    def serialize_decode_reader(reader: io.BytesIO) -> Self:
        s = []
        for _ in range(compact_u16_decode_reader(reader)):
            s.append(bytearray(reader.read(64)))
        return Transaction(s, Message.serialize_decode_reader(reader))
