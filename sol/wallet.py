import base64
import json
import random
import sol


class Wallet:
    def __init__(self, prikey: sol.core.PriKey):
        self.prikey = prikey
        self.pubkey = prikey.pubkey()

    def __repr__(self):
        return json.dumps(self.json())

    def json(self):
        return {
            'prikey': self.prikey.base58(),
            'pubkey': self.pubkey.base58(),
        }

    def balance(self):
        return sol.rpc.get_balance(self.pubkey.base58())

    def program_deploy(self, program: bytearray) -> sol.core.PubKey:
        program_buffer_prikey = sol.core.PriKey(bytearray(random.randbytes(32)))
        program_buffer_pubkey = program_buffer_prikey.pubkey()
        program_data = program
        program_data_size = sol.core.ProgramLoaderUpgradeable.size_program_data_metadata + len(program_data)

        # Initialize buffer
        tx = sol.core.Transaction([], sol.core.Message(sol.core.MessageHeader(2, 0, 2), [], bytearray(), []))
        tx.message.account_keys.append(self.pubkey)
        tx.message.account_keys.append(program_buffer_pubkey)
        tx.message.account_keys.append(sol.core.ProgramSystem.pubkey)
        tx.message.account_keys.append(sol.core.ProgramLoaderUpgradeable.pubkey)
        tx.message.recent_blockhash = sol.base58.decode(sol.rpc.get_latest_blockhash()['blockhash'])
        tx.message.instructions.append(sol.core.Instruction(2, [0, 1], sol.core.ProgramSystem.create(
            sol.rpc.get_minimum_balance_for_rent_exemption(program_data_size),
            len(program_data) + sol.core.ProgramLoaderUpgradeable.size_buffer_metadata,
            sol.core.ProgramLoaderUpgradeable.pubkey,
        )))
        tx.message.instructions.append(sol.core.Instruction(
            3, [1, 0], sol.core.ProgramLoaderUpgradeable.initialize_buffer()))
        tx.signatures.append(self.prikey.sign(tx.message.serialize()))
        tx.signatures.append(program_buffer_prikey.sign(tx.message.serialize()))
        hash = sol.rpc.send_transaction(base64.b64encode(tx.serialize()).decode(), {
            'encoding': 'base64'
        })
        sol.rpc.wait(hash)

        # Write
        size = 1012
        hall = []
        for i in range(0, len(program_data), size):
            elem = program_data[i:i+size]
            tx = sol.core.Transaction([], sol.core.Message(sol.core.MessageHeader(1, 0, 1), [], bytearray(), []))
            tx.message.account_keys.append(self.pubkey)
            tx.message.account_keys.append(program_buffer_pubkey)
            tx.message.account_keys.append(sol.core.ProgramLoaderUpgradeable.pubkey)
            tx.message.recent_blockhash = sol.base58.decode(sol.rpc.get_latest_blockhash()['blockhash'])
            tx.message.instructions.append(sol.core.Instruction(
                2, [1, 0], sol.core.ProgramLoaderUpgradeable.write(i, elem)))
            tx.signatures.append(self.prikey.sign(tx.message.serialize()))
            assert len(tx.serialize()) <= 1232
            hash = sol.rpc.send_transaction(base64.b64encode(tx.serialize()).decode(), {
                'encoding': 'base64'
            })
            hall.append(hash)
        sol.rpc.hang(hall)

        program_prikey = sol.core.PriKey(bytearray(random.randbytes(32)))
        program_pubkey = program_prikey.pubkey()
        program_data_pubkey = sol.core.pda(sol.core.ProgramLoaderUpgradeable.pubkey, program_pubkey.p)

        # Deploy with max data len
        tx = sol.core.Transaction([], sol.core.Message(sol.core.MessageHeader(2, 0, 4), [], bytearray(), []))
        tx.message.account_keys.append(self.pubkey)
        tx.message.account_keys.append(program_pubkey)
        tx.message.account_keys.append(program_data_pubkey)
        tx.message.account_keys.append(program_buffer_pubkey)
        tx.message.account_keys.append(sol.core.ProgramSystem.pubkey)
        tx.message.account_keys.append(sol.core.ProgramLoaderUpgradeable.pubkey)
        tx.message.account_keys.append(sol.core.ProgramRent.pubkey)
        tx.message.account_keys.append(sol.core.ProgramClock.pubKey)
        tx.message.recent_blockhash = sol.base58.decode(sol.rpc.get_latest_blockhash()['blockhash'])
        tx.message.instructions.append(sol.core.Instruction(4, [0, 1], sol.core.ProgramSystem.create(
            sol.rpc.get_minimum_balance_for_rent_exemption(sol.core.ProgramLoaderUpgradeable.size_program),
            sol.core.ProgramLoaderUpgradeable.size_program,
            sol.core.ProgramLoaderUpgradeable.pubkey,
        )))
        tx.message.instructions.append(sol.core.Instruction(
            5, [0, 2, 1, 3, 6, 7, 4, 0],
            sol.core.ProgramLoaderUpgradeable.deploy_with_max_data_len(len(program_data) * 2),
        ))
        tx.signatures.append(self.prikey.sign(tx.message.serialize()))
        tx.signatures.append(program_prikey.sign(tx.message.serialize()))
        hash = sol.rpc.send_transaction(base64.b64encode(tx.serialize()).decode(), {
            'encoding': 'base64'
        })
        sol.rpc.wait(hash)
        return program_pubkey

    def transfer(self, pubkey: sol.core.PubKey, value: int) -> bytearray:
        tx = sol.core.Transaction([], sol.core.Message(sol.core.MessageHeader(1, 0, 1), [], bytearray(), []))
        tx.message.account_keys.append(self.pubkey)
        tx.message.account_keys.append(pubkey)
        tx.message.account_keys.append(sol.core.ProgramSystem.pubkey)
        tx.message.recent_blockhash = sol.base58.decode(sol.rpc.get_latest_blockhash()['blockhash'])
        tx.message.instructions.append(sol.core.Instruction(2, [0, 1], sol.core.ProgramSystem.transfer(value)))
        tx.signatures.append(self.prikey.sign(tx.message.serialize()))
        hash = sol.rpc.send_transaction(base64.b64encode(tx.serialize()).decode(), {
            'encoding': 'base64'
        })
        return sol.base58.decode(hash)

    def transfer_all(self, pubkey: sol.core.PubKey) -> bytearray:
        return self.transfer(pubkey, self.balance() - sol.config.current.base_fee)
