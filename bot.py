import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
from telegram.error import BadRequest

# --- KONFIGURÁCIÓ ---
# A Te Bot Tokened (ellenőrizd, hogy ez a legfrissebb!)
TOKEN = "8501071283:AAHAmAsZ2r1NBUSQsCI-grq4Bmrek3Cbrts"
# A Te Telegram ID-d (hogy csak te kapj admin értesítést)
ADMIN_ID = 1979330363 
# A GitHub Pages linked (az App gomb ide fog vinni)
WEB_APP_URL = "https://veresbarnabas97-ui.github.io/SkyAIWeb3" 
SUPPORT_CONTACT = "https://t.me/VeresBarnabas1"

# Fizetési Linkek
BINANCE_PAY_URL = "https://s.binance.com/FcZ8aA7w" 
REVOLUT_PAY_URL = "https://revolut.me/veresbarnabas1"

# Naplózás beállítása
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Ez a függvény fut le a /start parancsra, vagy ha a weboldalról
    érkezik egy kifizetési kérelem (deep link).
    """
    user = update.effective_user
    args = context.args

    # 1. KIFIZETÉS KEZELÉSE (Web -> Bot Deep Link)
    # Ha a linkben van paraméter (pl. t.me/bot?start=withdraw_...), akkor ez fut le.
    if args and args[0].startswith('withdraw_'):
        await handle_withdrawal_request(update, context, args[0])
        return

    # 2. ALAP FŐMENÜ (Normál indítás)
    welcome_text = (
        f"🌌 **SkyAI Ecosystem v3.8**\n\n"
        f"Üdvözöllek a fedélzeten, {user.first_name}!\n"
        "Ez a hivatalos vezérlőpult a SkyAI Web3 rendszerhez.\n\n"
        "🔥 **Már tag vagy?** Nyisd meg az APP-ot a kereskedéshez.\n"
        "🔹 **Sniper:** Gyors kereskedés ($1-$100)\n"
        "🔸 **Whale:** Intézményi szint (>$100)\n\n"
        "🔻 **Válassz opciót:**"
    )

    # Gombok létrehozása
    keyboard = [
        [InlineKeyboardButton("💎 VIP Vásárlás ($15)", callback_data='buy_vip')],
        [InlineKeyboardButton("🚀 APP MEGNYITÁSA", web_app=WebAppInfo(url=WEB_APP_URL))],
        [InlineKeyboardButton("👤 Ügyfélszolgálat", url=SUPPORT_CONTACT)]
    ]
    
    await update.message.reply_text(
        text=welcome_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gombnyomások kezelése"""
    query = update.callback_query
    
    # Hibakezelés: Ha a gomb már "lejárt" (régi üzenet), ne omoljon össze a bot
    try:
        await query.answer()
    except BadRequest:
        pass

    # --- VIP VÁSÁRLÁS MENÜ ---
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

    # --- HOZZÁFÉRÉS MEGADÁSA ---
    elif query.data == 'grant_access':
        text = (
            "🎉 **Köszönjük a bizalmat!**\n\n"
            "A rendszerünk regisztrálta az igényt. "
            "A használathoz csatlakoztasd a Phantom vagy TrustWallet tárcádat az Appon belül.\n\n"
            "**Kattints a gombra a belépéshez:**"
        )
        keyboard = [[InlineKeyboardButton("🚀 BELÉPÉS A RENDSZERBE", web_app=WebAppInfo(url=WEB_APP_URL))]]
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    # --- VISSZA A FŐMENÜBE ---
    elif query.data == 'back_home':
        await start(update, context)

    # --- ADMIN KIFIZETÉS JÓVÁHAGYÁS / ELUTASÍTÁS ---
    elif query.data.startswith('approve_') or query.data.startswith('deny_'):
        # Csak TE (az Admin) nyomhatod meg ezeket a gombokat
        if update.effective_user.id != ADMIN_ID:
            await query.answer("⛔ Nincs admin jogosultságod!", show_alert=True)
            return

        # Adatok kinyerése a gombból (action_netAmount_currency_address)
        parts = query.data.split('_')
        if len(parts) < 4: return

        action = parts[0]
        net_amount = parts[1]
        currency = parts[2]
        address = parts[3]
        
        if action == 'approve':
            # Üzenet az Adminnak a teendőkről
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=(
                    f"✅ **KIFIZETÉS JÓVÁHAGYVA!**\n\n"
                    f"⚠️ **Admin teendő:** Hajtsd végre a tranzakciót manuálisan a tárcádból.\n\n"
                    f"💸 Utalandó: **{net_amount} {currency}**\n"
                    f"📬 Cím: `{address}`\n\n"
                    f"_(A 15% levonva, a felhasználó értesítve a rendszerben.)_"
                ),
                parse_mode='Markdown'
            )
            # Gombok eltüntetése
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
    """
    Ez a függvény dolgozza fel a weboldalról érkező kifizetési kérelmet.
    Kiszámolja a 15%-ot és értesítést küld neked (Admin).
    """
    try:
        parts = payload.split('_')
        if len(parts) < 4:
            await update.message.reply_text("⚠️ Hibás kérelem formátum.")
            return

        gross_amount_str = parts[1]
        address = parts[2]
        currency = parts[3]
        
        gross_amount = float(gross_amount_str)

        # 15% SIKERDÍJ LEVONÁSA (A matek itt történik)
        fee = gross_amount * 0.15
        net_amount = gross_amount * 0.85
        
        # Formázás 4 tizedesjegyre
        net_str = f"{net_amount:.4f}"
        fee_str = f"{fee:.4f}"

        # 1. USER ÉRTESÍTÉSE (Aki kérte)
        await update.message.reply_text(
            f"🏦 **SkyAI Kifizetési Kérelem Fogadva**\n\n"
            f"A rendszerünk feldolgozás alatt tartja az igényedet.\n\n"
            f"📥 Visszakért tőke: {gross_amount_str} {currency}\n"
            f"📉 SkyAI Díj (15%): {fee_str} {currency}\n"
            f"✅ **Várható jóváírás: {net_str} {currency}**\n\n"
            f"⏳ Státusz: **Jóváhagyásra vár...**"
        )

        # 2. ADMIN ÉRTESÍTÉSE (Te kapod meg)
        if ADMIN_ID != 0:
            admin_text = (
                f"🚨 **PÉNZÜGYI TRANZAKCIÓ IGÉNY**\n\n"
                f"👤 Felhasználó: {update.effective_user.first_name} (@{update.effective_user.username})\n"
                f"💰 Bruttó tőke: {gross_amount_str} {currency}\n"
                f"✂️ 15% Rész (Nálad marad): **{fee_str} {currency}**\n"
                f"💸 **Kifizetendő (Netto): {net_str} {currency}**\n"
                f"🏦 Cím: `{address}`"
            )
            
            # Gombok az Adminnak
            keyboard = [
                [
                    InlineKeyboardButton("✅ UTALÁS ENGEDÉLYEZÉSE", callback_data=f"approve_{net_str}_{currency}_{address}"),
                    InlineKeyboardButton("❌ ELUTASÍTÁS", callback_data=f"deny_{net_str}_{currency}_{address}")
                ]
            ]
            
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=admin_text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )

    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("⚠️ Hiba történt a kérelem feldolgozásakor.")

if __name__ == '__main__':
    # Bot indítása
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Parancsok hozzáadása
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("SkyAI Ecosystem Bot Online... (Nyomj Ctrl+C-t a leállításhoz)")
    application.run_polling()
