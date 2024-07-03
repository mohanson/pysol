import argparse
import base64
import sol
import pathlib

# Publish a hello solana program, then call it to show "Hello, Solana!".

parser = argparse.ArgumentParser()
parser.add_argument('--action', type=str, choices=['deploy', 'call'])
parser.add_argument('--addr', type=str, help='addr')
parser.add_argument('--net', type=str, choices=['develop', 'mainnet', 'testnet'], default='develop')
parser.add_argument('--prikey', type=str, help='private key')
args = parser.parse_args()

if args.net == 'develop':
    sol.config.current = sol.config.develop
if args.net == 'mainnet':
    sol.config.current = sol.config.mainnet
if args.net == 'testnet':
    sol.config.current = sol.config.testnet


if args.action == 'deploy':
    user = sol.wallet.Wallet(sol.core.PriKey(bytearray(int(args.prikey, 0).to_bytes(32))))
    data = bytearray(pathlib.Path('res/hello_solana_program.so').read_bytes())
    pubkey = user.program_deploy(data)
    print('Program ID:', pubkey)

if args.action == 'call':
    user = sol.wallet.Wallet(sol.core.PriKey(bytearray(int(args.prikey, 0).to_bytes(32))))
    tx = sol.core.Transaction([], sol.core.Message(sol.core.MessageHeader(1, 0, 1), [], bytearray(), []))
    tx.message.account_keys.append(user.pubkey)
    tx.message.account_keys.append(sol.core.PubKey.base58_decode(args.addr))
    tx.message.recent_blockhash = sol.base58.decode(sol.rpc.get_latest_blockhash()['blockhash'])
    tx.message.instructions.append(sol.core.Instruction(1, [], bytearray()))
    tx.signatures.append(user.prikey.sign(tx.message.serialize()))
    hash = sol.rpc.send_transaction(base64.b64encode(tx.serialize()).decode(), {
        'encoding': 'base64'
    })
    sol.rpc.wait(hash)
    r = sol.rpc.get_transaction(hash)
    for e in r['meta']['logMessages']:
        print(e)