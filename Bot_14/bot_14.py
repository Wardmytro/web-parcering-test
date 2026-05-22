import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from config import BOT_TOKEN, PRICES, WALLETS, ADMIN_ID
from database import init_database, create_order, get_pending_orders, update_order_status, get_order_by_id, get_all_orders
from payment_monitor import create_monitor

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

btn_100 = KeyboardButton(text="100 golds\n$30 USDT")
btn_500 = KeyboardButton(text="500 golds\n$140 USDT")
btn_1000 = KeyboardButton(text="1000 golds\n$285 USDT")
main_menu = ReplyKeyboardMarkup(keyboard=[[btn_100, btn_500, btn_1000]], resize_keyboard=True)

btn_tron = KeyboardButton(text="TRON")
btn_ton = KeyboardButton(text="TON")
btn_solana = KeyboardButton(text="SOLANA")
network_menu = ReplyKeyboardMarkup(keyboard=[[btn_tron, btn_ton, btn_solana]], resize_keyboard=True)

btn_skip = KeyboardButton(text="/skip")
skip_menu = ReplyKeyboardMarkup(keyboard=[[btn_skip]], resize_keyboard=True)

class OrderForm(StatesGroup):
    waiting_for_gold = State()
    waiting_for_char_name = State()
    waiting_for_discord = State()
    waiting_for_note = State()
    waiting_for_network = State()
    payment_pending = State()
    awaiting_admin_approval = State()

monitor = None

@dp.message(Command("start"))
async def command_start(message: types.Message, state: FSMContext):
    await message.answer("👋 Welcome! I am your gold order bot.\n\nHow much USDT worth of golds would you like to order?", reply_markup=main_menu)
    await state.set_state(OrderForm.waiting_for_gold)

@dp.message(OrderForm.waiting_for_gold)
async def select_gold(message: types.Message, state: FSMContext):
    if not message.text:
        await message.answer("Please select from the menu", reply_markup=main_menu)
        return
    gold_amount = message.text.split()[0]
    if gold_amount in ["100", "500", "1000"]:
        price = PRICES[gold_amount]
        await state.update_data(gold_amount=gold_amount)
        await message.answer(f"Great! You chose {gold_amount} golds for ${price} USDT.\n\n👤 Now, please enter your discord name:", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[btn_skip]]))
        await state.set_state(OrderForm.waiting_for_char_name)
    else:
        await message.answer("Please select a valid option from the menu", reply_markup=main_menu)
@dp.message(OrderForm.waiting_for_char_name)
async def get_char_name(message: types.Message, state: FSMContext):
    await state.update_data(char_name=message.text)
    await message.answer("🎮 Enter your Discord username:")
    await state.set_state(OrderForm.waiting_for_discord)

@dp.message(OrderForm.waiting_for_discord)
async def get_discord(message: types.Message, state: FSMContext):
    await state.update_data(discord=message.text)
    await message.answer("📝 Add a note or special request (/skip if none):")
    await state.set_state(OrderForm.waiting_for_note)

@dp.message(OrderForm.waiting_for_note)
async def get_note(message: types.Message, state: FSMContext):
    note = "No notes" if message.text == "/skip" else message.text
    await state.update_data(note=note)
    await message.answer("🌐 Choose payment network:", reply_markup=network_menu)
    await state.set_state(OrderForm.waiting_for_network)

