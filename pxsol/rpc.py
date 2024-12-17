import base64
import itertools
import pxsol.config
import random
import requests
import time
import typing

# Doc: https://solana.com/docs/rpc/http


def call(method: str, params: typing.List) -> typing.Any:
    # Send a json rpc request.
    r = requests.post(pxsol.config.current.url, json={
        'id': random.randint(0x00000000, 0xffffffff),
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
    }).json()
    if 'error' in r:
        raise Exception(r['error'])
    return r['result']


def wait(sigs: typing.List[str]) -> None:
    # Wait for all signatures in the parameter to be confirmed. There is no limit on the number of signatures.
    remain = sigs.copy()
    for _ in itertools.repeat(0):
        pxsol.log.debugln(f'pxsol: transaction wait remain={len(remain)}')
        if len(remain) == 0:
            break
        time.sleep(0.5)
        oldest = remain[:256]
        newest = remain[256:]
        result = get_signature_statuses(oldest, {})
        match pxsol.config.current.commitment:
            case 'confirmed':
                select = [e is None or e['confirmationStatus'] not in ['confirmed', 'finalized'] for e in result]
            case 'finalized':
                select = [e is None or e['confirmationStatus'] not in ['finalized'] for e in result]
            case _:
                select = [e is None or e['confirmationStatus'] not in ['finalized'] for e in result]
        remain = list(itertools.compress(oldest, select)) + newest


def step() -> None:
    # Waiting for at least one new block.
    data = get_block_height({})
    for _ in itertools.repeat(0):
        time.sleep(0.5)
        if get_block_height({}) != data:
            break


def get_account_info(pubkey: str, conf: typing.Dict) -> typing.Dict:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getAccountInfo', [pubkey, conf])['value']


def get_balance(pubkey: str, conf: typing.Dict) -> int:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getBalance', [pubkey, conf])['value']


def get_block(slot_number: int, conf: typing.Dict) -> typing.Dict:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getBlock', [slot_number, conf])


def get_block_commitment(block_number: int) -> typing.Dict:
    return call('getBlockCommitment', [block_number])


def get_block_height(conf: typing.Dict) -> int:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getBlockHeight', [conf])


def get_block_production(conf: typing.Dict) -> typing.Dict:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getBlockProduction', [conf])


def get_block_time(block_number: int) -> int:
    return call('getBlockTime', [block_number])


def get_blocks(start_slot: int, end_slot: int, conf: typing.Dict) -> typing.List[int]:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getBlocks', [start_slot, end_slot, conf])


def get_blocks_with_limit(start_slot: int, limit: int, conf: typing.Dict) -> typing.List[int]:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getBlocksWithLimit', [start_slot, limit, conf])


def get_cluster_nodes() -> typing.List[typing.Dict]:
    return call('getClusterNodes', [])


def get_epoch_info(conf: typing.Dict) -> typing.Dict:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getEpochInfo', [conf])


def get_epoch_schedule() -> typing.Dict:
    return call('getEpochSchedule', [])


def get_fee_for_message(message: str, conf: typing.Dict) -> int:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getFeeForMessage', [message, conf])


def get_first_available_block() -> int:
    return call('getFirstAvailableBlock', [])


def get_genesis_hash() -> str:
    return call('getGenesisHash', [])


def get_health() -> typing.Dict | str:
    return call('getHealth', [])


def get_highest_snapshot_slot() -> typing.Dict:
    return call('getHighestSnapshotSlot', [])


def get_identity() -> typing.Dict:
    return call('getIdentity', [])


def get_inflation_governor(conf: typing.Dict) -> typing.Dict:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getInflationGovernor', [conf])


def get_inflation_rate() -> typing.Dict:
    return call('getInflationRate', [])


def get_inflation_reward(addr_list: typing.List[str], conf: typing.Dict) -> typing.Dict:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getInflationReward', [addr_list, conf])


def get_largest_accounts(conf: typing.Dict) -> typing.List[typing.Dict]:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getLargestAccounts', [conf])


def get_latest_blockhash(conf: typing.Dict) -> typing.Dict:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getLatestBlockhash', [conf])['value']


def get_leader_schedule(epoch: int, conf: typing.Dict) -> typing.Dict:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getLeaderSchedule', [epoch, conf])


