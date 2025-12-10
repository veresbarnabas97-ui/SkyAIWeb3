import telebot
import google.generativeai as genai
import os
from telebot import types

# --- KONFIGURÁCIÓ (A TE ADATAIDDAL) ---
CONFIG = {
    # A TE Telegram Bot Tokened
    "TELEGRAM_TOKEN": "8501071283:AAHAmAsZ2r1NBUSQsCI-grq4Bmrek3Cbrts",
    
    # A TE Admin ID-d (Ide jönnek az értesítések)
    "ADMIN_ID": "1979330363",
    
    # Google Gemini API kulcs (A HTML-ből másolva - érdemes sajátot generálni!)
    "GEMINI_API_KEY": "AIzaSyBQdBJtfipjQp0FrhjjL0e8rASorng0ics",
    
    # A TE TÁRCACÍMEID (Ezekre érkezik a pénz a weboldalról)
    # Ellenőrizd, hogy ezek a saját címeid-e!
    "OWNER_BSC": "0xC424c3119e5D1fA6dD91eF72aF25e1F4A260f69C",
    "OWNER_SOL": "4iubzdpP14Mo32iRseD7nZEhP1RVLWjjwbsh228uBk3z"
}

# --- INICIALIZÁLÁS ---
try:
    bot = telebot.TeleBot(CONFIG["TELEGRAM_TOKEN"])
    genai.configure(api_key=CONFIG["GEMINI_API_KEY"])
    print("✅ Bot sikeresen csatlakozott a Telegramhoz!")
except Exception as e:
    print(f"❌ Hiba a csatlakozáskor: {e}")
    exit()

# Gemini Modell beállítása
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", 
        generation_config=generation_config,
        system_instruction="Te a SkyAI kereskedési ökoszisztéma professzionális asszisztense vagy. Segítesz a felhasználóknak a kripto elemzésben és a platform használatában. Válaszolj röviden, lényegre törően, magyar nyelven."
    )
    print("✅ Gemini AI modul betöltve.")
except Exception as e:
    print(f"⚠️ Gemini AI hiba (lehet, hogy a kulcs lejárt): {e}")

print("--- SkyAI Bot System Online (Várakozás üzenetekre...) ---")

# --- START PARANCS & KIFIZETÉS KEZELÉS ---
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    username = message.from_user.username if message.from_user.username else "Ismeretlen"
    text = message.text.split()

    # Ellenőrizzük, hogy van-e paraméter (pl. withdraw_...)
    if len(text) > 1:
        param = text[1]
        
        # KIFIZETÉSI KÉRELEM FELDOLGOZÁSA
        if param.startswith("withdraw_"):
            try:
                # A HTML ezt a formátumot küldi: withdraw_AMOUNT_ADDRESS_CURRENCY
                # Példa: withdraw_1.5_0xabc..._BNB
                parts = param.split("_")
                # Biztonsági ellenőrzés, ha a címben alulvonás lenne
                amount = parts[1]
                address = parts[2]
                currency = parts[3]
                
                # Válasz a felhasználónak
                reply = f"✅ <b>Kifizetési kérelem rögzítve!</b>\n\n" \
                        f"💰 Összeg: <b>{amount} {currency}</b>\n" \
                        f"🏦 Cím: <code>{address}</code>\n\n" \
                        f"⏳ Az adminisztrátor hamarosan ellenőrzi és jóváhagyja a tranzakciót."
                
                bot.send_message(user_id, reply, parse_mode="HTML")
                
                # Értesítés az ADMINNAK (Neked)
                admin_alert = f"⚠️ <b>ÚJ KIFIZETÉSI IGÉNY!</b>\n\n" \
                              f"👤 User: @{username} (ID: <code>{user_id}</code>)\n" \
                              f"💰 Összeg: <b>{amount} {currency}</b>\n" \
                              f"🏦 Cím: <code>{address}</code>\n" \
                              f"🔗 <a href='tg://user?id={user_id}'>Felhasználó profilja</a>"
                
                # Gombok az Adminnak
                markup = types.InlineKeyboardMarkup()
                # Callback data-ba eltároljuk a UserID-t
                btn_approve = types.InlineKeyboardButton("✅ Jóváhagyás (Manual)", callback_data=f"approve_{user_id}")
                btn_reject = types.InlineKeyboardButton("❌ Elutasítás", callback_data=f"reject_{user_id}")
                markup.add(btn_approve, btn_reject)
                
                # Küldés az ADMIN ID-ra
                bot.send_message(CONFIG["ADMIN_ID"], admin_alert, parse_mode="HTML", reply_markup=markup)
                print(f"Új kifizetési kérelem érkezett: {username} - {amount} {currency}")
                return

            except Exception as e:
                bot.send_message(user_id, "❌ Hibás kifizetési formátum. Kérlek használd a weboldalt a generáláshoz.")
                print(f"Hiba a paraméter feldolgozásakor: {e}")
                return

    # Sima üdvözlés, ha nincs paraméter
    welcome_msg = "Üdvözöllek a <b>SkyAI Ecosystem</b> hivatalos botjában! 🌌\n\n" \
                  "Itt tudod kezelni a profilodat, értesítéseket kapsz a kereskedésekről, " \
                  "és beszélgethetsz a Gemini AI asszisztenssel.\n\n" \
                  "<i>Írj be bármit a csevegéshez!</i>"
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📈 Piacok"), types.KeyboardButton("👤 Profilom"))
    bot.send_message(user_id, welcome_msg, parse_mode="HTML", reply_markup=markup)

