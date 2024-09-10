import re
import linecache


def WARNING(path, line_for_check, line):
    match1 = re.search(r'WARNING', line)
    full_message = ''
    if match1:
        line_for_check += 2
        line = linecache.getline(path, line_for_check)
        full_message = line
        # await send_message(id, line.strip())
        # await asyncio.sleep(10)
        line_for_check += 1
    return line_for_check, full_message   
    

def ERROR(path, line_for_check, line):
    match2 = re.search(r'ERROR', line)
    FullContext = ''
    full_message = ''        
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
        full_message = line.strip() + '\n' + Context.strip() + '\n' + FullContext.strip()
        # await send_message(id, line.strip() + '\n' + Context.strip() + '\n' + FullContext.strip())
        # await asyncio.sleep(10)
    return line_for_check, full_message    
       
                        

def FATAL(line, line_for_check):
    match3 = re.search(r'FATAL', line) 
    full_message = ''                                 
    if match3:
        full_message = line.strip()
        # await send_message(id, line.strip()) 
        # await asyncio.sleep(10)
    return line_for_check, full_message      

    
def err(path, line, line_for_check, full_message):

    line_for_check, full_message = WARNING(path, line_for_check, line)
    
    line_for_check, full_message = ERROR(path, line_for_check, line)
   
    line_for_check, full_message = FATAL(line, line_for_check)

            
    return line_for_check, full_message



        