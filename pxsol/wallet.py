import base64
import json
import pxsol.base58
import pxsol.config
import pxsol.core
import pxsol.denomination
import pxsol.rpc
import random
import typing


class Wallet:
    # A built-in solana wallet that can be used to perform most on-chain operations.

    def __init__(self, prikey: pxsol.core.PriKey) -> None:
        self.prikey = prikey
        self.pubkey = prikey.pubkey()

    def __repr__(self) -> str:
        return json.dumps(self.json())

    def json(self) -> typing.Dict:
        return {
            'prikey': self.prikey.base58(),
            'pubkey': self.pubkey.base58(),
        }

    def balance(self) -> int:
        # Returns the lamport balance of the account.
        return pxsol.rpc.get_balance(self.pubkey.base58(), {})

    def program_buffer_closed(self, program_buffer_pubkey: pxsol.core.PubKey) -> None:
        # Close a buffer account. This method is used to withdraw all lamports when the buffer account is no longer in
        # use due to unexpected errors.
        tx = pxsol.core.Transaction([], pxsol.core.Message(pxsol.core.MessageHeader(1, 0, 1), [], bytearray(), []))
        tx.message.account_keys.append(self.pubkey)
        tx.message.account_keys.append(program_buffer_pubkey)
        tx.message.account_keys.append(pxsol.core.ProgramLoaderUpgradeable.pubkey)
        tx.message.recent_blockhash = pxsol.base58.decode(pxsol.rpc.get_latest_blockhash({})['blockhash'])
        tx.message.instructions.append(pxsol.core.Instruction(
            2, [1, 0, 0], pxsol.core.ProgramLoaderUpgradeable.close()))
        tx.signatures.append(self.prikey.sign(tx.message.serialize()))
        txid = pxsol.rpc.send_transaction(base64.b64encode(tx.serialize()).decode(), {})
        pxsol.rpc.wait([txid])

    def program_buffer_create(self, program: bytearray) -> pxsol.core.PubKey:
        # Writes a program into a buffer account. The buffer account is randomly generated, and its public key serves
        # as the function's return value.
        program_buffer_prikey = pxsol.core.PriKey(bytearray(random.randbytes(32)))
        program_buffer_pubkey = program_buffer_prikey.pubkey()
        program_data_size = pxsol.core.ProgramLoaderUpgradeable.size_program_data_metadata + len(program)
        # Sends a transaction which creates a buffer account large enough for the byte-code being deployed. It also
        # invokes the initialize buffer instruction to set the buffer authority to restrict writes to the deployer's
        # chosen address.
        tx = pxsol.core.Transaction([], pxsol.core.Message(pxsol.core.MessageHeader(2, 0, 2), [], bytearray(), []))
        tx.message.account_keys.append(self.pubkey)
        tx.message.account_keys.append(program_buffer_pubkey)
        tx.message.account_keys.append(pxsol.core.ProgramSystem.pubkey)
        tx.message.account_keys.append(pxsol.core.ProgramLoaderUpgradeable.pubkey)
        tx.message.recent_blockhash = pxsol.base58.decode(pxsol.rpc.get_latest_blockhash({})['blockhash'])
        tx.message.instructions.append(pxsol.core.Instruction(2, [0, 1], pxsol.core.ProgramSystem.create(
            pxsol.rpc.get_minimum_balance_for_rent_exemption(program_data_size, {}),
            pxsol.core.ProgramLoaderUpgradeable.size_buffer_metadata + len(program),
            pxsol.core.ProgramLoaderUpgradeable.pubkey,
        )))
        tx.message.instructions.append(pxsol.core.Instruction(
            3, [1, 0], pxsol.core.ProgramLoaderUpgradeable.initialize_buffer()))
        tx.signatures.append(self.prikey.sign(tx.message.serialize()))
        tx.signatures.append(program_buffer_prikey.sign(tx.message.serialize()))
        txid = pxsol.rpc.send_transaction(base64.b64encode(tx.serialize()).decode(), {})
        pxsol.rpc.wait([txid])
        # Breaks up the program byte-code into ~1KB chunks and sends transactions to write each chunk with the write
        # buffer instruction.
        size = 1012
        hall = []
        for i in range(0, len(program), size):
            elem = program[i:i+size]
            tx = pxsol.core.Transaction([], pxsol.core.Message(pxsol.core.MessageHeader(1, 0, 1), [], bytearray(), []))
            tx.message.account_keys.append(self.pubkey)
            tx.message.account_keys.append(program_buffer_pubkey)
            tx.message.account_keys.append(pxsol.core.ProgramLoaderUpgradeable.pubkey)
            tx.message.recent_blockhash = pxsol.base58.decode(pxsol.rpc.get_latest_blockhash({})['blockhash'])
            tx.message.instructions.append(pxsol.core.Instruction(
                2, [1, 0], pxsol.core.ProgramLoaderUpgradeable.write(i, elem)))
            tx.signatures.append(self.prikey.sign(tx.message.serialize()))
            assert len(tx.serialize()) <= 1232
            txid = pxsol.rpc.send_transaction(base64.b64encode(tx.serialize()).decode(), {})
            hall.append(txid)
        pxsol.rpc.wait(hall)
        return program_buffer_pubkey

    def program_closed(self, program_pubkey: pxsol.core.PubKey) -> None:
        # Close a program. The sol allocated to the on-chain program can be fully recovered by performing this action.
        program_data_pubkey = pxsol.core.ProgramLoaderUpgradeable.pubkey.derive(program_pubkey.p)
        tx = pxsol.core.Transaction([], pxsol.core.Message(pxsol.core.MessageHeader(1, 0, 1), [], bytearray(), []))
        tx.message.account_keys.append(self.pubkey)
        tx.message.account_keys.append(program_pubkey)
        tx.message.account_keys.append(program_data_pubkey)
        tx.message.account_keys.append(pxsol.core.ProgramLoaderUpgradeable.pubkey)
        tx.message.recent_blockhash = pxsol.base58.decode(pxsol.rpc.get_latest_blockhash({})['blockhash'])
        tx.message.instructions.append(pxsol.core.Instruction(
            3, [2, 0, 0, 1], pxsol.core.ProgramLoaderUpgradeable.close()))
        tx.signatures.append(self.prikey.sign(tx.message.serialize()))
        txid = pxsol.rpc.send_transaction(base64.b64encode(tx.serialize()).decode(), {})
        pxsol.rpc.wait([txid])

    def program_deploy(self, program: bytearray) -> pxsol.core.PubKey:
        # Deploying a program on solana, returns the program's public key.
        program_buffer_pubkey = self.program_buffer_create(program)
        program_prikey = pxsol.core.PriKey(bytearray(random.randbytes(32)))
        program_pubkey = program_prikey.pubkey()
        program_data_pubkey = pxsol.core.ProgramLoaderUpgradeable.pubkey.derive(program_pubkey.p)
        # Deploy with max data len.
        tx = pxsol.core.Transaction([], pxsol.core.Message(pxsol.core.MessageHeader(2, 0, 4), [], bytearray(), []))
        tx.message.account_keys.append(self.pubkey)
        tx.message.account_keys.append(program_pubkey)
        tx.message.account_keys.append(program_data_pubkey)
        tx.message.account_keys.append(program_buffer_pubkey)
        tx.message.account_keys.append(pxsol.core.ProgramSystem.pubkey)
        tx.message.account_keys.append(pxsol.core.ProgramLoaderUpgradeable.pubkey)
        tx.message.account_keys.append(pxsol.core.ProgramClock.pubKey)
        tx.message.account_keys.append(pxsol.core.ProgramRent.pubkey)
        tx.message.recent_blockhash = pxsol.base58.decode(pxsol.rpc.get_latest_blockhash({})['blockhash'])
        tx.message.instructions.append(pxsol.core.Instruction(4, [0, 1], pxsol.core.ProgramSystem.create(
            pxsol.rpc.get_minimum_balance_for_rent_exemption(pxsol.core.ProgramLoaderUpgradeable.size_program, {}),
            pxsol.core.ProgramLoaderUpgradeable.size_program,
            pxsol.core.ProgramLoaderUpgradeable.pubkey,
        )))
        tx.message.instructions.append(pxsol.core.Instruction(
            5, [0, 2, 1, 3, 7, 6, 4, 0],
            pxsol.core.ProgramLoaderUpgradeable.deploy_with_max_data_len(len(program) * 2),
        ))
        tx.signatures.append(self.prikey.sign(tx.message.serialize()))
        tx.signatures.append(program_prikey.sign(tx.message.serialize()))
        txid = pxsol.rpc.send_transaction(base64.b64encode(tx.serialize()).decode(), {})
        pxsol.rpc.wait([txid])
        return program_pubkey

    def program_update(self, program: bytearray, program_pubkey: pxsol.core.PubKey) -> None:
        # Updating an existing solana program by new program data and the same program id.
        program_buffer_pubkey = self.program_buffer_create(program)
        program_data_pubkey = pxsol.core.ProgramLoaderUpgradeable.pubkey.derive(program_pubkey.p)
        tx = pxsol.core.Transaction([], pxsol.core.Message(pxsol.core.MessageHeader(1, 0, 3), [], bytearray(), []))
        tx.message.account_keys.append(self.pubkey)
        tx.message.account_keys.append(program_data_pubkey)
        tx.message.account_keys.append(program_pubkey)
        tx.message.account_keys.append(program_buffer_pubkey)
        tx.message.account_keys.append(pxsol.core.ProgramLoaderUpgradeable.pubkey)
        tx.message.account_keys.append(pxsol.core.ProgramClock.pubKey)
        tx.message.account_keys.append(pxsol.core.ProgramRent.pubkey)
        tx.message.recent_blockhash = pxsol.base58.decode(pxsol.rpc.get_latest_blockhash({})['blockhash'])
        tx.message.instructions.append(pxsol.core.Instruction(
            4, [1, 2, 3, 0, 6, 5, 0],
            pxsol.core.ProgramLoaderUpgradeable.upgrade(),
        ))
        tx.signatures.append(self.prikey.sign(tx.message.serialize()))
        txid = pxsol.rpc.send_transaction(base64.b64encode(tx.serialize()).decode(), {})
        pxsol.rpc.wait([txid])

    def transfer(self, pubkey: pxsol.core.PubKey, value: int) -> bytearray:
        # Transfers the specified lamports to the target. The function returns the first signature of the transaction,
        # which is used to identify the transaction (transaction id).
        tx = pxsol.core.Transaction([], pxsol.core.Message(pxsol.core.MessageHeader(1, 0, 1), [], bytearray(), []))
        tx.message.account_keys.append(self.pubkey)
        tx.message.account_keys.append(pubkey)
        tx.message.account_keys.append(pxsol.core.ProgramSystem.pubkey)
        tx.message.recent_blockhash = pxsol.base58.decode(pxsol.rpc.get_latest_blockhash({})['blockhash'])
        tx.message.instructions.append(pxsol.core.Instruction(2, [0, 1], pxsol.core.ProgramSystem.transfer(value)))
        tx.signatures.append(self.prikey.sign(tx.message.serialize()))
        txid = pxsol.rpc.send_transaction(base64.b64encode(tx.serialize()).decode(), {})
        assert pxsol.base58.decode(txid) == tx.signatures[0]
        pxsol.rpc.wait([txid])
        return tx.signatures[0]

    def transfer_all(self, pubkey: pxsol.core.PubKey) -> bytearray:
        # Transfers all lamports to the target.
        # Solana's base fee is a fixed 5000 lamports (0.000005 SOL) per signature.
        return self.transfer(pubkey, self.balance() - 5000)
