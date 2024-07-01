# import asyncio
# import time
# import aiohttp
#
#
# async def fetch(session):
#     async with session.get("https://worldtimeapi.org/api/timezone/Asia/Tashkent") as response:
#         response_json = await response.json()
#         return response_json
#
#
# async def main(n):
#     async with aiohttp.ClientSession() as session:
#         tasks = [fetch(session)] * n
#         return await asyncio.gather(*tasks)
#
#
# before = time.time()
# loop = asyncio.get_event_loop()
# results = loop.run_until_complete(main(5))
#
# print(time.time() - before)
#
# # import requests
# # before = time.time()
# # for i in range(5):
# #     response = requests.get("https://worldtimeapi.org/api/timezone/Asia/Tashkent")
# #     response_json = response.json()
# #
# # print(time.time() - before)
# #


# from asgiref.sync import sync_to_async
# from authentication.models import User
#
#
# async def start(msg):
#     users = await sync_to_async(User.objects.all)()
#     await msg.reply('text')
