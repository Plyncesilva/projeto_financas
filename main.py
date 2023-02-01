import pickle
from pasta import Pasta
import sys
from messages import Message
from animador import Animador
from tipos import DIR
from tipos import Sections
import os
import string

# TODO FOCUS ON FEATURES AND LESS UI DESIGN FROM NOW ON
# Handle different pasta types
# Auto complete commands
# Ability to add line types?
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
        out += '- ' + str(get_pasta(p).get_nome()) + '\n'
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

# hardcoded
def view_sections():
    out = ''
    for s in Sections:
        out += f'- {s.name}\n'
    return out

def view() -> str:

    if curr_dir == DIR.GLOBAL:
        return view_sections()
    elif curr_dir == DIR.PASTAS:
        return view_all_pastas()
    elif curr_dir == DIR.ANIMADORES:
        return view_all_animadores()
    elif curr_dir == DIR.ANIMADOR:
        return view_animador(curr_animador)
    elif curr_dir == DIR.PASTA:
        return view_pasta(curr_pasta)
    elif curr_dir == DIR.ACTIVITY:
        return view_activity(curr_pasta, curr_activity)
    elif curr_dir == DIR.LINE:
        return view_line(curr_pasta, curr_activity, curr_line)
    elif curr_dir == DIR.STATISTICS:
        return 'Statistics still on development phase!\n'
    else:
        pass # never gets here 

def clear():
    os.system('clear') # this is linux dependent!

def edit_pasta(pasta_name: str):
    pasta = get_pasta(pasta_name)
    clear()
    pasta_name = input(f"> pasta_name({pasta.get_nome()}): ")
    pasta_type = input(f"> pasta_type({pasta.get_tipo()}): ")
    if pasta_type != '':
        update_pasta_type(pasta.get_nome(), pasta_type)
    if pasta_name != '':
        update_pasta_name(pasta.get_nome(), pasta_name)

def edit_activity(activity_name: str):
    activity = get_pasta(curr_pasta).get_activity(activity_name)
    clear()
    activity_name = input(f"> activity_name({activity.get_activity_name()}): ")
    if activity_name != '':
        update_activity_name(activity.get_activity_name(), activity_name)

def edit_line(line_type: str):
    line = get_pasta(curr_pasta).get_activity(curr_activity).get_line_type(line_type)
    clear()
    line_type = input(f"> line_type({line.get_line_type()}): ")
    line_budget = input(f"> line_budget({line.get_budget()}): ")
    if line_budget != '':
        update_line_budget(curr_pasta, curr_activity, line.get_line_type(), line_budget)
    if line_type != '':
        update_line_type(curr_pasta, curr_activity, line.get_line_type(), line_type)

def edit_animador(name: str):
    animador = get_animador(name)
    clear()
    new_name = input(f"> name({animador.get_name()}): ")
    nib = input(f"> nib({animador.get_NIB()}): ")
    nuc = input(f"> nucleo({animador.get_nucleo()}): ")
    if nuc != '':
        update_animador_nucleo(animador.get_name(), nuc)
    if nib != '':
        update_animador_nucleo(animador.get_name(), nib)
    if new_name != '':
        update_animador_name(animador.get_name(), new_name)


def update(command) -> str:

    l = len(command)

    if l != 2:
        return Message.UPDATE_COMMAND_USAGE

    request = command[1]

    if curr_dir == DIR.PASTAS:
        edit_pasta(request)
    elif curr_dir == DIR.PASTA:
        edit_activity(request)
    elif curr_dir == DIR.ACTIVITY:
        edit_line(request)
    elif curr_dir == DIR.ANIMADORES:
        edit_animador(request)
    else:
        raise Exception(Message.CANNOT_EDIT_HERE)
        
def add(command):
    l = len(command)

    if l <= 1:
        return Message.ADD_COMMAND_USAGE

    request = command[1]

    if curr_dir == DIR.PASTAS:
        if l != 3:
            raise Exception(Message.ADD_COMMAND_USAGE)
        add_pasta(request, command[2])
    elif curr_dir == DIR.PASTA:
        if l != 2:
            raise Exception(Message.ADD_COMMAND_USAGE)
        add_activity(curr_pasta, request)
    elif curr_dir == DIR.ACTIVITY:
        if l != 3:
            raise Exception(Message.ADD_COMMAND_USAGE)
        add_line_type(curr_pasta, curr_activity, request, command[2])
    elif curr_dir == DIR.ANIMADORES:
        if l != 4:
            raise Exception(Message.ADD_COMMAND_USAGE)
        add_animador(command[1], command[2], command[3])
    else:
        raise Exception(Message.CANNOT_ADD_HERE)

