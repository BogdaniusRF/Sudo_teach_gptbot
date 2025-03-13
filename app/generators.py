import asyncio
from mistralai import Mistral
import os
from dotenv import load_dotenv

async def gpt_text(req):
    load_dotenv()
    async with Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    ) as mistral:

        completion = await mistral.chat.complete_async(model="mistral-small-latest", messages=[
            {
                "role": "user",
                "content": req,
            },
        ], stream=False)

        # Handle response
        return completion.choices[0].message.content
        print(completion.choices[0].message.content)



# async def get_horoscope(req):
#     load_dotenv()
#     async with Mistral(
#         api_key=os.getenv("MISTRAL_API_KEY", ""),
#     ) as mistral:

#         completion = await mistral.chat.complete_async(model="mistral-small-latest", messages=[
#             {
#                 "content": "system",
#                 "role": '''твоя задача распарсить сообщение и достать из сообщения город, дату и время рождения.
#                  Вывести информацию в формате: Город: Дата рождения: Время рождения:''',
#             },
#                 "role": "user",
#                 "content": req

#         ], stream=False)

#         # Handle response
#         return completion.choices[0].message.content

asyncio.run(gpt_text('Сделай телеграм пост с обзором одной из политических новостей за сегодня?'))