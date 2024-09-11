import re
import linecache


# def WARNING(path, line_for_check):
#     line = linecache.getline(path, line_for_check)
#     match1 = re.search(r'WARNING', line)
#     full_message = ''
#     if match1:
#         line_for_check += 2
#         line = linecache.getline(path, line_for_check)
#         full_message = line
#         line_for_check += 1
#     return line_for_check, full_message   
    


# def ERROR(path, line_for_check):
#     line = linecache.getline(path, line_for_check)
#     match2 = re.search(r'ERROR', line)
#     FullContext = ''
#     full_message = ''      
#     if match2:
#         while True:
#             line_for_check += 1
#             Context = linecache.getline(path, line_for_check)
#             match4 = re.search(r'CONTEXT', Context)
#             if match4:
#                 while True:
#                     line_for_check += 1
#                     Part_of_Context = linecache.getline(path, line_for_check)
#                     match5 = re.search(r'LOG', Part_of_Context)
#                     match6 = re.search(r'STATEMENT', Part_of_Context)
#                     if match5 or match6: 
#                         break
#                     else:
#                         FullContext = FullContext + Part_of_Context.strip()
#                 break 
#         full_message = line.strip() + '\n' + Context.strip() + '\n' + FullContext.strip()
#     return line_for_check, full_message   
       
                        

# def FATAL(path, line_for_check):
#     line = linecache.getline(path, line_for_check)
#     match3 = re.search(r'FATAL', line) 
#     full_message = ''                               
#     if match3:
#         full_message = line.strip()
#     return line_for_check, full_message     



def flag_and_text(line) -> tuple[str, str]:
        search = re.search(r'([A-Z]*):  (.*)', line)
        return search.group(1), search.group(2)
                    


def error(path: str, line_for_check: int) -> tuple[int, str]:
    err_message = ''
    context_message = ''
    line = linecache.getline(path, line_for_check)

    if not re.findall(r'[A-Z]*:  ', line):
        # Если в этой строке нет никакого флага, то мы пропускаем ее и переходим на следующую
         return line_for_check+1, ''

    flag, text = flag_and_text(line=line)
    
    if flag=='ERROR':
        err_message = text
        line_for_check += 1

        
        while True:
            # ищем строку где есть какой нибудь флаг
            if re.findall(r'[A-Z]*:  ', linecache.getline(path, line_for_check)):
                flag, text = flag_and_text(line=linecache.getline(path, line_for_check))

                if flag == 'CONTEXT':
                    context_message += text
                    line_for_check += 1
                    break

            line_for_check += 1

        # пока в нашей строке нет флага, значит это все относится к контексту
        while not re.findall(r'[A-Z]*:  ', linecache.getline(path, line_for_check)):
            context_message += linecache.getline(path, line_for_check)
            line_for_check += 1

        full_message = err_message + "\n" + context_message

        return line_for_check, full_message
    else:
        return line_for_check+1, ''
    


def warning(path: str, line_for_check: int) -> tuple[int, str]:
    err_message = ''
    context_message = ''
    line = linecache.getline(path, line_for_check)

    if not re.findall(r'[A-Z]*:  ', line):
        # Если в этой строке нет никакого флага, то мы пропускаем ее и переходим на следующую
         return line_for_check+1, ''

    flag, text = flag_and_text(line=line)
    
    if flag=='WARNING':
        err_message = text
        line_for_check += 2
        while True:
            # ищем строку где есть какой нибудь флаг
            if re.findall(r'[A-Z]*:  ', linecache.getline(path, line_for_check)):
                flag, text = flag_and_text(line=linecache.getline(path, line_for_check))

                if flag == 'WARNING':
                    context_message += text
                    line_for_check += 1
                    break
        line_for_check += 1

        full_message = err_message + "\n" + context_message

        return line_for_check, full_message
    else:
        return line_for_check+1, ''



def fatal(path: str, line_for_check: int) -> tuple[int, str]:
    full_message = ''
    line = linecache.getline(path, line_for_check)

    if not re.findall(r'[A-Z]*:  ', line):
        # Если в этой строке нет никакого флага, то мы пропускаем ее и переходим на следующую
         return line_for_check+1, ''

    flag, text = flag_and_text(line=line)
    
    if flag=='FATAL':
        full_message = text
        line_for_check += 1 
       
        return line_for_check, full_message
    else:
        return line_for_check+1, ''


set_errors = set()

def err(path_, line_for_check_):
     
    line_for_check, full_message = error(path = path_, line_for_check = line_for_check_)

    
    if full_message in set_errors:
        full_message = ''
    else:
        set_errors.add(full_message)

    
    if not full_message:
        line_for_check, full_message = warning(path = path_, line_for_check = line_for_check_)


        if full_message in set_errors:
            full_message = ''
        else:
            set_errors.add(full_message)

        

        if not full_message:
            line_for_check, full_message = fatal(path = path_, line_for_check = line_for_check_)
 

            if full_message in set_errors:
                full_message = ''
            else:
                set_errors.add(full_message)

    return line_for_check, full_message    





 



        