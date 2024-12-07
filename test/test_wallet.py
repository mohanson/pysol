import pathlib
import pxsol


def test_program_deploy_update():
    user = pxsol.wallet.Wallet(pxsol.core.PriKey(bytearray(int(1).to_bytes(32))))
    pubkey = user.program_deploy(bytearray(pathlib.Path('res/hello_solana_program.so').read_bytes()))
    user.program_update(bytearray(pathlib.Path('res/hello_update_program.so').read_bytes()), pubkey)


def test_transfer():
    user = pxsol.wallet.Wallet(pxsol.core.PriKey(bytearray(int(1).to_bytes(32))))
    hole = pxsol.wallet.Wallet(pxsol.core.PriKey(bytearray(int(2).to_bytes(32))))
    a = hole.balance()
    hash = user.transfer(hole.pubkey, 1 * pxsol.denomination.sol)
    pxsol.rpc.wait(pxsol.base58.encode(hash))
    b = hole.balance()
    assert b == a + 1 * pxsol.denomination.sol


def test_transfer_all():
    user = pxsol.wallet.Wallet(pxsol.core.PriKey(bytearray(int(1).to_bytes(32))))
    hole = pxsol.wallet.Wallet(pxsol.core.PriKey(bytearray(int(2).to_bytes(32))))
    hash = user.transfer(hole.pubkey, 1 * pxsol.denomination.sol)
    pxsol.rpc.wait(pxsol.base58.encode(hash))
    hash = hole.transfer_all(user.pubkey)
    pxsol.rpc.wait(pxsol.base58.encode(hash))
    assert hole.balance() == 0
