# --- bot.py a /SkyAIWeb3 (Web3 App) projekthez ---
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
from telegram.error import BadRequest

# --- CONFIGURATION (SkyAIWeb3 - PAYMENT BOT) ---
TOKEN = "8415660573:AAEn_SBRtcCkFXOTeicrYzCkglsuiDeL050" # <<< @SkyAI_PaymentBot token
WEB_URL = "https://veresbarnabas97-ui.github.io/SkyAIWeb3" # <<< A Web3 app URL-je
BASE_APP_URL = "https://veresbarnabas97-ui.github.io/SkyAI" # <<< Link az Alap Appra
SUPPORT_CONTACT = "https://t.me/VeresBarnabas1" 

# Payment Links (Kiemelten kezelve)
BINANCE_PAY_URL = "https://s.binance.com/FcZ8aA7w"
REVOLUT_PAY_URL = "https://revolut.me/veresbarnabas1"

# --- LOGGING SETUP ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Főmenü indítása /start parancsra (Payment Bot fókusszal)"""
    user_name = update.effective_user.first_name
    
    # Payment-orientált üdvözlő üzenet
    welcome_text = (
        f"💳 **Üdvözlünk, {user_name}! Én vagyok a SkyAI Payment & Support Bot!**\n\n"
        "Én felelek a **SkyAI Web3** platformhoz tartozó **fizetési tranzakciókért, támogatásokért és a számlázással** kapcsolatos kérdések kezeléséért.\n\n"
        "⬇️ **Válaszd ki az alábbiak közül a számodra releváns opciót:**"
    )

    # Főmenü Gombok (Fókusz: Fizetés, Web3 App, és Átirányítás a Business Bothoz)
    keyboard = [
        # 1. sor: A legfontosabb akció (Fizetés/Támogatás)
        [InlineKeyboardButton("✅ Előfizetés/Támogatás (Donate)", callback_data='donate_menu')],
        
        # 2. sor: A Web3 app indítása
        [InlineKeyboardButton("🚀 SkyAI Web3 Terminál Indítása", web_app=WebAppInfo(url=WEB_URL))],
        
        # 3. sor: Keresztpromóció
        [InlineKeyboardButton("➡️ Business Bot / Alap App", url="https://t.me/SkyAIBusinessBot")], 
         
        # 4. sor: Info
        [InlineKeyboardButton("ℹ️ Általános Kérdések (GYIK)", callback_data='faq'),
         InlineKeyboardButton("📞 Közvetlen Kapcsolat", url=SUPPORT_CONTACT)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=welcome_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gombnyomások kezelése"""
    query = update.callback_query

    try:
        await query.answer() 
    except BadRequest:
        return

    # --- MENÜPONTOK LOGIKÁJA ---
    
    elif query.data == 'donate_menu':
        # Támogatási almenü (Binance & Revolut)
        donate_text = (
            "💳 **Fizetési / Támogatási Lehetőségek**\n\n"
            "Itt tudsz előfizetni a SkyAI Web3 prémium funkciókra, vagy támogathatod a fejlesztéseket (adományt max. $50 értékig fogadunk el).\n\n"
            "**Kérlek, válassz fizetési módot:**"
        )
        keyboard = [
            [InlineKeyboardButton("🟡 Binance PAY (Crypto/USDC)", url=BINANCE_PAY_URL)],
            [InlineKeyboardButton("🔵 Revolut PAY (EUR/HUF Fiat)", url=REVOLUT_PAY_URL)],
            [InlineKeyboardButton("🔙 Vissza a főmenübe", callback_data='back_home')]
        ]
        await query.edit_message_text(text=donate_text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'faq':
        # Gyakran Ismételt Kérdések
        faq_text = (
            "ℹ️ **Gyakran Ismételt Kérdések (GYIK)**\n\n"
            "1. **Hol van a Business Bot?** \n   A fő app funkcióiért kérlek keresd a @SkyAIBusinessBot-ot.\n"
            "2. **Hogyan fizethetek?** \n   Kattints az 'Előfizetés/Támogatás' gombra és válassz módot.\n"
            "3. **Működik a Web3 app mobilról?** \n   Igen, a Telegram WebApp támogatja a mobil használatot.\n"
            "4. **Hol kérhetek technikai segítséget?** \n   A 'Közvetlen Kapcsolat' gomb alatt érhetsz el minket."
        )
        keyboard = [
            [InlineKeyboardButton("📞 Közvetlen Kapcsolat", url=SUPPORT_CONTACT)],
            [InlineKeyboardButton("🔙 Vissza a főmenübe", callback_data='back_home')]
        ]
        await query.edit_message_text(text=faq_text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))


    elif query.data == 'back_home':
        # Visszatérés a főmenübe (Payment Bot fókusszal)
        welcome_text = "💳 **Főmenü**\n\nMiben segíthetek a fizetési folyamatokban?"
        
        keyboard = [
            [InlineKeyboardButton("✅ Előfizetés/Támogatás (Donate)", callback_data='donate_menu')],
            [InlineKeyboardButton("🚀 SkyAI Web3 Terminál Indítása", web_app=WebAppInfo(url=WEB_URL))],
            [InlineKeyboardButton("➡️ Business Bot / Alap App", url="https://t.me/SkyAIBusinessBot")],
            [InlineKeyboardButton("ℹ️ Általános Kérdések (GYIK)", callback_data='faq'),
             InlineKeyboardButton("📞 Közvetlen Kapcsolat", url=SUPPORT_CONTACT)]
        ]
        await query.edit_message_text(text=welcome_text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

if __name__ == '__main__':
    # Bot Inicializálása
    application = ApplicationBuilder().token(TOKEN).build()

    # Handlerek hozzáadása
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_click))

    print("SkyAI Payment Bot (Web3 App) ONLINE...")
    
    # Futtatás
    application.run_polling()
