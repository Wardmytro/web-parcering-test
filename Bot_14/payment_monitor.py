import asyncio
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import PAYMENT_MONITOR_INTERVAL, ADMIN_ID, PRICES, WALLETS
from database import get_pending_orders, update_order_status, record_transaction, get_order_by_id
from tron_checker import check_tron_wallet
from ton_checker import check_ton_wallet
from solana_checker import check_solana_wallet

CHECKER_FUNCTIONS = {
    "TRON": check_tron_wallet,
    "TON": check_ton_wallet,
    "SOLANA": check_solana_wallet
}

class PaymentMonitor:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.running = False

    async def start(self):
        """Start the payment monitoring background task."""
        self.running = True
        asyncio.create_task(self._monitor_loop())

    async def stop(self):
        """Stop the payment monitoring background task."""
        self.running = False

    async def _monitor_loop(self):
        """Continuous monitoring loop."""
        while self.running:
            try:
                await self._check_all_payments()
            except Exception as e:
                print(f"Monitor error: {e}")

            await asyncio.sleep(PAYMENT_MONITOR_INTERVAL)

    async def _check_all_payments(self):
        """Check all pending orders for payments."""
        pending_orders = get_pending_orders()

        for order in pending_orders:
            network = order['selected_network']
            wallet = order['wallet_address']
            expected_amount = order['price_usd']
            order_id = order['order_id']

            checker = CHECKER_FUNCTIONS.get(network)
            if not checker:
                continue

            transactions = checker(wallet, expected_amount)

            for tx in transactions:
                tx_hash = tx['tx_hash']

                record_transaction(tx_hash, wallet, tx['amount'], network, order_id)
                update_order_status(order_id, 'paid')

                await self._notify_admin_payment(order)

    async def _notify_admin_payment(self, order):
        """Send admin notification of payment received."""
        text = f"""
✅ <b>Payment Detected!</b>

📋 <b>Order Details:</b>
├ Order ID: <code>{order['order_id']}</code>
├ Gold: {order['gold_amount']}
├ Amount: ${order['price_usd']} USDT
├ Character: {order['character_name']}
├ Discord: {order['discord']}
├ Network: {order['selected_network']}
├ Note: {order['note'] or 'None'}
└ Status: <b>PAYMENT CONFIRMED</b>

<i>Click below to approve delivery or mark as fraud:</i>
"""

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Approve & Deliver", callback_data=f"approve_{order['order_id']}"),
                InlineKeyboardButton(text="❌ Mark Fraud", callback_data=f"fraud_{order['order_id']}")
            ]
        ])

        try:
            await self.bot.send_message(
                chat_id=ADMIN_ID,
                text=text,
                reply_markup=keyboard,
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"Failed to send notification to admin: {e}")

    async def notify_order_delivered(self, user_id: int, order_id: str):
        """Notify user that their order has been delivered."""
        order = get_order_by_id(order_id)
        if not order:
            return

        text = f"""
✅ <b>Order Delivered!</b>

Your order has been confirmed and processed.

📋 <b>Order Details:</b>
├ Order ID: <code>{order_id}</code>
├ Gold: {order['gold_amount']}
├ Character: {order['character_name']}
└ Amount Paid: ${order['price_usd']} USDT

Thank you for your purchase! You will receive your golds shortly.
Contact us on Discord if you have any issues.
"""

        try:
            await self.bot.send_message(
                chat_id=user_id,
                text=text,
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"Failed to send delivery confirmation: {e}")

async def create_monitor(bot: Bot) -> PaymentMonitor:
    """Factory function to create and start monitor."""
    monitor = PaymentMonitor(bot)
    await monitor.start()
    return monitor
