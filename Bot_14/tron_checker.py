from tronpy import Tron
from tronpy.async_tron import AsyncTron
from config import BLOCKCHAIN_CONFIG, WALLETS, TRON_API_KEY
import asyncio
from tronpy.providers import HTTPProvider, AsyncHTTPProvider

tron = Tron(provider=HTTPProvider(api_key=TRON_API_KEY))

TRON_CONFIG = BLOCKCHAIN_CONFIG["TRON"]
USDT_CONTRACT = TRON_CONFIG["usdt_contract"]
DECIMALS = TRON_CONFIG["decimals"]

async def check_tron_wallet(wallet_address, min_amount_usd, tolerance=0.01):
    """
    Check TRON wallet for USDT transfers matching the order amount.
    Returns: List of transactions matching the amount (within tolerance)
    """
    try:
        async_tron = AsyncTron(provider=AsyncHTTPProvider(api_key=TRON_API_KEY))

        account_info = await async_tron.get_account(wallet_address)
        transactions = account_info.get('transactions', [])

        matches = []
        divisor = 10 ** DECIMALS

        for tx in transactions[-50:]:
            try:
                if tx['type'] == 'Transfer':
                    if tx['contract_address'] == USDT_CONTRACT:
                        tx_hash = tx.get('txID', '')
                        amount_raw = tx.get('value', 0)
                        amount_usdt = amount_raw / divisor

                        if min_amount_usd - tolerance <= amount_usdt <= min_amount_usd + tolerance:
                            matches.append({
                                'tx_hash': tx_hash,
                                'amount': amount_usdt,
                                'timestamp': tx.get('timestamp', 0)
                            })
            except (KeyError, TypeError):
                continue

        await async_tron.close()
        return matches

    except Exception as e:
        if "not found" in str(e).lower():
            return []
        print(f"TRON checker error: {e}")
        return []

def check_tron_wallet_sync(wallet_address, min_amount_usd, tolerance=0.01):
    """Synchronous wrapper for TRON checking."""
    try:
        account_info = tron.get_account(wallet_address)
        transactions = account_info.get('transactions', [])

        matches = []
        divisor = 10 ** DECIMALS

        for tx in transactions[-100:]:
            try:
                tx_type = tx.get('type', '')
                if tx_type == 'Transfer' or 'token_transfer' in str(tx):
                    tx_hash = tx.get('txID', '')
                    amount_raw = tx.get('value', 0)
                    if amount_raw == 0:
                        continue

                    amount_usdt = amount_raw / divisor

                    if min_amount_usd - tolerance <= amount_usdt <= min_amount_usd + tolerance:
                        matches.append({
                            'tx_hash': tx_hash,
                            'amount': amount_usdt,
                            'timestamp': tx.get('timestamp', 0),
                            'network': 'TRON'
                        })
            except (KeyError, TypeError, ValueError):
                continue

        return matches

    except Exception as e:
        if "not found" in str(e).lower():
            return []
        print(f"TRON checker error: {e}")
        return []