def remove(command):
    l = len(command)

    if l != 2:
        raise Exception(Message.REMOVE_COMMAND_USAGE)

    request = command[1]

    if curr_dir == DIR.PASTAS:
        delete_pasta(request)
    elif curr_dir == DIR.PASTA:
        delete_activity(curr_pasta, request)
    elif curr_dir == DIR.ACTIVITY:
        delete_line_type(curr_pasta, curr_activity, request)
    elif curr_dir == DIR.ANIMADORES:
        delete_animador(request)
    else:
        raise Exception(Message.CANNOT_REMOVE_HERE)

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
    global curr_section
    global curr_animador

    if len(command) != 2:
        raise Exception(Message.INVALID_OPERAND)
    
    request = command[1]

    if curr_dir == DIR.GLOBAL:
        if request not in Sections._member_names_: # isto esta muito mau
            raise Exception(Message.SECTION_NAME_NON_EXISTENT)
        curr_section = request
        curr_dir = DIR._member_map_[request.upper()]
    elif curr_dir == DIR.PASTAS:
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
    elif curr_dir == DIR.ANIMADORES:
        if not animador_exists(request):
            raise Exception(Message.ANIMADOR_NON_EXISTENT)
        curr_animador = request
        curr_dir = DIR.ANIMADOR
    else:
        raise Exception(Message.CANNOT_GO_ANY_FURTHER)
    path += '/' + request

def exit_directory():
    global path
    global curr_dir
    global curr_pasta
    global curr_activity
    global curr_line
    global curr_animador
    global curr_section
    
    if len(command) != 1:
        raise Exception(Message.INVALID_OPERAND)

    if curr_dir == DIR.PASTAS:
        curr_dir = DIR.GLOBAL
        curr_section = None
    elif curr_dir == DIR.ANIMADOR:
        curr_dir = DIR.ANIMADORES
        curr_animador = None
    elif curr_dir == DIR.ANIMADORES:
        curr_dir = DIR.GLOBAL
        curr_section = None
    elif curr_dir == DIR.PASTA:
        curr_pasta = None
        curr_dir = DIR.PASTAS    
    elif curr_dir == DIR.ACTIVITY:
        curr_activity = None
        curr_dir = DIR.PASTA    
    elif curr_dir == DIR.LINE:
        curr_line = None
        curr_dir = DIR.ACTIVITY
    elif curr_dir == DIR.STATISTICS:
        curr_dir = DIR.GLOBAL
        curr_section = None
    else: 
        raise Exception(Message.CANNOT_EXIT_GLOBAL)    
    path = '/'.join(path.split('/')[:-1])


# Main

if __name__ == "__main__":
    
    global pastas
    global animadores
    
    global path
    global curr_pasta
    global curr_activity
    global curr_line
    global curr_dir
    global curr_animador
    global curr_section

    path = 'global'
    curr_dir = DIR.GLOBAL
    curr_pasta = None
    curr_activity = None
    curr_line = None
    curr_animador = None
    curr_section = None

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
        clear()
        print(view())
        if user_info != '':
            print(user_info)
            user_info = ''
        
        raw = input(f'\n{path} > ')
        command = raw.split(' ')

        key_word = command[0]

        try:
            if key_word == 'exit': # exit
                break
            elif key_word == 'edit': # update some information
                update(command)
                save_db()
            elif key_word == 'add':
                add(command)
                save_db()
            elif key_word == "rm":
                remove(command)
                save_db()
            elif key_word == "h":
                user_info = Message.HELP
            elif key_word == 'in':
                enter_directory(command)
            elif key_word == 'out':
                exit_directory()
            else:
                user_info = Message.UNKNOWN_COMMAND
        except (Exception, TypeError) as e:
            user_info = e

    # save data base
    save_db()