from datetime import datetime, timezone
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from emojis import encode
from requests import get
import json
import requests
import aiogram
from config import TOKEN
from getLikersVKfinal import hashtag
from getLikersVKfinal import getPostsToLike
from getLikersVKfinal import translateToID
from getLikersVKfinal import tryGettingPage
from config import access_token


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

lang = "eng"
greetings = encode(
    'Привет! :muscle: Я помогаю получать взаимные лайки на посты, для того чтобы получить заветный хэштэг, который можно указать в посте и все остальные смогут его пролайкать, нужно будет лайкнуть другие участвующие в задании посты. Если готовы, то начнем: нажмите кнопку /получить_тэг')
s = requests.Session()

addChannelButton = "/получить_тэг"

button1 = KeyboardButton(addChannelButton)
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_kb.add(button1)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(greetings, reply_markup=greet_kb)


@dp.message_handler(commands=['получить_тэг'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id, "напишите свой id или короткое имя аккаунта, с которого будете лайкать посты участников\nПример: 123451234\nПример: myshortname")


# @dp.message_handler(commands=['help'])
# async def process_start_command(message: types.Message):
#     await bot.send_message(message.from_user.id, "Bot will recognize only existing channels id's. If you don't receive an answer that means bot haven't found this channel in public web")

@dp.message_handler()
async def process_start_command(message: types.Message):
    # обработка случая с числовым id
    if message.text.isdigit():
        userObj = tryGettingPage(message.text, access_token)
        if len(userObj['response']) == 0:
            await bot.send_message(message.from_user.id, encode("пришлите, пожалуйста, ваш действующий id :no_mouth:\nмне нужны только его цифры, либо ваше короткое имя без @"))
        elif userObj['response'][0]['first_name'] == 'DELETED':
            await bot.send_message(message.from_user.id, encode("пришлите, пожалуйста, ваш действующий id :no_mouth:\nмне нужны только его цифры, либо ваше короткое имя без @"))
        else:
            arrayOfPosts = getPostsToLike(int(message.text))
            if len(arrayOfPosts) == 0:
                await bot.send_message(message.from_user.id, encode(f"все пролайкано! :white_check_mark:\nдержи тэг: #{hashtag}\nрекомендую добавить и другие тэги(#лайки #новое #взаимно #абсолютно #классный),чтобы нечестные пользователи не получали лайки ничего не лайкнув:innocent:"))
            else:
                await bot.send_message(message.from_user.id, f"пролайкай следующие посты и я дам тэг, с которым ты получишь лайки!")
                a = ""
                for element in arrayOfPosts:
                    a += f"{element}\n"
                await bot.send_message(message.from_user.id, a)
    else:
        # обработка случая с коротким именем пользователя
        # await bot.send_message(message.from_user.id, encode("пришлите, пожалуйста, ваш id :no_mouth:\nмне нужны только его цифры, либо ваше короткое имя без @"))
        id = translateToID(message.text, access_token)
        if id == None:
            await bot.send_message(message.from_user.id, encode("пришлите, пожалуйста, ваш действующий id :no_mouth:\nмне нужны только его цифры, либо ваше короткое имя без @"))
        else:
            arrayOfPosts = getPostsToLike(int(id))
            if len(arrayOfPosts) == 0:
                await bot.send_message(message.from_user.id, encode(f"все пролайкано! :white_check_mark:\nдержи тэг: #{hashtag}\nрекомендую добавить и другие тэги(#лайки #новое #взаимно #абсолютно #классный),чтобы нечестные пользователи не получали лайки ничего не лайкнув:innocent:"))
            else:
                await bot.send_message(message.from_user.id, encode(f"пролайкай следующие посты и я дам тэг :trophy:, с которым ты получишь лайки!"))
                a = ""
                for element in arrayOfPosts:
                    a += f"{element}\n"
                await bot.send_message(message.from_user.id, a)


if __name__ == "__main__":

    executor.start_polling(dp)
