from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

contact_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📞Telefon raqamni ulashish', request_contact=True)
        ]
    ],
    resize_keyboard=True
)

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="☕️ Bo'lishish"),
            KeyboardButton(text="📞 Aloqa")
        ],
        [
            KeyboardButton(text="💻Loyihalar")
        ],
    ],
    resize_keyboard=True
)

def reply_to_btn(message_id):
    reply_btn = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text='🖋Reply to Message', callback_data=message_id)
    reply_btn.add(button)
    return reply_btn

backbtn = ReplyKeyboardMarkup(resize_keyboard=True)
btn = KeyboardButton(text='🔙ortga')
backbtn.insert(btn)