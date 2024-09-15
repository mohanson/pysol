import argparse
import sol

# Transfer sol to other.

parser = argparse.ArgumentParser()
parser.add_argument('--net', type=str, choices=['develop', 'mainnet', 'testnet'], default='develop')
parser.add_argument('--prikey', type=str, help='private key')
parser.add_argument('--to', type=str, help='to address')
parser.add_argument('--value', type=float, help='sol value')
args = parser.parse_args()

if args.net == 'develop':
    sol.config.current = sol.config.develop
if args.net == 'mainnet':
    sol.config.current = sol.config.mainnet
if args.net == 'testnet':
    sol.config.current = sol.config.testnet

user = sol.wallet.Wallet(sol.core.PriKey(bytearray(int(args.prikey, 0).to_bytes(32))))
hole = sol.core.PubKey.base58_decode(args.to)
hash = user.transfer(hole, 0.05 * sol.denomination.sol)
sol.rpc.wait(sol.base58.encode(hash))
print(sol.base58.encode(hash))