@dp.message(OrderForm.waiting_for_network)
async def select_network(message: types.Message, state: FSMContext):
    if message.text not in WALLETS:
        await message.answer("Choose from the menu", reply_markup=network_menu)
        return

    data = await state.get_data()
    gold = data['gold_amount']
    price = PRICES[gold]
    wallet = WALLETS[message.text]

    order_id = create_order(
        user_id=message.from_user.id,
        character_name=data['char_name'],
        discord=data['discord'],
        gold_amount=int(gold),
        price_usd=price,
        network=message.text,
        note=data['note']
    )

    summary = f"""
📋 <b>Order Summary</b>

💰 Gold: {gold} → ${price} USDT
👤 Character: {data['char_name']}
🎮 Discord: {data['discord']}
📝 Note: {data['note']}
🌐 Network: {message.text}

<b>💳 Payment Details:</b>
Network: <code>{message.text}</code>
Send exactly: <code>${price} USDT</code>
To address: <code>{wallet}</code>

<i>Waiting for payment confirmation...</i>
Order ID: <code>{order_id}</code>
"""

    await state.update_data(network=message.text, price=price, wallet=wallet, order_id=order_id)
    await message.answer(summary, parse_mode="HTML")
    await state.set_state(OrderForm.payment_pending)

@dp.message(OrderForm.payment_pending)
async def payment_pending(message: types.Message, state: FSMContext):
    await message.answer("⏳ Waiting for payment confirmation...\n\nOnce payment is received, the admin will review and approve delivery.")

@dp.message(Command("pending_orders"))
async def pending_orders(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ This command is for admins only.")
        return

    orders = get_pending_orders()
    if not orders:
        await message.answer("✅ No pending orders!")
        return

    text = "<b>📋 Pending Orders:</b>\n\n"
    for order in orders:
        status_emoji = "⏳" if order['status'] == 'pending' else "💰" if order['status'] == 'paid' else "✅"
        text += f"{status_emoji} <b>Order {order['order_id']}</b>\n"
        text += f"  Gold: {order['gold_amount']} | Price: ${order['price_usd']}\n"
        text += f"  Character: {order['character_name']} | Discord: {order['discord']}\n"
        text += f"  Status: {order['status']}\n\n"

    await message.answer(text, parse_mode="HTML")

@dp.message(Command("all_orders"))
async def all_orders(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ This command is for admins only.")
        return

    orders = get_all_orders()
    if not orders:
        await message.answer("✅ No orders!")
        return

    text = "<b>📊 All Orders:</b>\n\n"
    for order in orders[:10]:
        status_emoji = "⏳" if order['status'] == 'pending' else "💰" if order['status'] == 'paid' else "✅"
        text += f"{status_emoji} <b>{order['order_id']}</b> - {order['status']}\n"

    await message.answer(text, parse_mode="HTML")

@dp.callback_query(F.data.startswith("approve_"))
async def approve_delivery(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ Unauthorized", show_alert=True)
        return

    order_id = callback.data.replace("approve_", "")
    order = get_order_by_id(order_id)

    if not order:
        await callback.answer("❌ Order not found", show_alert=True)
        return

    update_order_status(order_id, 'delivered')

    await callback.answer("✅ Order approved and marked as delivered!", show_alert=True)
    await callback.message.edit_text(
        callback.message.text + "\n\n✅ <b>APPROVED BY ADMIN</b>",
        parse_mode="HTML"
    )

    try:
        user_id = order['user_id']
        confirmation = f"""
✅ <b>Your order has been approved!</b>

Order ID: <code>{order_id}</code>
Gold: {order['gold_amount']}
Character: {order['character_name']}

Your golds will be delivered shortly.
Contact us on Discord if you have any questions.
"""
        await bot.send_message(user_id, confirmation, parse_mode="HTML")
    except Exception as e:
        print(f"Failed to send user confirmation: {e}")

@dp.callback_query(F.data.startswith("fraud_"))
async def mark_fraud(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ Unauthorized", show_alert=True)
        return

    order_id = callback.data.replace("fraud_", "")
    update_order_status(order_id, 'fraud')

    await callback.answer("❌ Order marked as fraud", show_alert=True)
    await callback.message.edit_text(
        callback.message.text + "\n\n❌ <b>MARKED AS FRAUD</b>",
        parse_mode="HTML"
    )

async def main():
    init_database()

    global monitor
    monitor = await create_monitor(bot)

    try:
        print("🤖 Bot started and listening...")
        await dp.start_polling(bot)
    finally:
        if monitor:
            await monitor.stop()

if __name__ == "__main__":
    asyncio.run(main())
