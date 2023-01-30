import pickle
from pasta import Pasta
import sys
from messages import Message
from animador import Animador
from tipos import DIR
import os

# TODO
# Melhorar eficiencia estrutural do codigo, muita coisa repetida diria
# Handle different pasta types
# Ability to add line types?
# Auto complete commands
# Improve usability and CLI, less extensive commands, memorize current path
# Remove All animadores, pastas, all... (cuidado com isto, nao tem assim tanto interesse apagar tudo...)

# Database management

def save_db() -> None:
    try:
        with open('pastas.dat', 'wb') as f:
            pickle.dump(pastas, f, pickle.HIGHEST_PROTOCOL)
        with open('animadores.dat', 'wb') as f:
            pickle.dump(animadores, f, pickle.HIGHEST_PROTOCOL)
    except:
        print(Message.DATABASE_ERROR_SAVING)
        exit()

# UI handlers

def get_user_info(op: str):
    if op in ['-p', '-pt', '-a', '-l', '-lb']:
        return view_all_pastas()
    elif op in ['-ani', '-nib', '-nuc']:
        return view_all_animadores()
    elif op in ['-all']:
        return view_all_pastas() + view_all_animadores()

# Global structures handlers

def get_pasta(pasta_name) -> Pasta:
    if pasta_exists(pasta_name):
        return pastas[pasta_name]
    raise Exception(Message.PASTA_NON_EXISTENT)

def get_animador(name) -> Animador:
    if animador_exists(name):
        return animadores[name]
    raise Exception(Message.ANIMADOR_NON_EXISTENT)

def pasta_exists(pasta_name) -> bool:
    return pasta_name in pastas

def animador_exists(name):
    return name in animadores

# individual commands

# Delete

def delete_pasta(pasta_name) -> None:
    if not pasta_exists(pasta_name):
        raise Exception(Message.PASTA_NON_EXISTENT)
    del(pastas[pasta_name])

def delete_activity(pasta_name, activity_name) -> None:
    get_pasta(pasta_name).delete_activity(activity_name)

def delete_line_type(pasta_name, activity_name, line_type) -> None:
    get_pasta(pasta_name).get_activity(activity_name).delete_line_type(line_type)

def delete_animador(name):
    if not animador_exists(name):
        raise Exception(Message.ANIMADOR_NON_EXISTENT)
    del(animadores[name])

# Update

def update_pasta_name(pasta_name, new_pasta_name):
    pasta = get_pasta(pasta_name)
    if pasta_exists(new_pasta_name):
        raise Exception(Message.PASTA_ALREADY_EXIST)
    pasta.set_name(new_pasta_name)
    pastas[new_pasta_name] = pasta
    delete_pasta(pasta_name) 

def update_pasta_type(pasta_name, new_pasta_type):
    get_pasta(pasta_name).set_type(new_pasta_type)

def update_activity_name(pasta_name, activity_name, new_activity_name):
    get_pasta(pasta_name).set_activity_name(activity_name, new_activity_name)

def update_line_type(pasta_name, activity_name, line_type, new_line_type):
    get_pasta(pasta_name).get_activity(activity_name).set_line_type(line_type, new_line_type)

def update_line_budget(pasta_name, activity_name, line_type, new_budget):
    get_pasta(pasta_name).get_activity(activity_name).get_line_type(line_type).set_budget(new_budget)

def update_animador_name(name, new_name):
    animador = get_animador(name)
    if animador_exists(new_name):
        raise Exception(Message.ANIMADOR_ALREADY_EXIST)
    animador.set_name(new_name)
    animadores[new_name] = animador
    delete_animador(name)

def update_animador_nib(name, new_nib):
    get_animador(name).set_NIB(new_nib)

def update_animador_nucleo(name, new_nucleo):
    get_animador(name).set_nucleo(new_nucleo)

# View

def view_pasta(pasta_name) -> str:
    return str(get_pasta(pasta_name))

def view_activity(pasta_name, activity_name) -> str:
    return str(get_pasta(pasta_name).get_activity(activity_name))

def view_line(pasta_name, activity_name, line_type) -> str:
    return str(get_pasta(pasta_name).get_activity(activity_name).get_line_type(line_type))
        
def view_animador(name) -> str:
    return str(get_animador(name))

