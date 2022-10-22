import os
import telebot
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from hashlib import blake2b
from decouple import config
from db import insert, user_search, in_process, process_search, delete_process

bot = telebot.TeleBot(config('Token'))

def extract_unique_code(text):
	print(text)
	return text.split()[1] if len(text.split()) > 1 else None

@bot.message_handler(commands=['start'])
def start(msg):
	link_part = '[link](https://github.com)'
	
	unique_code = extract_unique_code(msg.text)
	if unique_code:  
		username = user_search(unique_code)

		if username != str(msg.chat.id): 
			
			process_hash = blake2b(str(f'{msg.chat.id}{username}').encode('utf-8'),digest_size=10).hexdigest()
			in_process(msg.chat.id, username, process_hash)
			
			reply = '''
شما در حال پیام دادن به مخاطب خود هستید...

میتونی هر حرفی که دلت میخواد رو بگی ولی سعی کن حواست رو جمع کنی چون تو اینترنت ناشناس واقعی وجود نداره.
   '''
			bot.reply_to(msg, reply)

		elif username == str(msg.chat.id):

			text = 'اینکه آدم گاهی با خودش حرف بزنه خوبه ، ولی اینجا نمیتونی به خودت پیام ناشناس بفرستی ! :)'
            
			bot.send_message(msg.chat.id, text)
			
		else:
			
			reply = "لینکی که روی آن کلیک کرده اید، وجود ندارد یا منقضی شده است."
			bot.reply_to(msg, reply)
			
	else:
		reply = f'''سلام
من ربات ناشناس هستم ولی بهتره که تو به من اعتماد نکنی
من تمام تلاشم رو میکنم که کمترین اطلاعات ممکنه رو ذخیره کنم اما چه بخوای و چه نخوای مجبورم یه سری چیزا رو ذخیره کنم 

برای اینکه لینک ناشناس خودت رو داشته باشی روی /my_link کلیک کن

'''
		
		github_text = f'''
 برای دیدن کد های این ربات میتونید از این {link_part} استفاده کنید.
	
 💙از مشارکت شما در این پروژه خوشحال میشیم💙
 '''
		
		bot.reply_to(msg, reply)
		bot.send_message(msg.chat.id, github_text, parse_mode='MARKDOWN')


@bot.message_handler(commands=['my_link'])
def my_link(msg):
	link = 'https://t.me/thisanonymousbot?start='
	
	user_hash = blake2b(str(msg.chat.id).encode('utf-8'),digest_size=10).hexdigest()
	
	try:
		insert(msg.chat.id, user_hash)
	except:
		pass

	this_user_link = f'{link}{user_hash}'

	reply = f'''
سلام {msg.from_user.first_name} هستم 👋

لینک زیر رو لمس کن و هر حرفی که تو دلت هست یا هر انتقادی که نسبت به من داری رو با خیال راحت بنویس و بفرست. بدون اینکه از اسمت با خبر بشک پیامت به من میرسه. خودت هم میتونی امتحان کنی و از بقیه بخوای راحت و ناشناس بهت پیام بفرستن، حرفای خیلی جالبی میشنوی!

👇👇👇👇👇👇
{this_user_link} 
 
 '''
	
	bot.reply_to(msg, reply)


@bot.message_handler(content_types=['text'])
def messages(msg):
	markup = InlineKeyboardMarkup()
	markup.row_width = 2

	receiver = process_search(msg.chat.id)
	print(receiver)

	text = f'''
شما یک پیام ناشناس دارید:

{msg.text}
 '''

	answer = InlineKeyboardButton("پاسخ دادن", callback_data=msg.chat.id)
# 	ban = InlineKeyboardButton("مسدود کردن", callback_data="receiver")

	markup.add(answer)

	bot.send_message(msg.chat.id, 'پیام شما ارسال شد.')
	bot.send_message(receiver, text, reply_markup=markup)
	
	delete_process(msg.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
	print(call)
	receiver = str(call.data)
	
	process_hash = blake2b(str(f'{call.from_user.id}{receiver}').encode('utf-8'),digest_size=10).hexdigest()
	in_process(call.from_user.id, receiver, process_hash)

	reply = '''
شما در حال پاسخ دادن به مخاطب خود هستید...

میتونی هر حرفی که دلت میخواد رو بگی ولی سعی کن حواست رو جمع کنی چون تو اینترنت ناشناس واقعی وجود نداره.
   '''
	bot.reply_to(call.message, reply)
	

bot.infinity_polling()
