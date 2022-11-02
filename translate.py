import aiogram
from flask import  Flask , json ,  request
import config as cfg
from googletrans import Translator
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
    
TOKEN = '5779185522:AAHbsYLJoyzLZQ6ORsgHWFqxWdLqKg0TbIY'

class LangSetting:
    lang = 'ru'
    @classmethod
    def change_lang(cls, lang):
        cls.lang = lang
a = 0
keyss = []
keyb = InlineKeyboardMarkup()
for i, j in cfg.LANGDICT.items():
    # print(f'Ключ : {i}')
    # print(f'значения : {j}')
    key = InlineKeyboardButton(j, callback_data=i)
    keyss.append(key)
    a+= 1;
    if a == 3:
        a = 0
        keyb.add(keyss[0], keyss[1], keyss[2] )
        keyss = []

bot = aiogram.Bot(TOKEN)
dp = aiogram.Dispatcher(bot)
translater = Translator()

@dp.message_handler(commands=['start'])
async def message_start(message) :
    await bot.send_message(message.chat.id, f'<strong>Привет я бот переводчик \nВыберите язык на какой хотите перевести с помощью команды /choose \n</strong>' , parse_mode='html' )
    
@dp.message_handler(commands=['choose'])
async def process_start_command(message: aiogram.types.Message):
    await message.reply('Выбери язык', reply_markup=keyb)

@dp.callback_query_handler()
async def process_callback_kb1btn1(callback_query: aiogram.types.CallbackQuery ):
        if callback_query.data in cfg.LANGUES:
            lang = callback_query.data
            LangSetting.change_lang(lang=lang)
            val = (lang, str(callback_query.from_user.id))
            await bot.send_message(callback_query.from_user.id, f"<strong>Вы выбрали {cfg.LANGDICT[lang]}\nВведите слово для перевода</strong>" , parse_mode='html' )
            
@dp.message_handler() 
async def message_trans(message):
    lang = LangSetting.lang
    if message.text == translater.translate(f'{message.text}', dest=f'{lang}').text:
     await message.reply(translater.translate(f'{message.text}', dest=f'ru').text)
    else :
     await message.reply(translater.translate(f'{message.text}' , dest=f'{lang}').text)
    
if __name__ == '__main__':
    aiogram.executor.start_polling(dp)
    
    
    