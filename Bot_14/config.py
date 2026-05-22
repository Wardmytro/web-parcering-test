import os
from dotenv import load_dotenv

load_dotenv("Keys.env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
TRON_API_KEY = os.getenv("TRON_API_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))


PRICES = {
    "100": 30,
    "500": 140,
    "1000": 285
}

WALLETS = {
    "TRON": "TLcPUcFVKRAkEK3wAMyhycXNJTX7isN1MK",
    "TON": "UQAsM_9Kd3hlckAOyTOlhs3To6BhJtLK6_sdYvhM2t2-_hvw",
    "SOLANA": "HcjEq6Cj74FHjXkhPAATPBCNTGTT4YMzu9jrYNizR35z"
}

BLOCKCHAIN_CONFIG = {
    "TRON": {
        "rpc": "https://api.tronstack.com",
        "usdt_contract": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
        "decimals": 6
    },
    "TON": {
        "rpc": "https://ton-http-api.com",
        "usdt_contract": "EQCxE6mUtQJKFnGfaROTKOt1lZbDgitvEAHxF7BtD5XRAAAB",
        "decimals": 6
    },
    "SOLANA": {
        "rpc": "https://api.mainnet-beta.solana.com",
        "usdt_contract": "Es9vMFrzaCERmJfqV3E3wFsUjfxJosrv3NFxNYcXzLsUV5DJ",
        "decimals": 6
    }
}

PAYMENT_MONITOR_INTERVAL = 60

DB_PATH = "orders.db"
