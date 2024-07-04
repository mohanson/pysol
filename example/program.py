import argparse
import base64
import sol
import pathlib

# Publish a hello solana program, call it to show "Hello, Solana!". Then we update the program and call it again, and
# finally it will be explicit "Hello, Update!".

parser = argparse.ArgumentParser()
parser.add_argument('--action', type=str, choices=['call', 'deploy', 'update'])
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

user = sol.wallet.Wallet(sol.core.PriKey(bytearray(int(args.prikey, 0).to_bytes(32))))

if args.action == 'deploy':
    data = bytearray(pathlib.Path('res/hello_solana_program.so').read_bytes())
    pubkey = user.program_deploy(data)
    print('Program ID:', pubkey)

if args.action == 'call':
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

if args.action == 'update':
    data = bytearray(pathlib.Path('res/hello_update_program.so').read_bytes())
    pubkey = sol.core.PubKey.base58_decode(args.addr)
    user.program_update(data, pubkey)
    print('Program ID:', pubkey)