def view_all_animadores() -> str:
    out = 'Animadores:\n\n'
    for a in animadores:
        out += str(get_animador(a)) + '\n'
    return out

def view_all_pastas():
    out = 'Pastas:\n\n'
    for p in pastas:
        out += str(get_pasta(p)) + '\n'
    return out

# Add

def add_pasta(pasta_name, pasta_type) -> None:
    if pasta_exists(pasta_name):
        raise Exception(Message.PASTA_ALREADY_EXIST)
    else:
        pastas[pasta_name] = Pasta(pasta_name, pasta_type)

def add_activity(pasta_name, activity_name) -> None:
    get_pasta(pasta_name).add_activity(activity_name)

def add_line_type(pasta_name, activity_name, line_type, budget) -> None:
    get_pasta(pasta_name).get_activity(activity_name).add_line_type(line_type, budget)

def add_animador(name, NIB, nucleo):
    if animador_exists(name):
        raise Exception(Message.ANIMADOR_ALREADY_EXIST)
    else:
        animadores[name] = Animador(name, NIB, nucleo)

# Command logic controllers

def view(command) -> str:

    global wipe_screen
    
    if curr_dir == DIR.GLOBAL:
        return view_all_pastas() + view_all_animadores()
    elif curr_dir == DIR.PASTA:
        return view_pasta(curr_pasta)
    elif curr_dir == DIR.ACTIVITY:
        return view_activity(curr_pasta, curr_activity)
    elif curr_dir == DIR.LINE:
        return view_line(curr_pasta, curr_activity, curr_line)
    else:
        pass # never gets here 

    # if op == '-p':
        # if len(command) != 3:
            # wipe_screen = False
            # return Message.INVALID_OPERAND
        # try:
            # return view_pasta(command[2])
        # except Exception as e:
            # wipe_screen = False
            # return e
    # elif op == '-a':
        # if len(command) != 4:
            # wipe_screen = False
            # return Message.INVALID_OPERAND
        # try:
            # return view_activity(command[2], command[3])
        # except Exception as e:
            # wipe_screen = False
            # return e
    # elif op == '-l':
        # if len(command) != 5:
            # wipe_screen = False
            # return Message.INVALID_OPERAND
        # try:
            # return view_line(command[2], command[3], command[4])
        # except Exception as e:
            # wipe_screen = False
            # return e
    # elif op == '-ani':
        # if len(command) != 3:
            # wipe_screen = False
            # return Message.INVALID_OPERAND
        # try:
            # return view_animador(command[2])
        # except Exception as e:
            # wipe_screen = False
            # return e
    # elif op == '-P':
        # if len(command) != 2:
            # wipe_screen = False
            # return Message.INVALID_OPERAND
        # return view_all_pastas()
    # elif op == '-A':
        # if len(command) != 2:
            # wipe_screen = False
            # return Message.INVALID_OPERAND
        # return view_all_animadores()
    # elif op == '-all':
        # if len(command) != 2:
            # wipe_screen = False
            # return Message.INVALID_OPERAND
        # return view_all_pastas() + view_all_animadores()
    # else:
        # wipe_screen = False
        # return Message.INVALID_OPERAND

