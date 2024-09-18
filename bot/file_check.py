import re
import linecache
from session_data import Session

#функция нахождения флага и текста ошибки
def id_flag_text(line) -> tuple[str, str, str]:
        search = re.search(r'\[(\d+)\].* ([A-Z]+):  (.+)', line)
        return search.group(1), search.group(2), search.group(3)
                    
#функция нахождения ошибок
def error(session: Session) -> str:
    err_message = ''
    context_message = ''
    line = linecache.getline(session.last_open_file, session.line_for_check) #получаем строку

    #проверка наличия флага в строке
    if not re.findall(r'[A-Z]*:  ', line):
         return ''

    id, flag, text = id_flag_text(line=line) #получаем флаг и текст ошибки
    
    # в случае дебага выводим сообщение в консоль
    if session.debug:
        # print(f"error: id: {id}, flag: {flag}, text: {text}")
        pass
    
    #проверка найденного флага
    if flag=='ERROR':
        err_id = id
        err_message = text
        session.line_for_check += 1
        id, flag, text = id_flag_text(line=linecache.getline(session.last_open_file, session.line_for_check))
        #проверка на наличие контекста по айди

        context = False
        
        #цикл нахождения контекста 
        while True:
            if id != err_id:
                return err_message

            if re.findall(r'[A-Z]*:  ', linecache.getline(session.last_open_file, session.line_for_check)):
                id, flag, text = id_flag_text(line=linecache.getline(session.last_open_file, session.line_for_check))

                #если нашли флаг контекста, сохранияем текст контекста
                if flag == 'CONTEXT':
                    context = True
                    context_message += text
                    session.line_for_check += 1
                    break

            session.line_for_check += 1

        #сохранияем текст контекста до тех пор, пока не будет найден новый флаг
        while context:
            line = linecache.getline(session.last_open_file, session.line_for_check)
            #проверка на пустую строку после контекста и на наличие флага в строке
            if not line or re.findall(r'[A-Z]*:  ', line):
                break
            
            context_message += line
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





 



        