import re
import linecache


def flag_and_text(line) -> tuple[str, str]:
        search = re.search(r'([A-Z]*):  (.*)', line)
        return search.group(1), search.group(2)
                    


def error(path: str, line_for_check: int) -> tuple[int, str]:
    err_message = ''
    context_message = ''
    line = linecache.getline(path, line_for_check)

    if not re.findall(r'[A-Z]*:  ', line):
         return line_for_check, ''

    flag, text = flag_and_text(line=line)
    
    if flag=='ERROR':
        err_message = text
        line_for_check += 1

        
        while True:
            if re.findall(r'[A-Z]*:  ', linecache.getline(path, line_for_check)):
                flag, text = flag_and_text(line=linecache.getline(path, line_for_check))

                if flag == 'CONTEXT':
                    context_message += text
                    line_for_check += 1
                    break

            line_for_check += 1

        while not re.findall(r'[A-Z]*:  ', linecache.getline(path, line_for_check)):
            context_message += linecache.getline(path, line_for_check)
            line_for_check += 1

        full_message = err_message + "\n" + context_message

        return line_for_check, full_message
    else:
        return line_for_check, ''
    


def warning(path: str, line_for_check: int) -> tuple[int, str]:
    err_message = ''
    context_message = ''
    line = linecache.getline(path, line_for_check)

    if not re.findall(r'[A-Z]*:  ', line):
         return line_for_check, ''

    flag, text = flag_and_text(line=line)
    
    if flag=='WARNING':
        err_message = text
        line_for_check += 2

        flag, text = flag_and_text(line=linecache.getline(path, line_for_check))

        context_message += text

        full_message = err_message + "\n" + context_message

        return line_for_check, full_message
    else:
        return line_for_check, ''


# set_errors = set()

def err(path, line_for_check, set_errors):
     
    line_for_check, full_message = error(path, line_for_check)

    if not full_message:
        line_for_check, full_message = warning(path, line_for_check)

    if full_message in set_errors:
        full_message = ''
    else:
        set_errors.add(full_message)
    
    return line_for_check, full_message, set_errors    





 



        