import re
import linecache
from session_data import Session


def flag_and_text(line) -> tuple[str, str]:
        search = re.search(r'([A-Z]*):  (.*)', line)
        return search.group(1), search.group(2)
                    

def error(session: Session) -> str:
    err_message = ''
    context_message = ''
    line = linecache.getline(session.last_open_file, session.line_for_check)

    if not re.findall(r'[A-Z]*:  ', line):
         return ''

    flag, text = flag_and_text(line=line)
    
    if flag=='ERROR':
        err_message = text
        session.line_for_check += 1

        while True:
            if re.findall(r'[A-Z]*:  ', linecache.getline(session.last_open_file, session.line_for_check)):
                flag, text = flag_and_text(line=linecache.getline(session.last_open_file, session.line_for_check))

                if flag == 'CONTEXT':
                    context_message += text
                    session.line_for_check += 1
                    break

            session.line_for_check += 1

        while not re.findall(r'[A-Z]*:  ', linecache.getline(session.last_open_file, session.line_for_check)):
            context_message += linecache.getline(session.last_open_file, session.line_for_check)
            session.line_for_check += 1

        full_message = err_message + "\n" + context_message

        return full_message
    else:
        return ''


def err(session: Session) -> str:
     
    full_message = error(session)

    if full_message in session.set_errors:
        full_message = ''
    
    if full_message:
        session.set_errors.add(full_message)
        return full_message   





 



        