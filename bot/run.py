from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from session_data import Session

import asyncio
import logging
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

@dp.message(Command('healtcheck'))
async def healtcheck(message: Message):
    await message.answer('Bot is working')

single_loop = False    

session = Session(set_errors = set(), last_open_file = '', line_for_check = 1)

@dp.message(CommandStart()) 
async def start(message: Message):

    # добавляем новый айди
    if not int(message.chat.id) in joinedUsers:
        joinedUsers.add(message.chat.id)
        for err in session.set_errors:
            if not err:
                session.set_errors.remove(err)
            else:
                await send_message(err)

    global single_loop
    if not single_loop:
        single_loop = True
        while True:
            list_of_files = (os.listdir('./logs'))

            n = 0
            for n in range(len(list_of_files)):
                list_of_files[n] = os.path.join('logs', list_of_files[n])
                n += 1

            list_of_files.sort(key=lambda x: os.path.getmtime(x), reverse = True)

            if list_of_files:
                session.new_file(list_of_files[0])
            else:
                await message.answer('File with logs not found')
                break

            while True:
                linecache.checkcache(session.last_open_file)
                line = linecache.getline(session.last_open_file, session.line_for_check)

                if not line:
                    await asyncio.sleep(300)
                    break
                
                full_message = file_check.err(session)

                if full_message:
                    await send_message(full_message)
                    await asyncio.sleep(1)  

                session.line_for_check += 1    
    
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

