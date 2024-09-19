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
        context = False
        
        #цикл нахождения контекста 
        while True:
            session.line_for_check += 1
            line = linecache.getline(session.last_open_file, session.line_for_check)

            if not line: 
                return err_message

            if re.findall(r'[A-Z]*:  ', line):
                id, flag, text = id_flag_text(line=line)

                if id != err_id:
                    # session.line_for_check -= 1 #если нет контекста, мы откатываемся к предыдущей строке, чтобы не потерять строку
                    return err_message

                #если нашли флаг контекста, сохранияем текст контекста
                if flag == 'CONTEXT':
                    context = True
                    context_message += text
                    break




        #сохранияем текст контекста до тех пор, пока не будет найден новый флаг
        while context:
            session.line_for_check += 1

            line = linecache.getline(session.last_open_file, session.line_for_check)
            #проверка на пустую строку после контекста и на наличие флага в строке
            if not line or re.findall(r'[A-Z]*:  ', line):
                break
            
            context_message += line
            

        #возвращаем сообщение об ошибке, если она найдена, иначе пустое сообщение
        full_message = err_message + "\n" + context_message


        return full_message
    else:
        return ''

#функция обработки ошибки
def err(session: Session) -> str:
    full_message = error(session) #вызов функции нахождения ошибки

    #проверка наличия одинаковых ошибок
    if full_message:
        if full_message not in session.set_errors:
            session.set_errors.add(full_message)
            return full_message   

    else:
        session.line_for_check += 1

    return ''





 



        