import sol


def test_get_account_info():
    addr = sol.core.PriKey(bytearray(int(1).to_bytes(32))).pubkey().base58()
    sol.rpc.get_account_info(addr)


def test_get_balance():
    addr = sol.core.PriKey(bytearray(int(1).to_bytes(32))).pubkey().base58()
    sol.rpc.get_balance(addr)


def test_get_block():
    latest = sol.rpc.get_block_height()
    sol.rpc.get_block(latest)


def test_get_block_commitment():
    latest = sol.rpc.get_block_height()
    sol.rpc.get_block_commitment(latest)


def test_get_block_height():
    r = sol.rpc.get_block_height()
    assert r != 0


def test_get_block_production():
    sol.rpc.get_block_production()


def test_get_block_time():
    latest = sol.rpc.get_block_height()
    r = sol.rpc.get_block_time(latest)
    assert r != 0


def test_get_blocks():
    latest = sol.rpc.get_block_height()
    r = sol.rpc.get_blocks(latest)
    assert len(r) != 0


def test_get_blocks_with_limit():
    latest = sol.rpc.get_block_height()
    r = sol.rpc.get_blocks_with_limit(latest, 64)
    assert len(r) != 0


def test_get_cluster_nodes():
    r = sol.rpc.get_cluster_nodes()
    assert len(r) != 0


def test_get_epoch_info():
    sol.rpc.get_epoch_info()


def test_get_epoch_schedule():
    sol.rpc.get_epoch_schedule()


def test_get_fee_for_message():
    pass


def test_get_first_available_block():
    sol.rpc.get_first_available_block()


def test_get_genesis_hash():
    sol.rpc.get_genesis_hash()


def test_get_health():
    r = sol.rpc.get_health()
    assert r == 'ok'


def test_get_highest_snapshot_slot():
    sol.rpc.get_highest_snapshot_slot()


def test_get_identity():
    sol.rpc.get_identity()


def test_get_inflation_governor():
    sol.rpc.get_inflation_governor()


def test_get_inflation_rate():
    sol.rpc.get_inflation_rate()


def test_get_inflation_reward():
    pass


def test_get_largest_accounts():
    r = sol.rpc.get_largest_accounts()
    assert len(r) != 0


def test_get_latest_blockhash():
    sol.rpc.get_latest_blockhash()


def test_get_leader_schedule():
    pass


def test_get_max_retransmit_slot():
    sol.rpc.get_max_retransmit_slot()


def test_get_max_shred_insert_slot():
    sol.rpc.get_max_shred_insert_slot()


def test_get_minimum_balance_for_rent_exemption():
    sol.rpc.get_minimum_balance_for_rent_exemption(50)


def test_get_multiple_accounts():
    r = sol.rpc.get_multiple_accounts([
        sol.core.PriKey(bytearray(int(1).to_bytes(32))).pubkey().base58(),
        sol.core.PriKey(bytearray(int(2).to_bytes(32))).pubkey().base58(),
    ])
    assert len(r) == 2


def test_get_program_accounts():
    addr = sol.core.PriKey(bytearray(int(1).to_bytes(32))).pubkey().base58()
    sol.rpc.get_program_accounts(addr)


def test_get_recent_performance_samples():
    sol.rpc.get_recent_performance_samples()


def test_get_recent_prioritization_fees():
    sol.rpc.get_recent_prioritization_fees()


def test_get_signature_statuses():
    sol.rpc.get_signature_statuses([])


def test_get_signatures_for_address():
    addr = sol.core.PriKey(bytearray(int(1).to_bytes(32))).pubkey().base58()
    sol.rpc.get_signatures_for_address(addr)


def test_get_slot():
    sol.rpc.get_slot()


def test_get_slot_leader():
    sol.rpc.get_slot_leader()


def test_get_slot_leaders():
    latest = sol.rpc.get_block_height()
    r = sol.rpc.get_slot_leaders(latest, 1)
    assert len(r) == 1


def test_get_stake_activation():
    pass


def test_get_stake_minimum_delegation():
    sol.rpc.get_stake_minimum_delegation()


def test_get_supply():
    sol.rpc.get_supply()


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
    sol.rpc.get_transaction_count()


def test_get_version():
    sol.rpc.get_version()


def test_get_vote_accounts():
    sol.rpc.get_vote_accounts()


def test_is_blockhash_valid():
    sol.rpc.is_blockhash_valid('J7rBdM6AecPDEZp8aPq5iPSNKVkU5Q76F3oAV4eW5wsW')


def test_minimum_ledger_slot():
    sol.rpc.minimum_ledger_slot()


def test_request_airdrop():
    addr = sol.core.PriKey(bytearray(int(1).to_bytes(32))).pubkey().base58()
    sol.rpc.request_airdrop(addr, 1)


def test_send_transaction():
    pass


def test_simulate_transaction():
    pass
