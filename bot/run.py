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

        list_of_files = [file for file in os.listdir('./logs')]
        # list_of_files.reverse()

        last_open_file = 'fpogjdk'
        

        if last_open_file != list_of_files[0]:
            last_open_file = list_of_files[0]
            line_for_check = 0
        

        await message.answer(f'Open file: {last_open_file}')

        path = os.path.join('logs', last_open_file)

        # Имя файла источника
        list_of_files.reverse()
        src_file_name = list_of_files[0]
        path2 = os.path.join('logs', src_file_name)

        file = open(path, 'r')

        while True:

            with open(path2, 'r') as src_file:
                src_lines = src_file.readlines()

            for line in src_lines:
                with open(path, 'a') as dst_file:
                    dst_file.write(line + '\n')

                time.sleep(1)
            
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

