import base64
import json
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

    def transfer(self, pubkey: sol.core.PubKey, value: int) -> bytearray:
        tx = sol.core.Transaction([], sol.core.Message(sol.core.MessageHeader(1, 0, 1), [], bytearray(), []))
        tx.message.account_keys.append(self.pubkey)
        tx.message.account_keys.append(pubkey)
        tx.message.account_keys.append(sol.core.SystemProgram.pubkey)
        tx.message.recent_blockhash = sol.base58.decode(sol.rpc.get_latest_blockhash()['blockhash'])
        tx.message.instructions.append(sol.core.Instruction(2, [0, 1], sol.core.SystemProgram.transfer(value)))
        tx.signatures.append(sol.eddsa.sign(self.prikey.p, tx.message.serialize()))
        hash = sol.rpc.send_transaction(base64.b64encode(tx.serialize()).decode(), {
            'encoding': 'base64'
        })
        return sol.base58.decode(hash)

    def transfer_all(self, pubkey: sol.core.PubKey) -> bytearray:
        return self.transfer(pubkey, self.balance() - sol.config.current.base_fee)
