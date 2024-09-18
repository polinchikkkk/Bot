import re
import linecache
from session_data import Session

#функция нахождения флага и текста ошибки
def flag_and_text(line) -> tuple[str, str]:
        search = re.search(r'([A-Z]*):  (.*)', line)
        return search.group(1), search.group(2)
                    
#функция нахождения ошибок
def error(session: Session) -> str:
    err_message = ''
    context_message = ''
    line = linecache.getline(session.last_open_file, session.line_for_check) #получаем строку

    #проверка наличия флага в строке
    if not re.findall(r'[A-Z]*:  ', line):
         return ''

    flag, text = flag_and_text(line=line) #получаем флаг и текст ошибки
    
    #проверка найденного флага
    if flag=='ERROR':
        err_message = text
        session.line_for_check += 1
        
        #цикл нахождения контекста 
        while True:
            if re.findall(r'[A-Z]*:  ', linecache.getline(session.last_open_file, session.line_for_check)):
                flag, text = flag_and_text(line=linecache.getline(session.last_open_file, session.line_for_check))

                #если нашли флаг контекста, сохранияем текст контекста
                if flag == 'CONTEXT':
                    context_message += text
                    session.line_for_check += 1
                    break

            session.line_for_check += 1

        #сохранияем текст контекста до тех пор, пока не будет найден новый флаг
        while not re.findall(r'[A-Z]*:  ', linecache.getline(session.last_open_file, session.line_for_check)):
            context_message += linecache.getline(session.last_open_file, session.line_for_check)
            if not linecache.getline(session.last_open_file, session.line_for_check+1): #проверка на пустую строку после контекста
                break
            session.line_for_check += 1
            

        #возвращаем сообщение об ошибке, если она найдена, иначе пустое сообщение
        full_message = err_message + "\n" + context_message

        return full_message
    else:
        return ''

#функция обработки ошибки
def err(session: Session) -> str:
     
    full_message = error(session) #вызов функции нахождения ошибки

    #проверка наличия одинаковых ошибок
    if full_message in session.set_errors:
        full_message = ''
    
    #проверка пустого сообщения, занесение новой ошибки в сет
    if full_message:
        session.set_errors.add(full_message)
        return full_message   





 



        