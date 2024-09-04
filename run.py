from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message


import asyncio
import logging
import re
import time
import os

bot = Bot(token = '7282726810:AAHjJXz0-B1qmKVkN-WiPiIZEr3_J643bn0')
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):

    while True:
        await message.answer('Start verification')
    
        list_of_files = os.listdir('./logs')
        list_of_files.reverse()
    
        await message.answer(f'Open file: ' + list_of_files[0])
        path = os.path.join('logs', list_of_files[0])

        file = open(path, 'r')
        while True:
          line = file.readline()
          match = re.search(r'WARNING', line)
          if match:
              await message.answer(f'Error is found:')
              await message.answer(line.strip())
              time.sleep(60) 
          if not line:
            file.close()
          
            
    
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
