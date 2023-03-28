from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import data
import Process
import json
from imaplib import IMAP4, IMAP4_SSL
from aiogram.utils.callback_data import CallbackData
import email

bot = Bot(token=data.token)
dp = Dispatcher(bot)
idcnt1 = 0
remad = []
br = False


@dp.message_handler(commands="start")
async def start(message: types.message):
    data.chat_id = message.chat.id
    start_buttons = ['Email.ru', 'Parse NFT']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.clean()
    keyboard.add(*start_buttons)
    await message.answer('Maybe here will be a description', reply_markup=keyboard)

cb = CallbackData("post", "id")

async def ans_print(message, num):
    global idcnt1, cb

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Details", callback_data=cb.new(id=idcnt1)))
    await message.answer(f"Email: {get[str(num)]['address']}\n"
                     f"Password: {get[str(num)]['email_pas']}", reply_markup=keyboard)

    remad.append(num)
    idcnt1 += 1

@dp.message_handler(Text(equals='Parse NFT'))
async def parsenft(message: types.message):
    buttons = ['Open Sea']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.clean()
    keyboard.add(*buttons)
    await message.answer('Which site do you want to parse?')

@dp.message_handler(Text(equals='Open Sea'))
async def openseaa(message: types.message):
    site = []


@dp.message_handler(Text(equals='Email.ru'))
async def emailru(message: types.message):
    start_buttons = ['Parse New Post', 'Clear Post']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.clean()
    keyboard.add(*start_buttons)
    await message.answer('Only the email button is available.', reply_markup=keyboard)

@dp.message_handler(Text(equals='Clear Post'))
async def delete_post(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.clean()
    keyboard.add('Cancel')
    await message.answer("This might take a while... We will inform you when the process finishes.", reply_markup=keyboard)
    global br
    for num in range(0, len(get)):
        if br:
            br = False
            break
        address, imap_pas = get[str(num)]['address'], get[str(num)]['imap']
        Process.delete_all(address, imap_pas)

    await message.answer("All cleared!")

@dp.message_handler(Text(equals='Parse New Post'))
async def parse_post(message: types.Message):
    clarify_buttons = ['From address', 'Key words', 'New']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.clean()
    keyboard.add(*clarify_buttons)
    await message.answer('How to get one for you?', reply_markup=keyboard)

@dp.message_handler(Text(equals='From address'))
async def add_custom(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.clean()
    keyboard.add('Cancel')
    await message.answer("For which address do you want us to look for?", reply_markup=keyboard)

    @dp.message_handler()
    async def echo_message(msg: types.Message):
        await msg.answer("This might take a while... We will inform you when the process finishes.")
        look = msg.text
        cnt = 0
        global idcnt1, br

        for num in range(0, len(get)):
            if br:
                br = False
                break
            address, imap_pas = get[str(num)]['address'], get[str(num)]['imap']
            vec = Process.find_from(address, imap_pas, look, num)
            if len(vec) != 0:
                await ans_print(msg, num)
                cnt += 1

        await msg.answer(f"The search has finished, {cnt} letters have been found.")

        await start(message)

@dp.message_handler(Text(equals='Key words'))
async def add_custom(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.clean()
    keyboard.add('Cancel')
    await message.answer("For which key word do you want us to look for?", reply_markup=keyboard)

    @dp.message_handler()
    async def echo_message(msg: types.Message):
        await msg.answer("This might take a while... We will inform you when the process finishes.")
        look = msg.text
        cnt = 0
        global idcnt1, br

        for num in range(0, len(get)):
            if br:
                br = False
                break
            address, imap_pas = get[str(num)]['address'], get[str(num)]['imap']
            vec = Process.find_by_key(address, imap_pas, look, num)
            if len(vec) != 0:
                await ans_print(msg, num)
                cnt += 1
                cnt += 1

        await msg.answer(f"The search has finished, {cnt} letters have been found.")

        await start(message)

@dp.message_handler(Text(equals='New'))
async def add_custom(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.clean()
    keyboard.add('Cancel')
    await message.answer("This might take a while... We will inform you when the process finishes.", reply_markup=keyboard)
    cnt = 0
    global idcnt1, br

    for num in range(0, len(get)):
        if br:
            br = False
            break
        address, imap_pas = get[str(num)]['address'], get[str(num)]['imap']
        vec = Process.find_new(address, imap_pas, num)
        if len(vec) != 0:
            await ans_print(message, num)
            cnt += 1

    await message.answer(f"The search has finished, {cnt} letters have been found.")

    await start(message)

@dp.callback_query_handler(cb.filter())
async def send_random_value(call: types.CallbackQuery, callback_data: dict):
    x = remad[int(callback_data["id"])]
    repl = ''
    boxes = ["Inbox", '"&BB4EQgQ,BEAEMAQyBDsENQQ9BD0ESwQ1-"', '"&BCEEPwQwBDw-"', '"INBOX/Newsletters"']
    imap = IMAP4_SSL('imap.mail.ru')
    try:
        imap.login(get[str(x)]["address"], get[str(x)]["imap"])
    except:
        await call.message.answer(f'Sorry, the address has been blocked, consider restoring it\n'
                                  f'Address: {get[str(x)]["address"]}\n'
                                  f'Password: {get[str(x)]["email_pas"]}')
        return
    cntres = 0
    for box in boxes:
        imap.select(box)
        _, msum = imap.search(None, 'ALL')

        for num in msum[0].split():
            cntres += 1
            _, data = imap.fetch(num, "(RFC822)")

            message = email.message_from_bytes(data[0][1])

            number = str(num).replace("'", '').replace('b', '')
            mes = str(message.get('From')).split(' ')
            retansw = ''
            for y in mes:
                if '?' in y: continue
                retansw += (y + " ")

            repl += f"{number}. {retansw}\n"

    imap.close()
    imap.logout()

    repl = f"{cntres} letters in the box\n\n" + repl

    await call.message.answer(repl)


@dp.message_handler(Text(equals='Cancel'))
async def canc(message: types.Message):
    global br
    br = True
    print(1)


if __name__ == "__main__":
    with open("DB_tmp.json") as file:
        get = json.load(file)

    executor.start_polling(dp)



