import argparse
import sol

# Calculate the address from a private key.

parser = argparse.ArgumentParser()
parser.add_argument('--prikey', type=str, help='private key')
args = parser.parse_args()

prikey = sol.core.PriKey(bytearray(int(args.prikey, 0).to_bytes(32)))
pubkey = prikey.pubkey()
addr = pubkey.base58()
print(addr)
