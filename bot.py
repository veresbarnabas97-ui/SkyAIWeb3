import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
from telegram.error import BadRequest

# --- KONFIGURÁCIÓ ---
TOKEN = "8501071283:AAHAmAsZ2r1NBUSQsCI-grq4Bmrek3Cbrts"
ADMIN_ID = 1979330363 
WEB_APP_URL = "https://veresbarnabas97-ui.github.io/SkyAIWeb3" 
SUPPORT_CONTACT = "https://t.me/VeresBarnabas1"

# Fizetési Linkek
BINANCE_PAY_URL = "https://s.binance.com/FcZ8aA7w" 
REVOLUT_PAY_URL = "https://revolut.me/veresbarnabas1"

# Naplózás
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Főmenü és Deep Link kezelés"""
    user = update.effective_user
    args = context.args

    # 1. Kifizetési kérelem kezelése (csak ha üzenetből jön)
    if update.message and args and args[0].startswith('withdraw_'):
        await handle_withdrawal_request(update, context, args[0])
        return

    # 2. Főmenü szövege
    welcome_text = (
        f"🌌 **SkyAI Ecosystem v3.8**\n\n"
        f"Üdvözöllek a fedélzeten, {user.first_name}!\n"
        "Ez a hivatalos vezérlőpult a SkyAI Web3 rendszerhez.\n\n"
        "🔥 **Már tag vagy?** Nyisd meg az APP-ot a kereskedéshez.\n"
        "🔹 **Sniper:** Gyors kereskedés ($1-$100)\n"
        "🔸 **Whale:** Intézményi szint (>$100)\n\n"
        "🔻 **Válassz opciót:**"
    )

    keyboard = [
        [InlineKeyboardButton("💎 VIP Vásárlás ($15)", callback_data='buy_vip')],
        [InlineKeyboardButton("🚀 APP MEGNYITÁSA", web_app=WebAppInfo(url=WEB_APP_URL))],
        [InlineKeyboardButton("👤 Ügyfélszolgálat", url=SUPPORT_CONTACT)]
    ]
    
    # HIBAJAVÍTÁS: Külön kezeljük a gombnyomást és a szöveges parancsot
    if update.message:
        # Ha /start parancsot írtál
        await update.message.reply_text(
            text=welcome_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    elif update.callback_query:
        # Ha a "Vissza" gombot nyomtad meg (szerkesztjük az előző üzenetet)
        await update.callback_query.message.edit_text(
            text=welcome_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gombnyomások kezelése"""
    query = update.callback_query
    
    try:
        await query.answer()
    except BadRequest:
        pass

    if query.data == 'buy_vip':
        text = (
            "💎 **SkyAI VIP Access Vásárlás**\n\n"
            "A teljes ökoszisztéma ára: **$15** (Egyszeri díj)\n\n"
            "Mit kapsz érte?\n"
            "✅ Sniper & Whale modulok feloldása\n"
            "✅ Okosszerződéses kereskedés\n"
            "✅ Hozzáférés a chartokhoz és szignálokhoz\n\n"
            "**Fizetési lehetőségek:**"
        )
        keyboard = [
            [InlineKeyboardButton("🟡 Binance PAY (Crypto)", url=BINANCE_PAY_URL)],
            [InlineKeyboardButton("🔵 Revolut (Fiat)", url=REVOLUT_PAY_URL)],
            [InlineKeyboardButton("✅ Fizettem, kérem a hozzáférést", callback_data='grant_access')],
            [InlineKeyboardButton("🔙 Vissza", callback_data='back_home')]
        ]
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data == 'grant_access':
        text = (
            "🎉 **Köszönjük a bizalmat!**\n\n"
            "A rendszerünk regisztrálta az igényt. "
            "A használathoz csatlakoztasd a Phantom vagy TrustWallet tárcádat az Appon belül.\n\n"
            "**Kattints a gombra a belépéshez:**"
        )
        keyboard = [[InlineKeyboardButton("🚀 BELÉPÉS A RENDSZERBE", web_app=WebAppInfo(url=WEB_APP_URL))]]
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data == 'back_home':
        await start(update, context)

    # --- ADMIN MŰVELETEK ---
    elif query.data.startswith('approve_') or query.data.startswith('deny_'):
        if update.effective_user.id != ADMIN_ID:
            await query.answer("⛔ Nincs admin jogosultságod!", show_alert=True)
            return

        parts = query.data.split('_')
        if len(parts) < 4: return

        action = parts[0]
        net_amount = parts[1]
        currency = parts[2]
        address = parts[3]
        
        if action == 'approve':
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=(
                    f"✅ **KIFIZETÉS JÓVÁHAGYVA!**\n\n"
                    f"⚠️ **Admin teendő:** Hajtsd végre a tranzakciót manuálisan.\n\n"
                    f"💸 Utalandó: **{net_amount} {currency}**\n"
                    f"📬 Cím: `{address}`\n\n"
                    f"_(A 15% levonva, a felhasználó értesítve a rendszerben.)_"
                ),
                parse_mode='Markdown'
            )
            try: await query.edit_message_reply_markup(reply_markup=None)
            except BadRequest: pass 
            
        elif action == 'deny':
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"❌ **KIFIZETÉS ELUTASÍTVA.**\nA tőke a te walletedben maradt.",
                parse_mode='Markdown'
            )
            try: await query.edit_message_reply_markup(reply_markup=None)
            except BadRequest: pass

async def handle_withdrawal_request(update: Update, context: ContextTypes.DEFAULT_TYPE, payload: str):
    """Kifizetési kérelem feldolgozása"""
    try:
        parts = payload.split('_')
        if len(parts) < 4: return

        gross = float(parts[1])
        address = parts[2]
        currency = parts[3]
        
        fee = gross * 0.15
        net = gross * 0.85
        
        # Usernek
        await update.message.reply_text(
            f"🏦 **SkyAI Kifizetési Kérelem Fogadva**\n\n"
            f"📥 Visszakért: {gross} {currency}\n"
            f"📉 Díj (15%): {fee:.4f} {currency}\n"
            f"✅ **Kifizetendő: {net:.4f} {currency}**\n\n"
            f"⏳ Státusz: **Jóváhagyásra vár...**"
        )

        # Adminnak (NEKED)
        if ADMIN_ID != 0:
            admin_text = (
                f"🚨 **PÉNZÜGYI TRANZAKCIÓ IGÉNY**\n\n"
                f"👤 Felhasználó: {update.effective_user.first_name}\n"
                f"💰 Bruttó: {gross} {currency}\n"
                f"💸 **Netto (Utalandó): {net:.4f} {currency}**\n"
                f"🏦 Cím: `{address}`"
            )
            
            keyboard = [
                [InlineKeyboardButton("✅ ENGEDÉLYEZÉS", callback_data=f"approve_{net:.4f}_{currency}_{address}")],
                [InlineKeyboardButton("❌ ELUTASÍTÁS", callback_data=f"deny_{net:.4f}_{currency}_{address}")]
            ]
            
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=admin_text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )

    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))
    print("SkyAI Ecosystem Bot Online... (Nyomj Ctrl+C-t a leállításhoz)")
    application.run_polling()
