# Python SDK for SOL

Python SOL is an experimental project that aims to provide human-friendly interfaces for common SOL operations. Note that Python SOL is not a complete SDK, but only implements the SOL functions that I am interested in.

Features:

- No third-party dependencies. All code is visible.
- Incredibly simple.

## Installation

```sh
$ git clone https://github.com/mohanson/pysol
$ cd pysol
$ python -m pip install --editable . --config-settings editable_mode=strict
```

## Usage

**example/addr.py**

Calculate the address from a private key. Solana's private key is a 32-byte array, which can be represented as a u256 integer.

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

**example/transfer.py**

Transfer sol to other.

```sh
$ python example/transfer.py --prikey 0x1 --to 8pM1DN3RiT8vbom5u1sNryaNT1nyL8CTTW3b5PwWXRBH --value 0.05

# 4GhcAygac8krnrJgF2tCSNxRyWsquCZ26NPM6o9oP3bPQFkAzi22CGn9RszBXzqPErujVxwzenTHoTMHuiZm98Wu
```

## Test

```sh
$ wget https://github.com/solana-labs/solana/releases/download/v1.18.15/solana-release-x86_64-unknown-linux-gnu.tar.bz2
$ tar -jxvf solana-release-x86_64-unknown-linux-gnu.tar.bz2
$ cd solana-release-x86_64-unknown-linux-gnu.tar.bz2

# Run test validator
$ solana-test-validator -l /tmp/test-ledger
$ solana config set --url localhost
$ solana airdrop 99 6ASf5EcmmEHTgDJ4X4ZT5vT6iHVJBXPg5AN5YoTCpGWt

$ pytest -v
```

## License

MIT
