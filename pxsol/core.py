import hashlib
import io
import json
import pxsol.base58
import pxsol.eddsa
import typing


class PriKey:
    # Solana's private key is a 32-byte array, selected arbitrarily. In general, the private key is not used in
    # isolation; instead, it forms a 64-byte keypair together with the public key, which is also a 32-byte array.
    # Most solana wallets, such as phantom, import and export private keys in base58-encoded keypair format.

    def __init__(self, p: bytearray) -> None:
        assert len(p) == 32
        self.p = p

    def __repr__(self) -> str:
        return self.base58()

    def __eq__(self, other) -> bool:
        return self.p == other.p

    def base58(self) -> str:
        return pxsol.base58.encode(self.p)

    @classmethod
    def base58_decode(cls, data: str) -> typing.Self:
        return PriKey(pxsol.base58.decode(data))

    def hex(self) -> str:
        return self.p.hex()

    @classmethod
    def hex_decode(cls, data: str) -> typing.Self:
        return PriKey(bytearray.fromhex(data))

    def pubkey(self):
        # Get the public key.
        return PubKey(pxsol.eddsa.pubkey(self.p))

    def sign(self, data: bytearray) -> bytearray:
        # Use this private key to sign a message of arbitrary length. The resulting signature is deterministic.
        return pxsol.eddsa.sign(self.p, data)

    def wif(self) -> str:
        pubkey = self.pubkey()
        return pxsol.base58.encode(self.p + pubkey.p)

    @classmethod
    def wif_decode(cls, data: str) -> typing.Self:
        pripub = pxsol.base58.decode(data)
        prikey = PriKey(pripub[:32])
        pubkey = PubKey(pripub[32:])
        assert prikey.pubkey() == pubkey
        return prikey


class PubKey:
    # Solana's public key is a 32-byte array. The base58 representation of the public key is also referred to as the
    # address.

    def __init__(self, p: bytearray) -> None:
        assert len(p) == 32
        self.p = p

    def __repr__(self) -> str:
        return self.base58()

    def __eq__(self, other) -> bool:
        return self.p == other.p

    def base58(self) -> str:
        return pxsol.base58.encode(self.p)

    @classmethod
    def base58_decode(cls, data: str) -> typing.Self:
        return PubKey(pxsol.base58.decode(data))

    def derive(self, seed: bytearray) -> typing.Self:
        # Program Derived Address (PDA). PDAs are addresses derived deterministically using a combination of user-defined
        # seeds, a bump seed, and a program's ID.
        # See: https://solana.com/docs/core/pda
        data = bytearray()
        data.extend(seed)
        data.append(0xff)
        data.extend(self.p)
        data.extend(bytearray('ProgramDerivedAddress'.encode()))
        for i in range(255, -1, -1):
            data[len(seed)] = i
            hash = bytearray(hashlib.sha256(data).digest())
            # The pda should fall off the ed25519 curve.
            if not pxsol.eddsa.pt_exists(hash):
                return PubKey(hash)
        raise Exception

    def hex(self) -> str:
        return self.p.hex()

    @classmethod
    def hex_decode(cls, data: str) -> typing.Self:
        return PubKey(bytearray.fromhex(data))


class ProgramClock:

    pubKey = PubKey.base58_decode('SysvarC1ock11111111111111111111111111111111')


class ProgramLoaderUpgradeable:

    pubkey = PubKey.base58_decode('BPFLoaderUpgradeab1e11111111111111111111111')

    size_uninitialized = 4  # Size of a serialized program account.
    size_buffer_metadata = 37  # Size of a buffer account's serialized metadata.
    size_program_data_metadata = 45  # Size of a programdata account's serialized metadata.
    size_program = 36  # Size of a serialized program account.

    @classmethod
    def initialize_buffer(cls) -> bytearray:
        r = bytearray()
        r.extend(bytearray([0x00, 0x00, 0x00, 0x00]))
        return r

    @classmethod
    def write(cls, offset: int, data: bytearray) -> bytearray:
        r = bytearray()
        r.extend(bytearray([0x01, 0x00, 0x00, 0x00]))
        r.extend(bytearray(offset.to_bytes(4, 'little')))
        r.extend(bytearray(len(data).to_bytes(8, 'little')))
        r.extend(data)
        return r

    @classmethod
    def deploy_with_max_data_len(cls, size: int) -> bytearray:
        r = bytearray()
        r.extend(bytearray([0x02, 0x00, 0x00, 0x00]))
        r.extend(bytearray(size.to_bytes(8, 'little')))
        return r

    @classmethod
    def upgrade(cls) -> bytearray:
        r = bytearray()
        r.extend(bytearray([0x03, 0x00, 0x00, 0x00]))
        return r

    @classmethod
    def set_authority(cls):
        pass

    @classmethod
    def close(cls):
        r = bytearray()
        r.extend(bytearray([0x05, 0x00, 0x00, 0x00]))
        return r

    @classmethod
    def extend_program(cls):
        pass

    @classmethod
    def set_authority_checked(cls):
        pass


