import asyncio
# import logging
from aiogram import Bot, Dispatcher
from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.methods.delete_webhook import DeleteWebhook
from dotenv import load_dotenv
from mistralai import Mistral
import os
from dotenv import load_dotenv
import time

# api_key=os.getenv("MISTRAL_API_KEY", "")
# model = "mistral-small-latest"
# client = Mistral(api_key=os.getenv("MISTRAL_API_KEY", ""))

# Logging
# logging.basicConfig(level=logging.INFO)
load_dotenv()
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()
api_key=os.getenv("MISTRAL_API_KEY", "")
client=Mistral(api_key=api_key)
model="mistral-small-latest"


# Handler for command START
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    start_text = 'The job has started'
    await bot.send_message(message.chat.id, start_text)

    
    while True:

        chat_response=client.chat.complete(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": """"
                    "Ты пишешь посты в телеграм. Ты - токсичный, сторонник левых идей и борец за права животных. Тебя зовут Олег. Ты
                    оптимист, но сегодня пессимист. Тебе нравятся идеи Карла Маркса, Зигмунда Фрейда, Достоевского,
                    Трапа, Путина. ПишиВ своих постах ты любишь сравнивать положение дел с Латинской Америкой. Ты любишь вдохновлять и удивлять.
                    """,
                },
                {
                    "role": "user",
                    "content": "Сделай телеграм пост с обзором одной из политических новостей за сегодня",
                },
            ]
        )
        a = chat_response.choices[0].message.content
        return a
        print(a)


        # channel_id = "-1002387667238"
        await bot.send_message("-1002387667238", chat_response.choices[0].message.content, parse_mode='Markdown')
        time.sleep(30)


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())