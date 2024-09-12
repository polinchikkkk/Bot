from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message


import asyncio
import logging
import time
import os
import linecache
import file_check

bot = Bot(token = '7320431304:AAFJbGLzwDlGIw6hxag_lOSv3HgJJ_2gL4U')
dp = Dispatcher()

async def send_message(id: int, text: str):
        await bot.send_message(id, text)

@dp.message(CommandStart())
async def start(message: Message):
 
    id = message.chat.id
    
    while True:
        await message.answer('Start verification')

        list_of_files = (os.listdir('./logs'))

        n = 0
        for n in range(len(list_of_files)):
            list_of_files[n] = os.path.join('logs', list_of_files[n])
            n += 1

        list_of_files.sort(key=lambda x: os.path.getmtime(x), reverse = True)

        last_open_file = 'fpogjdk'

        if len(list_of_files) < 0:
            break
        else:
            if last_open_file != list_of_files[0]:
                last_open_file = list_of_files[0]
                line_for_check = 0        
        

        await message.answer(f'Open file: {last_open_file}')

        path = last_open_file

        file = open(path, 'r')

        while True:
            
            line = file.readline()

            if not line:
                file.close()
                time.sleep(300)
                break


            line = linecache.getline(path, line_for_check)


            line_for_check, full_message = file_check.err(path, line_for_check)

            if full_message:
                await send_message(id, full_message)
                await asyncio.sleep(1)  

            line_for_check += 1    




    
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')