class ProgramRent:

    pubkey = PubKey.base58_decode('SysvarRent111111111111111111111111111111111')


class ProgramSystem:

    pubkey = PubKey(bytearray(32))

    @classmethod
    def create(cls, value: int, space: int, program_id: PubKey) -> bytearray:
        r = bytearray()
        r.extend(bytearray([0x00, 0x00, 0x00, 0x00]))
        r.extend(bytearray(int(value).to_bytes(8, 'little')))
        r.extend(bytearray(int(space).to_bytes(8, 'little')))
        r.extend(program_id.p)
        return r

    @classmethod
    def assign(cls):
        pass

    @classmethod
    def transfer(cls, value: int) -> bytearray:
        r = bytearray()
        r.extend(bytearray([0x02, 0x00, 0x00, 0x00]))
        r.extend(bytearray(int(value).to_bytes(8, 'little')))
        return r

    @classmethod
    def create_with_seed(cls):
        pass

    @classmethod
    def advance_nonce_account(cls):
        pass

    @classmethod
    def withdraw_nonce_account(cls):
        pass

    @classmethod
    def initialize_nonce_account(cls):
        pass

    @classmethod
    def authorize_nonce_account(cls):
        pass

    @classmethod
    def allocate(cls):
        pass

    @classmethod
    def allocate_with_seed(cls):
        pass

    @classmethod
    def assign_with_seed(cls):
        pass

    @classmethod
    def transfer_with_seed(cls):
        pass

    @classmethod
    def upgrade_nonce_account(cls):
        pass


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
    # A compact encoding of an instruction.

    def __init__(self, program_id_index: int, accounts: typing.List[int], data: bytearray) -> None:
        # Identifies an on-chain program that will process the instruction. This is represented as an u8 index pointing
        # to an account address within the account addresses array.
        self.program_id_index = program_id_index
        # Array of u8 indexes pointing to the account addresses array for each account required by the instruction.
        self.accounts = accounts
        # A u8 byte array specific to the program invoked. This data specifies the instruction to invoke on the program
        # along with any additional data that the instruction requires (such as function arguments).
        self.data = data

    def __repr__(self) -> str:
        return json.dumps(self.json())

    def json(self) -> typing.Dict:
        return {
            'programIdIndex': self.program_id_index,
            'accounts': self.accounts,
            'data': pxsol.base58.encode(self.data)
        }

    @classmethod
    def json_decode(cls, data: typing.Dict) -> typing.Self:
        return Instruction(data['programIdIndex'], data['accounts'], pxsol.base58.decode(data['data']))

    def serialize(self) -> bytearray:
        r = bytearray()
        r.append(self.program_id_index)
        r.extend(compact_u16_encode(len(self.accounts)))
        for e in self.accounts:
            r.append(e)
        r.extend(compact_u16_encode(len(self.data)))
        r.extend(self.data)
        return r

    @classmethod
    def serialize_decode(cls, data: bytearray) -> typing.Self:
        return Instruction.serialize_decode_reader(io.BytesIO(data))

    @classmethod
    def serialize_decode_reader(cls, reader: io.BytesIO) -> typing.Self:
        i = Instruction(0, [], bytearray())
        i.program_id_index = int(reader.read(1)[0])
        for _ in range(compact_u16_decode_reader(reader)):
            i.accounts.append(int(reader.read(1)[0]))
        i.data = bytearray(reader.read(compact_u16_decode_reader(reader)))
        return i


