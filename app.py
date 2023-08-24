import logging

from config import API_TOKEN, ADMINS
from aiogram import Dispatcher, Bot, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from state import Register, Connection
from keyboards import contact_btn, start_menu, reply_to_btn, backbtn
from sqlite import Database

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Database(path_to_db='main.db')


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Bot ishga tushdi")

        except Exception as err:
            logging.exception(err)


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("help", "Yordam"),
        ]
    )

async def on_startup(dispatcher):
    # Birlamchi komandalar (/start va /help)
    await set_default_commands(dispatcher)

    # Ma'lumotlar bazasini yaratamiz:
    try:
        db.create_table_users()
    except Exception as err:
        print(err)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)




@dp.message_handler(commands=['start'])
async def get_register(message: types.Message, state: FSMContext):
    user_id = message.from_id 
    name = message.from_user.full_name
    
    try:
        db_user_id = db.select_user(Name=name, id=user_id)[0]
        await message.answer(
                text=f"Salom {name}",
                reply_markup=start_menu
            )
    except TypeError:
        await message.answer(
            text=f"Salom {message.from_user.full_name}. Iltimos Telefon raqamingizni ulashing!",
            reply_markup=contact_btn
        )
        await state.update_data(
            {
                'user_id' : user_id,
                'name' : name
            }
        )
        await Register.number.set()


@dp.message_handler(state=Register.number, content_types=types.ContentTypes.CONTACT)
async def get_register_save(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(
        {
            'phone' : phone
        }
    )
    data = await state.get_data()
    id = data.get('user_id')
    name = data.get('name')
    phone = data.get('phone') 
    db.add_user(id, name, phone)
    await message.answer(text='{}\n{}\n{}'.format(id, name, phone), reply_markup=start_menu)

@dp.message_handler(text='📞 Aloqa')
async def get_aloqa(message: types.Message):
    text = 'Telefon raqami: +998905061328\n'
    text += 'Telegram: @thenyuton'
    await message.answer(
        text=text
    )

@dp.message_handler(text='💻Loyihalar')
async def get_aloqa(message: types.Message):
    await message.answer(
        text="Loyihalar hozircha yo'q"
    )

#------------------------------------------------------------------

@dp.callback_query_handler()
async def send_admin(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(
        text="Admin xabaringizni kiriting:"
        )
    await Connection.answer_msg.set()
    await state.update_data(user_id=call.data)

@dp.message_handler(state=Connection.answer_msg, content_types=types.ContentTypes.ANY)
async def send_msg_Admin(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    try:
        await bot.copy_message(
            chat_id=data.get('user_id'), from_chat_id=message.chat.id, 
            message_id=message.message_id, reply_markup=message.reply_markup
        )
        await message.reply("✅Xabar yetkazildi!")
    except:
        await message.reply("❌Xabar yetkazilmadi!")
    await state.reset_state(with_data=True)

@dp.message_handler(text="☕️ Bo'lishish")
async def user_send_message(message: types.Message, state: FSMContext):
    await message.answer(
        "Men bilan ixtiyoriy narsa bo'lishishingiz mumkin. Ularni albatta ko'rib chiqaman.",
        reply_markup=backbtn
    )
    await state.set_state('sendMessage')

@dp.message_handler(state='sendMessage', content_types=types.ContentTypes.ANY)
async def send_msg(message: types.Message, state: FSMContext):
    if message.text=='🔙ortga' and message.text:
        await message.answer(
            text='Endi nima qilamiz?', 
            reply_markup=start_menu
        )
        await state.finish()
    else:
        msg_id = message.chat.id
        await bot.copy_message(
            chat_id=ADMINS[0], from_chat_id=msg_id, 
            message_id=message.message_id,
            reply_markup=reply_to_btn(msg_id)
            )
        await message.answer('✅Xabar yetkazildi!')
        await message.answer(
            text='Endi nima qilamiz?', 
            reply_markup=start_menu
        )
        await state.finish()



if __name__=='__main__':
    executor.start_polling(dp, on_startup=on_startup)
