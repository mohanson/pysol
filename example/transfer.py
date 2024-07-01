import argparse
import base64
import sol

# Transfer ether to other.


parser = argparse.ArgumentParser()
parser.add_argument('--net', type=str, choices=['develop', 'mainnet', 'testnet'], default='develop')
parser.add_argument('--prikey', type=str, help='private key')
parser.add_argument('--to', type=str, required=True, help='to address')
parser.add_argument('--value', type=float, help='sol value')
args = parser.parse_args()

if args.net == 'develop':
    sol.config.current = sol.config.develop
if args.net == 'mainnet':
    sol.config.current = sol.config.mainnet
if args.net == 'testnet':
    sol.config.current = sol.config.testnet

user_prikey = sol.core.PriKey(bytearray(int(args.prikey, 0).to_bytes(32)))
user_pubkey = user_prikey.pubkey()
hole_pubkey = sol.core.PubKey.base58_decode(args.to)

tx = sol.core.Transaction([], sol.core.Message(sol.core.MessageHeader(1, 0, 1), [], bytearray(), []))
tx.message.account_keys.append(user_pubkey)
tx.message.account_keys.append(hole_pubkey)
tx.message.account_keys.append(sol.core.PubKey(bytearray(32)))
tx.message.recent_blockhash = sol.base58.decode(sol.rpc.get_latest_blockhash()['blockhash'])
instruction_data = bytearray()
instruction_data.extend(bytearray(int(2).to_bytes(4, 'little')))
instruction_data.extend(bytearray(int(args.value * sol.denomination.sol).to_bytes(8, 'little')))
tx.message.instructions.append(sol.core.Instruction(2, [0, 1], instruction_data))
tx.signatures.append(sol.eddsa.sign(user_prikey.p, tx.message.ser_encode()))

hash = sol.rpc.send_transaction(base64.b64encode(tx.ser_encode()).decode(), {
    'encoding': 'base64'
})
print(hash)