class MessageHeader:
    # The message header specifies the privileges of accounts included in the transaction's account address array. It
    # is comprised of three bytes, each containing a u8 integer, which collectively specify:
    # 1. The number of required signatures for the transaction.
    # 2. The number of read-only account addresses that require signatures.
    # 3. The number of read-only account addresses that do not require signatures.

    def __init__(
        self,
        num_required_signatures: int,
        num_readonly_signed_accounts: int,
        num_readonly_unsigned_accounts: int
    ) -> None:
        self.num_required_signatures = num_required_signatures
        self.num_readonly_signed_accounts = num_readonly_signed_accounts
        self.num_readonly_unsigned_accounts = num_readonly_unsigned_accounts

    def __repr__(self) -> str:
        return json.dumps(self.json())

    def json(self) -> typing.Dict:
        return {
            'numRequiredSignatures': self.num_required_signatures,
            'numReadonlySignedAccounts': self.num_readonly_signed_accounts,
            'numReadonlyUnsignedAccounts': self.num_readonly_unsigned_accounts,
        }

    @classmethod
    def json_decode(cls, data: str) -> typing.Self:
        return MessageHeader(
            data['numRequiredSignatures'],
            data['numReadonlySignedAccounts'],
            data['numReadonlyUnsignedAccounts'],
        )

    def serialize(self) -> bytearray:
        return bytearray([
            self.num_required_signatures,
            self.num_readonly_signed_accounts,
            self.num_readonly_unsigned_accounts,
        ])

    @classmethod
    def serialize_decode(cls, data: bytearray) -> typing.Self:
        assert len(data) == 3
        return MessageHeader(data[0], data[1], data[2])

    @classmethod
    def serialize_decode_reader(cls, reader: io.BytesIO) -> typing.Self:
        return MessageHeader.serialize_decode(bytearray(reader.read(3)))


class Message:
    # List of instructions to be processed atomically.

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

    def __repr__(self) -> str:
        return json.dumps(self.json())

    def json(self) -> typing.Dict:
        return {
            'header': self.header.json(),
            'accountKeys': [e.base58() for e in self.account_keys],
            'recentBlockhash': pxsol.base58.encode(self.recent_blockhash),
            'instructions': [e.json() for e in self.instructions],
        }

    @classmethod
    def json_decode(cls, data: str) -> typing.Self:
        return Message(
            MessageHeader.json_decode(data['header']),
            [PubKey.base58_decode(e) for e in data['accountKeys']],
            pxsol.base58.decode(data['recentBlockhash']),
            [Instruction.json_decode(e) for e in data['instructions']]
        )

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

    @classmethod
    def serialize_decode(cls, data: bytearray) -> typing.Self:
        return Message.serialize_decode_reader(io.BytesIO(data))

    @classmethod
    def serialize_decode_reader(cls, reader: io.BytesIO) -> typing.Self:
        m = Message(MessageHeader.serialize_decode_reader(reader), [], bytearray(), [])
        for _ in range(compact_u16_decode_reader(reader)):
            m.account_keys.append(PubKey(bytearray(reader.read(32))))
        m.recent_blockhash = bytearray(reader.read(32))
        for _ in range(compact_u16_decode_reader(reader)):
            m. instructions.append(Instruction.serialize_decode_reader(reader))
        return m


class Transaction:
    # An atomically-committed sequence of instructions.

    def __init__(self, signatures: typing.List[bytearray], message: Message) -> None:
        self.signatures = signatures
        self.message = message

    def __repr__(self) -> str:
        return json.dumps(self.json())

    def json(self) -> typing.Dict:
        return {
            'signatures': [pxsol.base58.encode(e) for e in self.signatures],
            'message': self.message.json()
        }

    @classmethod
    def json_decode(cls, data: typing.Dict) -> typing.Self:
        return Transaction([pxsol.base58.decode(e) for e in data['signatures']], Message.json_decode(data['message']))

    def serialize(self) -> bytearray:
        r = bytearray()
        r.extend(compact_u16_encode(len(self.signatures)))
        for e in self.signatures:
            r.extend(e)
        r.extend(self.message.serialize())
        return r

    @classmethod
    def serialize_decode(cls, data: bytearray) -> typing.Self:
        return Transaction.serialize_decode_reader(io.BytesIO(data))

    @classmethod
    def serialize_decode_reader(cls, reader: io.BytesIO) -> typing.Self:
        s = []
        for _ in range(compact_u16_decode_reader(reader)):
            s.append(bytearray(reader.read(64)))
        return Transaction(s, Message.serialize_decode_reader(reader))
