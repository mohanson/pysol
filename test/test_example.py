import subprocess


def call(c: str):
    return subprocess.run(c, check=True, shell=True)


def test_addr():
    call('python example/addr.py --prikey 0x1')


def test_balance():
    call('python example/balance.py --net develop --addr 6ASf5EcmmEHTgDJ4X4ZT5vT6iHVJBXPg5AN5YoTCpGWt')


def test_program():
    call('python example/program.py --action deploy --prikey 0x1')


def test_transfer():
    call('python example/transfer.py --prikey 0x1 --to 8pM1DN3RiT8vbom5u1sNryaNT1nyL8CTTW3b5PwWXRBH --value 0.05')


def test_wif():
    call('python example/wif.py --prikey 0x1')
