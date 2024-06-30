import subprocess


def call(c: str):
    return subprocess.run(c, check=True, shell=True)


def test_addr():
    call('python example/addr.py --prikey 0x1')
