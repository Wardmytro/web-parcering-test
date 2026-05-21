import requests
from solders.rpc.requests import GetSignaturesForAddress
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
import asyncio

SOLANA_RPC = "https://api.mainnet-beta.solana.com"
USDT_CONTRACT = "Es9vMFrzaCERmJfqV3E3wFsUjfxJosrv3NFxNYcXzLsUV5DJ"
DECIMALS = 6

async def check_solana_wallet_async(wallet_address, min_amount_usd, tolerance=0.01):
    """
    Check Solana wallet for USDT token transfers.
    Returns: List of transactions matching the amount
    """
    try:
        async_client = AsyncClient(SOLANA_RPC)
        wallet_pubkey = Pubkey.from_string(wallet_address)

        sigs_response = await async_client.get_signatures_for_address(wallet_pubkey, limit=50)
        signatures = sigs_response.value

        matches = []
        divisor = 10 ** DECIMALS

        for sig in signatures[:50]:
            try:
                tx_response = await async_client.get_transaction(sig.signature, max_supported_transaction_version=0)
                tx = tx_response.value

                if not tx:
                    continue

                for instruction in tx.transaction.message.instructions:
                    amount_raw = instruction.data.get('tokenAmount', {}).get('amount', 0)
                    if not amount_raw:
                        continue

                    amount = int(amount_raw) / divisor

                    if min_amount_usd - tolerance <= amount <= min_amount_usd + tolerance:
                        matches.append({
                            'tx_hash': str(sig.signature),
                            'amount': amount,
                            'timestamp': sig.block_time or 0,
                            'network': 'SOLANA'
                        })

            except Exception as e:
                continue

        await async_client.close()
        return matches

    except Exception as e:
        print(f"Solana async checker error: {e}")
        return []

def check_solana_wallet(wallet_address, min_amount_usd, tolerance=0.01):
    """
    Synchronous Solana wallet checker via RPC.
    """
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSignaturesForAddress",
            "params": [wallet_address, {"limit": 50}]
        }

        response = requests.post(SOLANA_RPC, json=payload, timeout=10)
        if response.status_code != 200:
            return []

        data = response.json()
        signatures = data.get('result', [])

        matches = []
        divisor = 10 ** DECIMALS

        for sig in signatures[:50]:
            try:
                tx_payload = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "getTransaction",
                    "params": [sig['signature'], {"encoding": "json", "maxSupportedTransactionVersion": 0}]
                }

                tx_response = requests.post(SOLANA_RPC, json=tx_payload, timeout=10)
                if tx_response.status_code != 200:
                    continue

                tx_data = tx_response.json()
                tx = tx_data.get('result', {})

                if not tx or 'transaction' not in tx:
                    continue

                tx_message = tx.get('transaction', {}).get('message', {})

                if 'instructions' in tx_message:
                    for instruction in tx_message['instructions']:
                        data = instruction.get('data', '')

                        parsed = instruction.get('parsed', {})
                        if 'tokenAmount' in parsed:
                            amount_raw = parsed['tokenAmount'].get('amount', '0')
                            amount = int(amount_raw) / divisor

                            if min_amount_usd - tolerance <= amount <= min_amount_usd + tolerance:
                                matches.append({
                                    'tx_hash': sig['signature'],
                                    'amount': amount,
                                    'timestamp': tx.get('blockTime', 0),
                                    'network': 'SOLANA'
                                })

            except Exception as e:
                continue

        return matches

    except Exception as e:
        print(f"Solana checker error: {e}")
        return []
