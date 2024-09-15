import argparse
import sol

# Get the balance by an address.

parser = argparse.ArgumentParser()
parser.add_argument('--addr', type=str, help='address')
parser.add_argument('--net', type=str, choices=['develop', 'mainnet', 'testnet'], default='develop')
args = parser.parse_args()

if args.net == 'develop':
    sol.config.current = sol.config.develop
if args.net == 'mainnet':
    sol.config.current = sol.config.mainnet
if args.net == 'testnet':
    sol.config.current = sol.config.testnet

balance = sol.rpc.get_balance(args.addr)
print(balance / sol.denomination.sol)
