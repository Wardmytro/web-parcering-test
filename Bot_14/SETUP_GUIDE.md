# Telegram Bot Payment Verification System - Setup Guide

## Overview
This bot handles gold orders with automatic blockchain payment verification across TRON, TON, and SOLANA networks. Payments are continuously monitored, and admins receive notifications for approval/delivery.

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Configuration

#### Keys.env
Create or update `Keys.env` with:
```
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_ID=your_admin_telegram_id_here
```

**⚠️ SECURITY:** Never commit `Keys.env` to version control. It's in `.gitignore`.

#### config.py
Already configured with:
- Wallet addresses (TRON, TON, SOLANA)
- Price mapping (100/500/1000 golds)
- Free blockchain RPC endpoints
- Payment monitoring interval (45 seconds)

### 3. Initialize Database
```bash
python database.py
```
This creates `orders.db` with tables for orders and transactions.

## Running the Bot

### Start Payment Verification Bot
```bash
python bot_payment.py
```

The bot will:
1. Start listening for user orders
2. Automatically monitor all pending orders
3. Notify admin when payments are detected
4. Wait for admin approval before confirming delivery

## User Flow

### 1. Customer Order Process
1. `/start` - Begins order process
2. Select gold amount (100/500/1000)
3. Enter character name
4. Enter Discord username
5. Add optional note (/skip for none)
6. Select blockchain network (TRON/TON/SOLANA)
7. Receives wallet address and exact amount due
8. **Waits for payment confirmation**

### 2. Payment Detection
- Bot continuously monitors all 3 wallets (every 45 seconds)
- When exact amount is received, status changes to "PAID"
- Admin receives notification with order details

### 3. Admin Approval
- Admin sees button-based notification
- **✅ Approve & Deliver** - Marks as delivered, notifies user
- **❌ Mark Fraud** - Flags order as fraudulent

## Admin Commands

| Command | Purpose |
|---------|---------|
| `/pending_orders` | Show all orders awaiting payment or approval |
| `/all_orders` | Show recent orders (last 10) |

### Callback Actions (Button Clicks)
- **✅ Approve & Deliver** - Approve payment and send delivery confirmation
- **❌ Mark Fraud** - Mark order as fraudulent

## Price List

| Gold Amount | USD Price | Network |
|------------|-----------|---------|
| 100 | $30 | TRON/TON/SOLANA |
| 500 | $140 | TRON/TON/SOLANA |
| 1000 | $285 | TRON/TON/SOLANA |

## Wallet Addresses (USDT)

### TRON (TRC20)
```
TLcPUcFVKRAkEK3wAMyhycXNJTX7isN1MK
```

### TON
```
UQAsM_9Kd3hlckAOyTOlhs3To6BhJtLK6_sdYvhM2t2-_hvw
```

### SOLANA (SPL)
```
HcjEq6Cj74FHjXkhPAATPBCNTGTT4YMzu9jrYNizR35z
```

## Database Schema

### orders table
```
order_id (PK)
user_id
character_name
discord
gold_amount
price_usd
selected_network
wallet_address
note
status (pending/paid/delivered/fraud)
created_at
paid_at
delivered_at
```

### transactions table
```
tx_hash (PK)
wallet_address
amount_received
network
confirmed_at
order_id (FK)
```

## File Structure

```
├── bot_payment.py         # Main bot with user/admin interface
├── config.py              # Configuration (wallets, prices, RPC endpoints)
├── database.py            # SQLite setup and queries
├── payment_monitor.py     # Background payment monitoring service
├── tron_checker.py        # TRON blockchain verification
├── ton_checker.py         # TON blockchain verification
├── solana_checker.py      # SOLANA blockchain verification
├── requirements.txt       # Python dependencies
├── .gitignore             # Git configuration
├── Keys.env               # Environment secrets (never commit)
└── orders.db              # SQLite database (auto-created)
```

## Blockchain API Details

### TRON
- **Library:** tronpy
- **Endpoint:** https://api.tronstack.com (free)
- **No API key required**
- **USDT Contract:** TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t (TRC20)

### TON
- **Endpoint:** https://ton-http-api.com (free)
- **No authentication required**
- **Uses TON RPC API**

### SOLANA
- **Endpoint:** https://api.mainnet-beta.solana.com (free, rate-limited)
- **Libraries:** solders
- **Token:** Es9vMFrzaCERmJfqV3E3wFsUjfxJosrv3NFxNYcXzLsUV5DJ (USDT-SPL)

## Monitoring Details

**Interval:** 45 seconds (configurable in config.py as `PAYMENT_MONITOR_INTERVAL`)

**For each pending order:**
1. Queries blockchain for transactions to the order's wallet
2. Checks if amount matches (±$0.01 tolerance for network fees)
3. Updates order status to "paid"
4. Records transaction hash
5. Notifies admin with order summary + approval buttons

## Troubleshooting

### Bot doesn't respond
- Check `BOT_TOKEN` in Keys.env
- Ensure bot has message permissions in Telegram

### Payments not detected
- Verify wallet address is correct
- Check blockchain explorer that funds arrived
- Verify exact amount (including decimals)
- Increase monitoring interval if rate-limited by RPC

### Admin notifications not arriving
- Verify `ADMIN_ID` in Keys.env (get from @userinfobot)
- Ensure bot is running with monitor active
- Check if admin blocked the bot

### Database errors
- Delete `orders.db` and run `python database.py` again
- Check file permissions

## Security Considerations

✅ **Safe:**
- Wallet addresses are read-only (no funds at risk)
- All private keys remain client-side (user's wallet)

⚠️ **Important:**
- Keep Keys.env out of version control
- Admin ID must be correct (has full control)
- USDT contract addresses are hardcoded (verified)
- Regenerate bot token if compromised

## Testing

To test the bot locally:

1. **Create a test order** through the bot interface
2. **Send a test USDT transaction** from your wallet to the displayed address
3. **Monitor bot logs** - should show payment detection within 45 seconds
4. **Check admin notification** - admin receives payment confirmation
5. **Click approve button** - user receives delivery confirmation

For testing without real USDT:
- Use testnet addresses and adjust config.py endpoints
- Use test USDT on TRON testnet: https://testnet.trongrid.io

## Support

For issues:
1. Check error messages in bot logs
2. Verify all wallet addresses are correct
3. Ensure RPC endpoints are accessible
4. Check database is writable
5. Verify Telegram API token is valid

---

**Version:** 1.0  
**Last Updated:** 2026-05-22
