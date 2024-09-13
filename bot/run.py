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

# запись айди из файла в сет
joinedFile = open('bot/users.txt', 'r')
joinedUsers = set ()
for line in joinedFile:  
    if line.strip().isnumeric():
        joinedUsers.add(int(line.strip()))
joinedFile.close()


# рассылка сообщений всем пользователям по айди из документа
async def send_message(text: str):
    for user in joinedUsers:
        await bot.send_message(chat_id = user, text = text)

single_loop = False            

@dp.message(CommandStart())
async def start(message: Message):


    # добавляем новый айди
    if not str(message.chat.id) in joinedUsers:
        joinedUsers.add(message.chat.id)

    global single_loop
    if not single_loop:
        single_loop = True
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
                await message.answer('File with logs not found')
                break
            else:
                if last_open_file != list_of_files[0]:
                    last_open_file = list_of_files[0]
                    line_for_check = 0
                    set_errors = set() # решила для каждого нового файла обновлять сет
        

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


                line_for_check, full_message, set_errors = file_check.err(path, line_for_check, set_errors)

                if full_message:
                    await send_message(full_message)
                    await asyncio.sleep(1)  

                line_for_check += 1    

    
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        with open('bot/users.txt', 'w') as file: 
            for id in joinedUsers:
                file.write(str(id) + '\n')
        print('Exit')

