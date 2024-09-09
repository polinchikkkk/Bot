import re
import linecache
from aiogram import Bot


bot = Bot(token = '7320431304:AAFJbGLzwDlGIw6hxag_lOSv3HgJJ_2gL4U')


async def send_message(id: int, text: str):
    await bot.send_message(id, text)


async def WARNING(path, line_for_check, line, id):
    match1 = re.search(r'WARNING', line)
    if match1:
        line_for_check += 2
        line = linecache.getline(path, line_for_check)
        await send_message(id, line.strip())
        line_for_check += 1
    return line_for_check    
    

async def ERROR(path, line_for_check, line, id):
    match2 = re.search(r'ERROR', line)
    FullContext = ''        
    if match2:
        while True:
            line_for_check += 1
            Context = linecache.getline(path, line_for_check)
            match4 = re.search(r'CONTEXT', Context)
            if match4:
                while True:
                    line_for_check += 1
                    Part_of_Context = linecache.getline(path, line_for_check)
                    match5 = re.search(r'LOG', Part_of_Context)
                    match6 = re.search(r'STATEMENT', Part_of_Context)
                    if match5 or match6: 
                        break
                    else:
                        FullContext = FullContext + Part_of_Context.strip()
                break 
        await send_message(id, line.strip() + '\n' + Context.strip() + '\n' + FullContext.strip())
    return line_for_check    
       
                        

async def FATAL(line, id):
    match3 = re.search(r'FATAL', line)                                  
    if match3:
        await send_message(id, line.strip())    

    
        

        