def update(command) -> str:

    # update pasta name: set -p pasta_name new_pasta_name
    # update pasta type: set -pt pasta_name new_type

    # update activity name: set -a pasta_name activity_name new_activity_name

    # update line type: set -l pasta_name activity_name line_type new_line_type
    # update line budget: set -lb pasta_name activity_name line_type new_budget

    # update animador name: set -ani name new_name
    # update animador nibL set -nib name new_nib
    # update animador nucleo: set -n name new_nucleo

    global wipe_screen

    if len(command) <= 1:
        return Message.UPDATE_COMMAND_USAGE

    op = command[1]

    if op == '-p':
        if len(command) != 4:
            wipe_screen = False
            return Message.INVALID_OPERAND
        try:
            update_pasta_name(command[2], command[3])
        except Exception as e:
            wipe_screen = False
            return e
        return view_pasta(command[3])
    elif op == '-pt':
        if len(command) != 4:
            wipe_screen = False
            return Message.INVALID_OPERAND
        try:
            update_pasta_type(command[2], command[3])
        except Exception as e:
            wipe_screen = False
            return e
        return view_pasta(command[2])
    elif op == '-a':
        if len(command) != 5:
            wipe_screen = False
            return Message.INVALID_OPERAND
        try:
            update_activity_name(command[2], command[3], command[4])
        except Exception as e:
            wipe_screen = False
            return e
        return view_pasta(command[2])
    elif op == '-l':
        if len(command) != 6:
            wipe_screen = False
            return Message.INVALID_OPERAND
        try:
            update_line_type(command[2], command[3], command[4], command[5])
        except Exception as e:
            wipe_screen = False
            return e
        return view_pasta(command[2])
    elif op == '-lb':
        if len(command) != 6:
            wipe_screen = False
            return Message.INVALID_OPERAND
        try:
            update_line_budget(command[2], command[3], command[4], command[5])
        except Exception as e:
            wipe_screen = False
            return e
        return view_pasta(command[2])
    elif op == '-ani':
        if len(command) != 4:
            wipe_screen = False
            return Message.INVALID_OPERAND
        try:
            update_animador_name(command[2], command[3])
        except Exception as e:
            wipe_screen = False
            return e
        return view_animador(command[2])
    elif op == '-nib':
        if len(command) != 4:
            wipe_screen = False
            return Message.INVALID_OPERAND
        try:
            update_animador_nib(command[2], command[3])
        except Exception as e:
            wipe_screen = False
            return e
        return view_animador(command[2])
    elif op == '-nuc':
        if len(command) != 4:
            wipe_screen = False
            return Message.INVALID_OPERAND
        try:
            update_animador_nucleo(command[2], command[3])
        except Exception as e:
            wipe_screen = False
            return e
        return view_animador(command[2])
    else:
        wipe_screen = False
        return Message.INVALID_OPERAND
        
def add(command) -> str:

    global wipe_screen
    
    l = len(command)

    if l <= 1:
        return Message.ADD_COMMAND_USAGE

    op = command[1]

    if op == "-p":
        if l != 4:
            wipe_screen = False
            return Message.INVALID_OPERAND
        try:
            add_pasta(command[2], command[3])
        except (TypeError, Exception) as e:
            wipe_screen = False
            return e
        return view_pasta(command[2])
    elif op == "-a":
        if l != 4:
            wipe_screen = False
            return Message.INVALID_OPERAND
        try:
            add_activity(command[2], command[3])
        except (TypeError, Exception) as e:
            wipe_screen = False
            return e
        return view_pasta(command[2])
    elif op == "-l":
        if l != 6:
            return Message.INVALID_OPERAND
        try:
            add_line_type(command[2], command[3], command[4], command[5])
        except (Exception,TypeError) as e:
            wipe_screen = False
            return e
        return view_pasta(command[2])
    elif op == "-ani":
        if l != 5:
            wipe_screen = False
            return Message.INVALID_OPERAND
        try:
            add_animador(command[2], command[3], command[4])
        except (Exception, TypeError) as e:
            wipe_screen = False
            return e
        return view_animador(command[2])
    else:
        wipe_screen = False
        return Message.INVALID_OPERAND

def remove(command) -> str:

    global wipe_screen

    l = len(command)

    if l <= 1:
        return Message.REMOVE_COMMAND_USAGE

    op = command[1]

    if op == "-p":
        if l != 3:
            wipe_screen = False
            return Message.INVALID_OPERAND
        try:
            delete_pasta(command[2])
        except Exception as e:
            wipe_screen = False
            return e
        return view_all_pastas()
    elif op == "-a":
        if l != 4:
            wipe_screen = False
            return Message.INVALID_OPERAND
        try:
            delete_activity(command[2], command[3])
        except Exception as e:
            wipe_screen = False
            return e
        return view_pasta(command[2])
    elif op == "-l":
        if l != 5:
            wipe_screen = False
            return Message.INVALID_OPERAND
        try:
            delete_line_type(command[2], command[3], command[4])
        except Exception as e:
            wipe_screen = False
            return e     
        return view_activity(command[2], command[3])   
    elif op == "-ani":
        if l != 3:
            wipe_screen = False
            return Message.INVALID_OPERAND
        try:
            delete_animador(command[2])
        except Exception as e:
            wipe_screen = False
            return e
        return view_all_animadores()
    elif op == '-all':
        if l != 2:
            wipe_screen = False
            return Message.INVALID_OPERAND
        pastas.clear()
        animadores.clear()
        return view_all_animadores() + view_all_pastas()
    else:
        wipe_screen = False
        return Message.INVALID_OPERAND

