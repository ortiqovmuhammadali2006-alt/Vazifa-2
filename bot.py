from telebot import TeleBot
from telebot.types import Message,CallbackQuery,LabeledPrice,PreCheckoutQuery,ShippingAddress,ShippingOption,ShippingQuery
from buttons import pay_button


TOKEN = "7032898916:AAGQEZ5_CxicJKgKym5hy1F0Acf77VUx6ZQ"
CLICK_PRIVODER_TOKEN = "398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065"

bot = TeleBot(TOKEN,parse_mode="html")

iPhone = [
    {"id" : 1, "name" : "iPhone 11","price" : 200 ,"quantity" : 20},
    {"id" : 2, "name" : "iPhone 11 pro","price" : 250 ,"quantity" : 10},
    {"id" : 3, "name" : "iPhone 12","price" : 300 ,"quantity" : 15},
    {"id" : 4, "name" : "iPhone 13 pro","price" : 400 ,"quantity" : 20},
    {"id" : 5, "name" : "iPhone 14 pro max","price" : 600 ,"quantity" : 15},
]


@bot.message_handler(commands=["start"])
def reaction_to_start(message: Message):
    chat_id = message.chat.id

    bot.send_message(
        chat_id,
        "🛒 <b>BUYURTMANGIZ TAYYOR!</b>\n\n"
        "📱 <b>Tanlangan mahsulotlar:</b>\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "💳 To''lovni davom ettirish uchun pastdagi oynani tasdiqlang 👇",
        reply_markup=pay_button(),
        parse_mode="HTML"
    )

@bot.callback_query_handler(func=lambda call: call.data == "pay")
def reaction_to_pay(call: CallbackQuery):

    chat_id = call.message.chat.id

    prices = []
    total = 0

    for phone in iPhone:
        summa = phone["price"] * phone["quantity"] * 100
        total += summa
        prices.append(
            LabeledPrice(
                f'{phone["name"]} × {phone["quantity"]}',
                summa
            )
        )



    bot.send_invoice(
        chat_id=chat_id,
        title="🍎 Apple Store",
        description="iPhone buyurtmasi uchun to''lov",
        invoice_payload="iphone_order_001",
        provider_token=CLICK_PRIVODER_TOKEN,
        currency="UZS",
        prices=prices,
        photo_url="https://dleel.com/en/blog/iPhone-13-price-and-specifications/a-890002549?srsltid=AfmBOoogWpewGxpiziuCCZvOZhCR5Z9F6AM4DYss7Ux4gP21HR_bJlQw",
        need_name=True,
        need_phone_number=True,
        need_shipping_address=True,
        is_flexible=True
    )




@bot.pre_checkout_query_handler(func=lambda precheckout: True)
def precheckout_handler(precheckout:PreCheckoutQuery):
    
    bot.answer_pre_checkout_query(precheckout.id,ok=True)

@bot.shipping_query_handler(func=lambda shipping_query: True)
def reaction_to_shipping_query(shipping_query: ShippingQuery):

    city = ShippingOption("city", "🚚 Shahar ichida yetkazib berish")
    city.add_price(LabeledPrice("Yetkazib berish", 30000 * 100))

    village = ShippingOption("village", "🚛 Qishloq hududiga")
    village.add_price(LabeledPrice("Yetkazib berish", 50000 * 100))

    get_away = ShippingOption("pickup", "🏬 Do'kondan olib ketish")
    get_away.add_price(LabeledPrice("Olib ketish", 0))

    shipping_options = [city, village, get_away]

    bot.answer_shipping_query(
        shipping_query.id,
        ok=True,
        shipping_options=shipping_options
    )

@bot.message_handler(content_types=["successful_payment"])
def reaction_to_successful_payment(message: Message):
    payment = message.successful_payment

    bot.send_message(
        message.chat.id,
        "🎉 <b>TABRIKLAYMIZ!</b>\n\n"
        "✅ <b>To''lov muvaffaqiyatli amalga oshirildi</b>\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"💰 <b>Umumiy summa:</b> {payment.total_amount // 100:,} som\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "📦 Buyurtmangiz qabul qilindi va tez orada yetkazib beriladi.\n"
        "📞 Operatorimiz siz bilan bog''lanadi.\n\n"
        "🙏 <b>Xaridingiz uchun rahmat!</b>\n"
        "🍎 Apple Store jamoasi",
        parse_mode="HTML"
    )






if __name__ == "__main__":
    print("✅ Bot ishga tushdi")
    bot.infinity_polling()