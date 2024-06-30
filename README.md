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

## Test

```sh
$ wget https://github.com/solana-labs/solana/releases/download/v1.18.15/solana-release-x86_64-unknown-linux-gnu.tar.bz2
$ tar -jxvf solana-release-x86_64-unknown-linux-gnu.tar.bz2
$ cd solana-release-x86_64-unknown-linux-gnu.tar.bz2

$ solana config set --url localhost
# Create default wallet
$ solana-keygen new
# Run test validator
$ solana-test-validator -l /tmp/test-ledger
```

## License

MIT
