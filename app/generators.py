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


async def gpt_embed(req):
    load_dotenv()
    async with Mistral(
        api_key=os.getenv("MISTRAL_API_KEY", ""),
    ) as mistral:
        try:
            completion = await mistral.embeddings.create_async(
                model="mistral-embed",
                inputs=[req]
            )
            embedding = completion.data[0].embedding
            print(f"Сгенерирован вектор длиной: {len(embedding)}")
            return embedding
        except Exception as e:
            raise Exception(f"Ошибка в gpt_embed: {str(e)}")



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

# asyncio.run(gpt_text('Запрос'))
# asyncio.run(gpt_embed('Запрос'))