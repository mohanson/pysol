import argparse
import pxsol

# Calculate the wallet import format from the private key. This is useful when you are trying to import an account in
# phantom wallet.

parser = argparse.ArgumentParser()
parser.add_argument('--prikey', type=str, help='private key')
args = parser.parse_args()

prikey = pxsol.core.PriKey(bytearray(int(args.prikey, 0).to_bytes(32)))
wif = prikey.wif()
print(wif)
