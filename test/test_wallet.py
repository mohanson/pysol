import pathlib
import sol


def test_program_deploy_update():
    user = sol.wallet.Wallet(sol.core.PriKey(bytearray(int(1).to_bytes(32))))
    pubkey = user.program_deploy(bytearray(pathlib.Path('res/hello_solana_program.so').read_bytes()))
    user.program_update(bytearray(pathlib.Path('res/hello_update_program.so').read_bytes()), pubkey)


def test_transfer():
    user = sol.wallet.Wallet(sol.core.PriKey(bytearray(int(1).to_bytes(32))))
    hole = sol.wallet.Wallet(sol.core.PriKey(bytearray(int(2).to_bytes(32))))
    a = hole.balance()
    hash = user.transfer(hole.pubkey, 1 * sol.denomination.sol)
    sol.rpc.wait(sol.base58.encode(hash))
    b = hole.balance()
    assert b == a + 1 * sol.denomination.sol


def test_transfer_all():
    user = sol.wallet.Wallet(sol.core.PriKey(bytearray(int(1).to_bytes(32))))
    hole = sol.wallet.Wallet(sol.core.PriKey(bytearray(int(2).to_bytes(32))))
    hash = user.transfer(hole.pubkey, 1 * sol.denomination.sol)
    sol.rpc.wait(sol.base58.encode(hash))
    hash = hole.transfer_all(user.pubkey)
    sol.rpc.wait(sol.base58.encode(hash))
    assert hole.balance() == 0