def get_max_retransmit_slot() -> int:
    return call('getMaxRetransmitSlot', [])


def get_max_shred_insert_slot() -> int:
    return call('getMaxShredInsertSlot', [])


def get_minimum_balance_for_rent_exemption(data_size: int, conf: typing.Dict) -> int:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getMinimumBalanceForRentExemption', [data_size, conf])


def get_multiple_accounts(pubkey_list: typing.List[str], conf: typing.Dict) -> typing.List[typing.Dict]:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getMultipleAccounts', [pubkey_list, conf])


def get_program_accounts(pubkey: str, conf: typing.Dict) -> typing.List[typing.Dict]:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getProgramAccounts', [pubkey, conf])


def get_recent_performance_samples(limit: int) -> typing.List[typing.Dict]:
    return call('getRecentPerformanceSamples', [limit])


def get_recent_prioritization_fees(pubkey_list: typing.List[str]) -> typing.List[typing.Dict]:
    return call('getRecentPrioritizationFees', [pubkey_list])


def get_signature_statuses(sigs: typing.List[str], conf: typing.Dict) -> typing.Dict:
    conf.setdefault('searchTransactionHistory', True)
    return call('getSignatureStatuses', [sigs, conf])['value']


def get_signatures_for_address(pubkey: str, conf: typing.Dict) -> typing.List[typing.Dict]:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getSignaturesForAddress', [pubkey, conf])


def get_slot(conf: typing.Dict) -> int:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getSlot', [conf])


def get_slot_leader(conf: typing.Dict) -> str:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getSlotLeader', [conf])


def get_slot_leaders(start_slot: int, limit: int) -> typing.List[str]:
    return call('getSlotLeaders', [start_slot, limit])


def get_stake_minimum_delegation(conf: typing.Dict) -> typing.Dict:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getStakeMinimumDelegation', [conf])


def get_supply(conf: typing.Dict) -> typing.Dict:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getSupply', [conf])


def get_token_account_balance(pubkey: str, conf: typing.Dict) -> typing.Dict:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getTokenAccountBalance', [pubkey, conf])


def get_token_accounts_by_delegate(pubkey: str, by: typing.Dict, conf: typing.Dict) -> typing.Dict:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getTokenAccountsByDelegate', [pubkey, by, conf])


def get_token_accounts_by_owner(pubkey: str, by: typing.Dict, conf: typing.Dict) -> typing.Dict:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getTokenAccountsByOwner', [pubkey, by, conf])


def get_token_largest_accounts(pubkey: str, conf: typing.Dict) -> typing.Dict:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getTokenLargestAccounts', [pubkey, conf])


def get_token_supply(pubkey: str, conf: typing.Dict) -> typing.Dict:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getTokenSupply', [pubkey, conf])


def get_transaction(signature: str, conf: typing.Dict) -> typing.Dict:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getTransaction', [signature, conf])


def get_transaction_count(conf: typing.Dict) -> int:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getTransactionCount', [conf])


def get_version() -> typing.Dict:
    return call('getVersion', [])


def get_vote_accounts(conf: typing.Dict) -> typing.Dict:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('getVoteAccounts', [conf])


def is_blockhash_valid(blockhash: str, conf: typing.Dict) -> bool:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('isBlockhashValid', [blockhash, conf])


def minimum_ledger_slot() -> int:
    return call('minimumLedgerSlot', [])


def request_airdrop(pubkey: str, value: int, conf: typing.Dict) -> str:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    return call('requestAirdrop', [pubkey, value, conf])


def send_transaction(tx: str, conf: typing.Dict) -> str:
    conf.setdefault('encoding', 'base64')
    conf.setdefault('preflightCommitment', pxsol.config.current.commitment)
    txid = pxsol.core.Transaction.serialize_decode(base64.b64decode(tx)).signatures[0]
    txid = pxsol.base58.encode(txid)
    pxsol.log.debugln(f'pxsol: transaction send signature={txid}')
    return call('sendTransaction', [tx, conf])


def simulate_transaction(tx: str, conf: typing.Dict) -> typing.Dict:
    conf.setdefault('commitment', pxsol.config.current.commitment)
    conf.setdefault('encoding', 'base64')
    return call('simulateTransaction', [tx, conf])
