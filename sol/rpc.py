import itertools
import random
import requests
import sol.config
import time
import typing

# Doc: https://solana.com/docs/rpc/http


def call(method: str, params: typing.List) -> typing.Any:
    r = requests.post(sol.config.current.url, json={
        'id': random.randint(0x00000000, 0xffffffff),
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
    }).json()
    if 'error' in r:
        raise Exception(r['error'])
    return r['result']


def hang(signature: typing.List[str]) -> None:
    a = signature.copy()
    for _ in itertools.repeat(0):
        time.sleep(1)
        r = get_signature_statuses(a)
        s = [e['confirmationStatus'] != 'finalized' for e in r]
        a = list(itertools.compress(a, s))
        if len(a) == 0:
            break


def wait(signature: str) -> None:
    return hang([signature])


def get_account_info(pubkey: str, conf: typing.Dict | None = None) -> typing.Dict:
    return call('getAccountInfo', [pubkey, conf])['value']


def get_balance(pubkey: str, conf: typing.Dict | None = None) -> int:
    return call('getBalance', [pubkey, conf])['value']


def get_block(slot_number: int, conf: typing.Dict | None = None) -> typing.Dict:
    return call('getBlock', [slot_number, conf])


def get_block_commitment(block_number: int) -> typing.Dict:
    return call('getBlockCommitment', [block_number])


def get_block_height(conf: typing.Dict | None = None) -> int:
    return call('getBlockHeight', [conf])


def get_block_production(conf: typing.Dict | None = None) -> typing.Dict:
    return call('getBlockProduction', [conf])


def get_block_time(block_number: int) -> int:
    return call('getBlockTime', [block_number])


def get_blocks(start_slot: int, end_slot: int | None = None, conf: typing.Dict | None = None) -> typing.List[int]:
    return call('getBlocks', [start_slot, end_slot, conf])


def get_blocks_with_limit(start_slot: int, limit: int, conf: typing.Dict | None = None) -> typing.List[int]:
    return call('getBlocksWithLimit', [start_slot, limit, conf])


def get_cluster_nodes() -> typing.List[typing.Dict]:
    return call('getClusterNodes', [])


def get_epoch_info(conf: typing.Dict | None = None) -> typing.Dict:
    return call('getEpochInfo', [conf])


def get_epoch_schedule() -> typing.Dict:
    return call('getEpochSchedule', [])


def get_fee_for_message(message: str, conf: typing.Dict | None = None) -> int:
    # Param message is base-64 encoded.
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


def get_inflation_governor(conf: typing.Dict | None = None) -> typing.Dict:
    return call('getInflationGovernor', [conf])


def get_inflation_rate() -> typing.Dict:
    return call('getInflationRate', [])


def get_inflation_reward(addr_list: typing.List[str], conf: typing.Dict | None = None) -> typing.Dict:
    return call('getInflationReward', [addr_list, conf])


def get_largest_accounts(conf: typing.Dict | None = None) -> typing.List[typing.Dict]:
    return call('getLargestAccounts', [conf])


def get_latest_blockhash(conf: typing.Dict | None = None) -> typing.Dict:
    return call('getLatestBlockhash', [conf])['value']


def get_leader_schedule(epoch: int | None = None, conf: typing.Dict | None = None) -> typing.Dict:
    return call('getLeaderSchedule', [epoch, conf])


def get_max_retransmit_slot() -> int:
    return call('getMaxRetransmitSlot', [])


def get_max_shred_insert_slot() -> int:
    return call('getMaxShredInsertSlot', [])


def get_minimum_balance_for_rent_exemption(data_size: int, conf: typing.Dict | None = None) -> int:
    return call('getMinimumBalanceForRentExemption', [data_size, conf])


def get_multiple_accounts(pubkey_list: typing.List[str], conf: typing.Dict | None = None) -> typing.List[typing.Dict]:
    return call('getMultipleAccounts', [pubkey_list, conf])


def get_program_accounts(pubkey: str, conf: typing.Dict | None = None) -> typing.List[typing.Dict]:
    return call('getProgramAccounts', [pubkey, conf])


def get_recent_performance_samples(limit: int | None = None) -> typing.List[typing.Dict]:
    return call('getRecentPerformanceSamples', [limit])


def get_recent_prioritization_fees(pubkey_list: typing.List[str] | None = None) -> typing.List[typing.Dict]:
    return call('getRecentPrioritizationFees', [pubkey_list])


def get_signature_statuses(sigs: typing.List[str], conf: typing.Dict | None = None) -> typing.Dict:
    return call('getSignatureStatuses', [sigs, conf])['value']


def get_signatures_for_address(pubkey: str, conf: typing.Dict | None = None) -> typing.List[typing.Dict]:
    return call('getSignaturesForAddress', [pubkey, conf])


def get_slot(conf: typing.Dict | None = None) -> int:
    return call('getSlot', [conf])


def get_slot_leader(conf: typing.Dict | None = None) -> str:
    return call('getSlotLeader', [conf])


def get_slot_leaders(start_slot: int, limit: int) -> typing.List[str]:
    return call('getSlotLeaders', [start_slot, limit])


def get_stake_activation(pubkey: str, conf: typing.Dict | None = None) -> typing.Dict:
    return call('getStakeActivation', [pubkey, conf])


def get_stake_minimum_delegation(conf: typing.Dict | None = None) -> typing.Dict:
    return call('getStakeMinimumDelegation', [conf])


def get_supply(conf: typing.Dict | None = None) -> typing.Dict:
    return call('getSupply', [conf])


def get_token_account_balance(pubkey: str, conf: typing.Dict | None = None) -> typing.Dict:
    return call('getTokenAccountBalance', [pubkey, conf])


def get_token_accounts_by_delegate(
    pubkey: str,
    token: typing.Dict | None = None,
    conf: typing.Dict | None = None,
) -> typing.Dict:
    return call('getTokenAccountsByDelegate', [pubkey, token, conf])


def get_token_accounts_by_owner(
    pubkey: str,
    token: typing.Dict | None = None,
    conf: typing.Dict | None = None,
) -> typing.Dict:
    return call('getTokenAccountsByOwner', [pubkey, token, conf])


def get_token_largest_accounts(pubkey: str, conf: typing.Dict | None = None) -> typing.Dict:
    return call('getTokenLargestAccounts', [pubkey, conf])


def get_token_supply(pubkey: str, conf: typing.Dict | None = None) -> typing.Dict:
    return call('getTokenSupply', [pubkey, conf])


def get_transaction(signature: str, conf: typing.Dict | None = None) -> typing.Dict:
    return call('getTransaction', [signature, conf])


def get_transaction_count(conf: typing.Dict | None = None) -> int:
    return call('getTransactionCount', [conf])


def get_version() -> typing.Dict:
    return call('getVersion', [])


def get_vote_accounts(conf: typing.Dict | None = None) -> typing.Dict:
    return call('getVoteAccounts', [conf])


def is_blockhash_valid(blockhash: str, conf: typing.Dict | None = None) -> bool:
    return call('isBlockhashValid', [blockhash, conf])


def minimum_ledger_slot() -> int:
    return call('minimumLedgerSlot', [])


def request_airdrop(pubkey: str, value: int, conf: typing.Dict | None = None) -> str:
    return call('requestAirdrop', [pubkey, value, conf])


def send_transaction(tx: str, conf: typing.Dict | None = None) -> str:
    return call('sendTransaction', [tx, conf])


def simulate_transaction(tx: str, conf: typing.Dict | None = None) -> typing.Dict:
    return call('simulateTransaction', [tx, conf])
