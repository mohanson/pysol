import pathlib
import pxsol


def test_program():
    user = pxsol.wallet.Wallet(pxsol.core.PriKey.int_decode(1))
    pubkey = user.program_deploy(bytearray(pathlib.Path('res/hello_solana_program.so').read_bytes()))
    user.program_update(bytearray(pathlib.Path('res/hello_solana_program.so.2').read_bytes()), pubkey)
    pxsol.rpc.step()
    user.program_closed(pubkey)


def test_program_buffer():
    user = pxsol.wallet.Wallet(pxsol.core.PriKey.int_decode(1))
    pubkey = user.program_buffer_create(bytearray(pathlib.Path('res/hello_solana_program.so').read_bytes()))
    pxsol.rpc.step()
    user.program_buffer_closed(pubkey)


def test_transfer():
    user = pxsol.wallet.Wallet(pxsol.core.PriKey.int_decode(1))
    hole = pxsol.wallet.Wallet(pxsol.core.PriKey.int_decode(2))
    a = hole.balance()
    user.transfer(hole.pubkey, 1 * pxsol.denomination.sol)
    b = hole.balance()
    assert b == a + 1 * pxsol.denomination.sol


def test_transfer_all():
    user = pxsol.wallet.Wallet(pxsol.core.PriKey.int_decode(1))
    hole = pxsol.wallet.Wallet(pxsol.core.PriKey.int_decode(2))
    user.transfer(hole.pubkey, 1 * pxsol.denomination.sol)
    hole.transfer_all(user.pubkey)
    assert hole.balance() == 0
