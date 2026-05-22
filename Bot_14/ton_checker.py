import aiohttp
import asyncio
import requests
from config import BLOCKCHAIN_CONFIG

TON_CONFIG = BLOCKCHAIN_CONFIG["TON"]
TON_RPC = "https://tonapi.io/v2"
USDT_MASTER = "EQCxE6mUtQJKFnGfaROTKOt1lZbDgitvEAHxF7BtD5XRAAAB"

async def check_ton_wallet(wallet_address, min_amount_usd, tolerance=0.01):
    """
    Check TON wallet for USDT transfers.
    Returns: List of transactions matching the amount
    """
    try:
        async with aiohttp.ClientSession() as session:
            headers = {"Content-Type": "application/json"}
            url = f"{TON_RPC}/accounts/{wallet_address}/transactions"

            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status != 200:
                    return []

                data = await resp.json()
                transactions = data.get('transactions', [])

                matches = []
                divisor = 10 ** 6

                for tx in transactions[:50]:
                    try:
                        in_msg = tx.get('in_msg', {})
                        if not in_msg:
                            continue

                        body = in_msg.get('body', '')
                        value = int(in_msg.get('value', '0') or 0) / divisor

                        if min_amount_usd - tolerance <= value <= min_amount_usd + tolerance:
                            matches.append({
                                'tx_hash': tx.get('transaction_id', {}).get('hash', ''),
                                'amount': value,
                                'timestamp': tx.get('utime', 0),
                                'network': 'TON'
                            })

                    except (KeyError, ValueError, TypeError):
                        continue

                return matches

    except Exception as e:
        print(f"TON async checker error: {e}")
        return []

def check_ton_wallet_sync(wallet_address, min_amount_usd, tolerance=0.01):
    """
    Synchronous TON wallet checker.
    """
    try:
        url = f"{TON_RPC}/accounts/{wallet_address}/transactions"
        headers = {"Content-Type": "application/json"}

        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"TON API error: {response.status_code}")
            return []

        data = response.json()
        transactions = data.get('transactions', [])

        matches = []
        divisor = 10 ** 6

        for tx in transactions[:50]:
            try:
                in_msg = tx.get('in_msg', {})
                if not in_msg:
                    continue

                value = int(in_msg.get('value', '0') or 0) / divisor

                if min_amount_usd - tolerance <= value <= min_amount_usd + tolerance:
                    matches.append({
                        'tx_hash': tx.get('transaction_id', {}).get('hash', ''),
                        'amount': value,
                        'timestamp': tx.get('utime', 0),
                        'network': 'TON'
                    })

            except (KeyError, ValueError, TypeError):
                continue

        return matches

    except Exception as e:
        print(f"TON checker error: {e}")
        return []