# --- ADMIN GOMB KEZELÉS ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # Ellenőrizzük, hogy tényleg te nyomtad-e meg a gombot
    if str(call.from_user.id) != str(CONFIG["ADMIN_ID"]):
        bot.answer_callback_query(call.id, "Nincs jogosultságod ehhez!", show_alert=True)
        return

    try:
        if call.data.startswith("approve_"):
            target_id = call.data.split("_")[1]
            bot.answer_callback_query(call.id, "Kifizetés jóváhagyva (Manuális utalás szükséges!)")
            
            # Értesítjük a felhasználót
            bot.send_message(target_id, "✅ <b>Kifizetés JÓVÁHAGYVA!</b>\nAz összeg hamarosan megérkezik a tárcádba.")
            
            # Frissítjük az admin üzenetet
            bot.edit_message_text(f"✅ Kifizetés jóváhagyva a felhasználónak: {target_id}\n(Ne felejtsd el elutalni!)", call.message.chat.id, call.message.message_id)
            
        elif call.data.startswith("reject_"):
            target_id = call.data.split("_")[1]
            bot.answer_callback_query(call.id, "Kifizetés elutasítva")
            
            # Értesítjük a felhasználót
            bot.send_message(target_id, "❌ <b>Kifizetés ELUTASÍTVA!</b>\nKérlek vedd fel a kapcsolatot a supporttal.")
            
            # Frissítjük az admin üzenetet
            bot.edit_message_text(f"❌ Kifizetés elutasítva a felhasználónak: {target_id}", call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(f"Hiba a gombkezelésnél: {e}")

# --- AI CHAT KEZELÉS (Gemini) ---
@bot.message_handler(func=lambda message: True)
def handle_ai_chat(message):
    # Admin parancs teszthez
    if message.text == "/admin_check" and str(message.from_user.id) == str(CONFIG["ADMIN_ID"]):
        bot.reply_to(message, "👑 Adminisztrátor azonosítva. Rendszer működik.")
        return

    # Válaszoljunk a menü gombokra
    if message.text == "📈 Piacok":
        bot.reply_to(message, "A piacok megtekintéséhez látogass el a weboldalra: [SkyAI Ecosystem](https://skyai.com)", parse_mode="Markdown")
        return
    elif message.text == "👤 Profilom":
        bot.reply_to(message, f"Felhasználó: {message.from_user.first_name}\nID: `{message.from_user.id}`\nStátusz: SkyAI User", parse_mode="Markdown")
        return

    # Minden más üzenetet küldjünk a Gemini AI-nak
    try:
        # Chat session indítása (előzmények nélkül, hogy spóroljunk a tokennel)
        chat = model.start_chat(history=[])
        response = chat.send_message(message.text)
        
        # Formázzuk a választ Markdown-ba a Telegramnak
        bot.reply_to(message, response.text, parse_mode="Markdown")
    except Exception as e:
        print(f"AI Hiba: {e}")
        bot.reply_to(message, "⚠️ A SkyAI szerverek jelenleg túlterheltek, vagy a Gemini API kulcs limitje betelt. Próbáld újra később.")

# --- START BOT ---
if __name__ == "__main__":
    bot.infinity_polling()
