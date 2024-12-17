import pxsol


def test_get_account_info():
    addr = pxsol.core.PriKey.int_decode(1).pubkey().base58()
    pxsol.rpc.get_account_info(addr, {})


def test_get_balance():
    addr = pxsol.core.PriKey.int_decode(1).pubkey().base58()
    pxsol.rpc.get_balance(addr, {})


def test_get_block():
    latest = pxsol.rpc.get_block_height({})
    pxsol.rpc.get_block(latest, {})


def test_get_block_commitment():
    latest = pxsol.rpc.get_block_height({})
    pxsol.rpc.get_block_commitment(latest)


def test_get_block_height():
    r = pxsol.rpc.get_block_height({})
    assert r != 0


def test_get_block_production():
    pxsol.rpc.get_block_production({})


def test_get_block_time():
    latest = pxsol.rpc.get_block_height({})
    r = pxsol.rpc.get_block_time(latest)
    assert r != 0


def test_get_blocks():
    latest = pxsol.rpc.get_block_height({})
    r = pxsol.rpc.get_blocks(latest - 7, latest, {})
    assert len(r) == 8


def test_get_blocks_with_limit():
    latest = pxsol.rpc.get_block_height({})
    r = pxsol.rpc.get_blocks_with_limit(latest - 8, 8, {})
    assert len(r) == 8


def test_get_cluster_nodes():
    r = pxsol.rpc.get_cluster_nodes()
    assert len(r) != 0


def test_get_epoch_info():
    pxsol.rpc.get_epoch_info({})


def test_get_epoch_schedule():
    pxsol.rpc.get_epoch_schedule()


def test_get_fee_for_message():
    pass


def test_get_first_available_block():
    pxsol.rpc.get_first_available_block()


def test_get_genesis_hash():
    pxsol.rpc.get_genesis_hash()


def test_get_health():
    r = pxsol.rpc.get_health()
    assert r == 'ok'


def test_get_highest_snapshot_slot():
    pxsol.rpc.get_highest_snapshot_slot()


def test_get_identity():
    pxsol.rpc.get_identity()


def test_get_inflation_governor():
    pxsol.rpc.get_inflation_governor({})


def test_get_inflation_rate():
    pxsol.rpc.get_inflation_rate()


def test_get_inflation_reward():
    pass


def test_get_largest_accounts():
    r = pxsol.rpc.get_largest_accounts({})
    assert len(r) != 0


def test_get_latest_blockhash():
    pxsol.rpc.get_latest_blockhash({})


def test_get_leader_schedule():
    pass


def test_get_max_retransmit_slot():
    pxsol.rpc.get_max_retransmit_slot()


def test_get_max_shred_insert_slot():
    pxsol.rpc.get_max_shred_insert_slot()


def test_get_minimum_balance_for_rent_exemption():
    pxsol.rpc.get_minimum_balance_for_rent_exemption(50, {})


def test_get_multiple_accounts():
    r = pxsol.rpc.get_multiple_accounts([
        pxsol.core.PriKey.int_decode(1).pubkey().base58(),
        pxsol.core.PriKey.int_decode(2).pubkey().base58(),
    ], {})
    assert len(r) == 2


def test_get_program_accounts():
    addr = pxsol.core.PriKey.int_decode(1).pubkey().base58()
    pxsol.rpc.get_program_accounts(addr, {})


def test_get_recent_performance_samples():
    pxsol.rpc.get_recent_performance_samples(1)


def test_get_recent_prioritization_fees():
    pxsol.rpc.get_recent_prioritization_fees([])


def test_get_signature_statuses():
    pxsol.rpc.get_signature_statuses([], {})


def test_get_signatures_for_address():
    addr = pxsol.core.PriKey.int_decode(1).pubkey().base58()
    pxsol.rpc.get_signatures_for_address(addr, {})


def test_get_slot():
    pxsol.rpc.get_slot({})


def test_get_slot_leader():
    pxsol.rpc.get_slot_leader({})


def test_get_slot_leaders():
    latest = pxsol.rpc.get_block_height({})
    r = pxsol.rpc.get_slot_leaders(latest, 1)
    assert len(r) == 1


def test_get_stake_activation():
    pass


def test_get_stake_minimum_delegation():
    pxsol.rpc.get_stake_minimum_delegation({})


def test_get_supply():
    pxsol.rpc.get_supply({})


def test_get_token_account_balance():
    pass


def test_get_token_accounts_by_delegate():
    pass


def test_get_token_accounts_by_owner():
    pass


def test_get_token_largest_accounts():
    pass


def test_get_token_supply():
    pass


def test_get_transaction():
    pass


def test_get_transaction_count():
    pxsol.rpc.get_transaction_count({})


def test_get_version():
    pxsol.rpc.get_version()


def test_get_vote_accounts():
    pxsol.rpc.get_vote_accounts({})


def test_is_blockhash_valid():
    pxsol.rpc.is_blockhash_valid('J7rBdM6AecPDEZp8aPq5iPSNKVkU5Q76F3oAV4eW5wsW', {})


def test_minimum_ledger_slot():
    pxsol.rpc.minimum_ledger_slot()


def test_request_airdrop():
    addr = pxsol.core.PriKey.int_decode(1).pubkey().base58()
    pxsol.rpc.request_airdrop(addr, 1, {})


def test_send_transaction():
    pass


def test_simulate_transaction():
    pass
