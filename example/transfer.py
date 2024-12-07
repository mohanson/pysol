import argparse
import pxsol

# Transfer sol to other.

parser = argparse.ArgumentParser()
parser.add_argument('--net', type=str, choices=['develop', 'mainnet', 'testnet'], default='develop')
parser.add_argument('--prikey', type=str, help='private key')
parser.add_argument('--to', type=str, help='to address')
parser.add_argument('--value', type=float, help='sol value')
args = parser.parse_args()

if args.net == 'develop':
    pxsol.config.current = pxsol.config.develop
if args.net == 'mainnet':
    pxsol.config.current = pxsol.config.mainnet
if args.net == 'testnet':
    pxsol.config.current = pxsol.config.testnet

user = pxsol.wallet.Wallet(pxsol.core.PriKey(bytearray(int(args.prikey, 0).to_bytes(32))))
hole = pxsol.core.PubKey.base58_decode(args.to)
hash = user.transfer(hole, 0.05 * pxsol.denomination.sol)
pxsol.rpc.wait(pxsol.base58.encode(hash))
print(pxsol.base58.encode(hash))
