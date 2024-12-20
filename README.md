# Pxsol: Solana Library For Humans

> Pysol has been renamed to Pxsol, as the name is already taken on pypi.

Pxsol is a project that aims to provide human-friendly interfaces for common solana operations. Using pxsol, you can easily and happily complete everything you want to do on sol.

Features:

- No third-party dependencies, everything is visible.
- Incredibly simple, even a cat knows how to use it.

## Installation

```sh
$ pip install pxsol
# or
$ git clone https://github.com/mohanson/pxsol
$ cd pxsol
$ python -m pip install --editable .
```

## Usage

By default, pxsol is configured on the develop. To switch the network to the main network, use the following code:

```py
import pxsol
pxsol.config.current = pxsol.config.mainnet
```

**example/addr.py**

Calculate the address from a private key.

Solana's private key is a 32-byte array, selected arbitrarily. In general, the private key is not used in isolation instead, it forms a 64-byte keypair together with the public key, which is also a 32-byte array. Most solana wallets, such as phantom, import and export private keys in base58-encoded keypair format.

In this example, we use u256 to represent a 32-byte private key.

```sh
$ python example/addr.py --prikey 0x1

# 6ASf5EcmmEHTgDJ4X4ZT5vT6iHVJBXPg5AN5YoTCpGWt
```

**example/balance.py**

Get the balance by an address.

```sh
$ python example/balance.py --net develop --addr 6ASf5EcmmEHTgDJ4X4ZT5vT6iHVJBXPg5AN5YoTCpGWt

# 10000

$ python example/balance.py --net mainnet --addr 6ASf5EcmmEHTgDJ4X4ZT5vT6iHVJBXPg5AN5YoTCpGWt

# 0.002030181
```

**example/program.py**

Deploy a hello solana program, call it to show "Hello, Solana!". Then we update the program and call it again, it will display another welcome message. Finally, we close the program to withdraw all solanas.

```sh
$ python example/program.py --prikey 0x1 --action deploy
# Program 6B7KVuUQ42x8SagFuFaoiV9jWTSic3Qd771kNrmGwoBG create

$ python example/program.py --prikey 0x1 --action call --addr 6B7KVuUQ42x8SagFuFaoiV9jWTSic3Qd771kNrmGwoBG
# Program 6B7KVuUQ42x8SagFuFaoiV9jWTSic3Qd771kNrmGwoBG invoke [1]
# Program log: Hello, Solana!
# Program log: Our program's Program ID: 6B7KVuUQ42x8SagFuFaoiV9jWTSic3Qd771kNrmGwoBG
# Program 6B7KVuUQ42x8SagFuFaoiV9jWTSic3Qd771kNrmGwoBG consumed 11850 of 200000 compute units
# Program 6B7KVuUQ42x8SagFuFaoiV9jWTSic3Qd771kNrmGwoBG success

$ python example/program.py --prikey 0x1 --action update --addr 6B7KVuUQ42x8SagFuFaoiV9jWTSic3Qd771kNrmGwoBG
# Program 6B7KVuUQ42x8SagFuFaoiV9jWTSic3Qd771kNrmGwoBG update

$ python example/program.py --prikey 0x1 --action call --addr 6B7KVuUQ42x8SagFuFaoiV9jWTSic3Qd771kNrmGwoBG
# Program 6B7KVuUQ42x8SagFuFaoiV9jWTSic3Qd771kNrmGwoBG invoke [1]
# Program log: Hello, Update!
# Program log: Our program's Program ID: 6B7KVuUQ42x8SagFuFaoiV9jWTSic3Qd771kNrmGwoBG
# Program 6B7KVuUQ42x8SagFuFaoiV9jWTSic3Qd771kNrmGwoBG consumed 11850 of 200000 compute units
# Program 6B7KVuUQ42x8SagFuFaoiV9jWTSic3Qd771kNrmGwoBG success

$ python example/program.py --prikey 0x1 --action closed --addr 6B7KVuUQ42x8SagFuFaoiV9jWTSic3Qd771kNrmGwoBG
# Program 6B7KVuUQ42x8SagFuFaoiV9jWTSic3Qd771kNrmGwoBG closed
```

**example/transfer.py**

Transfer sol to other.

```sh
$ python example/transfer.py --prikey 0x1 --to 8pM1DN3RiT8vbom5u1sNryaNT1nyL8CTTW3b5PwWXRBH --value 0.05

# 4GhcAygac8krnrJgF2tCSNxRyWsquCZ26NPM6o9oP3bPQFkAzi22CGn9RszBXzqPErujVxwzenTHoTMHuiZm98Wu
```

**example/wif.py**

Calculate the wallet import format from the private key. This is useful when you are trying to import an account in phantom wallet.

```sh
$ python example/wif.py --prikey 0x1

# 1111111111111111111111111111111PPm2a2NNZH2EFJ5UkEjkH9Fcxn8cvjTmZDKQQisyLDmA
```

## Test

```sh
$ wget https://github.com/anza-xyz/agave/releases/download/v2.0.20/solana-release-x86_64-unknown-linux-gnu.tar.bz2
$ tar -xvf solana-release-x86_64-unknown-linux-gnu.tar.bz2
$ cd solana-release

# Run test validator
$ solana-test-validator -l /tmp/solana-ledger
$ solana config set --url localhost
$ solana airdrop 99 6ASf5EcmmEHTgDJ4X4ZT5vT6iHVJBXPg5AN5YoTCpGWt

$ pytest -v
```

## License

MIT