def get_path_pasta():
    split = path.split('/')
    if len(split) > 1:
        return split[1]
    return None

def get_path_activity():
    split = path.split('/')
    if len(split) > 2:
        return split[2]
    return None

def get_path_line():
    split = path.split('/')
    if len(split) > 3:
        return split[3]
    return None

def enter_directory(command):
    global path
    global curr_dir
    global curr_pasta
    global curr_activity
    global curr_line

    if len(command) != 2:
        raise Exception(Message.INVALID_OPERAND)
    
    request = command[1]

    if curr_dir == DIR.GLOBAL:
        if not pasta_exists(request):
            raise Exception(Message.PASTA_NON_EXISTENT)
        curr_pasta = request
        curr_dir = DIR.PASTA    
    elif curr_dir == DIR.PASTA:
        if not get_pasta(curr_pasta).activity_exists(request):
            raise Exception(Message.ACTIVITY_NON_EXISTENT)
        curr_activity = request
        curr_dir = DIR.ACTIVITY    
    elif curr_dir == DIR.ACTIVITY:
        if not get_pasta(curr_pasta).get_activity(curr_activity).line_type_exists(request):
            raise Exception(Message.LINE_TYPE_NON_EXISTENT)
        curr_line = request
        curr_dir = DIR.LINE    
    else: 
        pass # em teoria imporssivel chegar aqui
    path += '/' + request

def exit_directory():
    global path
    global curr_dir
    global curr_pasta
    global curr_activity
    global curr_line

    if curr_dir == DIR.GLOBAL:
        raise Exception(Message.CANNOT_EXIT_GLOBAL)    
    elif curr_dir == DIR.PASTA:
        curr_pasta = None
        curr_dir = DIR.GLOBAL    
    elif curr_dir == DIR.ACTIVITY:
        curr_activity = None
        curr_dir = DIR.PASTA    
    elif curr_dir == DIR.LINE:
        curr_line = None
        curr_dir = DIR.ACTIVITY
    else: 
        pass # em teoria imporssivel chegar aqui
    path = '/'.join(path.split('/')[:-1])


# Main

if __name__ == "__main__":
    
    global pastas
    global animadores
    global wipe_screen
    global path
    global curr_pasta
    global curr_activity
    global curr_line
    global curr_dir

    path = 'global'
    curr_dir = DIR.GLOBAL
    curr_pasta = None
    curr_activity = None
    curr_line = None

    wipe_screen = True
    prev_user_info = ''
    user_info = ''
    # load data base
    try:
        with open('pastas.dat', 'rb') as f:
            pastas = pickle.load(f)
        with open('animadores.dat', 'rb') as f:
            animadores = pickle.load(f)
    except:
        print(Message.DATABASE_ERROR_LOADING)
        exit()

    # interactive menu
    while True:
        os.system('clear') # this is linux dependent!
        if not wipe_screen:
            print(prev_user_info)
            wipe_screen = True
        
        print(user_info)
        if len(str(user_info)) > 0 and str(user_info)[0] != '#':
            prev_user_info = user_info
        user_info = ''
        
        
        raw = input(f'\n{path} > ')
        command = raw.split(' ')

        key_word = command[0]

        if key_word == 'exit': # exit
            break
        elif key_word == 'view': # view some type of information
            user_info = view(command)
        elif key_word == 'set': # update some information
            user_info = update(command)
            save_db()
        elif key_word == 'add':
            user_info = add(command)
            save_db()
        elif key_word == "rm":
            user_info = remove(command)
            save_db()
        elif key_word == "h":
            user_info = Message.HELP
        elif key_word == 'in':
            try:
                enter_directory(command)
            except Exception as e:
                user_info = e
        elif key_word == 'out':
            try:
                exit_directory()
            except Exception as e:
                user_info = e
        else:
            user_info = Message.UNKNOWN_COMMAND

    # save data base
    save_db()