from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton

def pay_button():
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton("To'lov qilish",callback_data="pay")
    markup.add(btn)
    return markup

