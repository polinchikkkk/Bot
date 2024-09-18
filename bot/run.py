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

#добавляю из файла айди в сет 
joinedUsers = set ()
with open('bot/users.txt', 'r') as file:
    for line in file:  
        if line.strip().isnumeric():
            joinedUsers.add(int(line.strip()))

#функция рассылки сообщений пользователям по айди из сета
async def send_message(text: str):
    for user in joinedUsers:
        await bot.send_message(chat_id = user, text = text)

#функция для вывода сообщения о том, что бот работает, пишет только пользователю, который написал healtcheck
@dp.message(Command('healtcheck'))
async def healtcheck(message: Message):
    await message.answer('Bot is working')

single_loop = False    

#создаем сессию
session = Session(set_errors = set(), last_open_file = '', line_for_check = 1)

@dp.message(CommandStart()) 
async def start(message: Message):

    #рассылка ошибок из сета новым позьвателям и проверка на пустой элемент в сете
    if not int(message.chat.id) in joinedUsers:
        joinedUsers.add(message.chat.id)
        for err in session.set_errors:
            if not err:
                session.set_errors.remove(err)
            else:
                await send_message(err)

    #запуск цикл с нахождением файла, ошибок и тд, также проверка на единичный запуск цикла
    global single_loop
    if not single_loop:
        single_loop = True

        #цикл нахождения нужного файла с ошибками
        while True:
            list_of_files = (os.listdir('./logs')) #получем неупорядоченный список названия файлов из папки logs

            #цикл получения путей файлов из их названий и занесение в список
            for n in range(len(list_of_files)):
                list_of_files[n] = os.path.join('logs', list_of_files[n])

            list_of_files.sort(key=lambda x: os.path.getmtime(x), reverse = True) #сортировка по времени изменения в порядке убывания

            #проверка последнего найденного файла на совпадение с предыдущем файлом для проверки, проверка на пустой список с файлами
            if list_of_files:
                session.new_file(list_of_files[0])
            else:
                await message.answer('File with logs not found') 
                break


            await message.answer('new file:' + session.last_open_file)
            await message.answer('line for check = ' + str(session.line_for_check))

            #обновление файла для проверки
            linecache.checkcache(session.last_open_file)

            #цикл нахождений ошибок и вывода сообщений об этом
            while True:
                line = linecache.getline(session.last_open_file, session.line_for_check) #получаем строку файла

                #если полученная строка пустая, засыпаем и выходим из цикла, ищем снова последний измененный файл
                if not line:
                    await message.answer('file close')
                    await asyncio.sleep(30)
                    break
                
                full_message = file_check.err(session) #получаем сообщение об ошибке 

                #проверка сообщения об ошибке
                if full_message:
                    await send_message(full_message)
                    await asyncio.sleep(1)  

                session.line_for_check += 1 #итерация строк файла   
    
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        #записываем новые айди в файл
        with open('bot/users.txt', 'w') as file: 
            for id in joinedUsers:
                file.write(str(id) + '\n')
        print('Exit')

