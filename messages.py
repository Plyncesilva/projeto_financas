from dataclasses import dataclass
from tipos import Tipos_de_Despesa
from tipos import Tipos_de_Pasta
from tipos import Nucleos

@dataclass
class Message:
    def italic(text) -> str:
        return f'\x1B[3m{text}\x1B[0m'

    UNKNOWN_COMMAND: str = "#! Unknown command."

    INVALID_NUCLEO: str = f'Invalid {italic("nucleo")}, should be one of {Nucleos._member_names_}'
    INVALID_NIB_IBAN: str = f'Invalid {italic("NIB or IBAN")}.'

    INVALID_LINE_TYPE: str = f'Invalid {italic("line_type")}, should be one of {Tipos_de_Despesa._member_names_}'
    INVALID_BUDGET: str = f'#! Wrong value type for {italic("budget")}. Should be numerical.'

    INVALID_PASTA_TYPE: str = f'Invalid {italic("pasta_type")}, should be one of {Tipos_de_Pasta._member_names_}'

    PASTA_NON_EXISTENT: str = "#! Chosen \x1B[3mpasta_name \x1B[0mdoes not exist."
    PASTA_ALREADY_EXIST: str = "#! Chosen \x1B[3mpasta_name \x1B[0malready exists."

    ACTIVITY_NON_EXISTENT: str = "#! Chosen \x1B[3mactivity_name \x1B[0mdoes not exist."
    ACTIVITY_ALREADY_EXIST: str = "#! Chosen \x1B[3mactivity_name \x1B[0malready exists."

    LINE_TYPE_NON_EXISTENT: str = "#! Chosen \x1B[3mline_type \x1B[0mdoes not exist."
    LINE_TYPE_ALREADY_EXIST: str = "#! Chosen \x1B[3mline_type \x1B[0malready exists."

    ANIMADOR_NON_EXISTENT: str = f'#! {italic("Animador")} with {italic("name")} does not exist.'
    ANIMADOR_ALREADY_EXIST: str = f'#! {italic("Animador")} with {italic("name")} already exists.'

    DATABASE_ERROR_LOADING: str = '#! Error loading data base!'
    DATABASE_ERROR_SAVING: str = '#! Error saving data base!'

    INVALID_OPERAND: str = '#! Invalid command usage, type the command name for help.'

    CANNOT_EXIT_GLOBAL: str = '#! You cannot exit the global directory.'
    CANNOT_GO_ANY_FURTHER: str = '#! There is no where else to go.'

    SECTION_NAME_NON_EXISTENT: str = "#! Chosen \x1B[3msection_name \x1B[0mdoes not exist."

    CANNOT_ADD_HERE: str = '#! You cannot add anything in here.'
    CANNOT_REMOVE_HERE: str = '#! You cannot remove anything in here.'

    HELP: str = f"""
    Available commands:

        > {italic("add")}
            To add an element.
        
        > {italic("rm")}
            To remove an element.
        
        > {italic("set")}
            To update an element.

        > {italic("view")}
            To view an element.
    
        For options within each command, type the command itself!
    """

    ADD_COMMAND_USAGE: str = f"""
    Usage: add [-p][-a][-l][-ani] args
    
        [-p] \x1B[3mpasta_name pasta_type\x1B[0m
            - add a \x1B[3mpasta \x1B[0mwith one of the \x1B[3mpasta_type \x1B[0min {str(Tipos_de_Pasta._member_names_)}.
        
        [-a] \x1B[3mpasta_name \x1B[3mactivity_name\x1B[0m
            - add a new activity.
        
        [-l] \x1B[3mpasta_name activity_name line_type budget_value\x1B[0m
            - add a new line with on of the \x1B[3mline_type \x1B[0min {str(Tipos_de_Despesa._member_names_)}.

        [-ani] {italic("name NIB nucleo")}
            - add a new {italic("animador")} with {italic("name")}, a valid {italic("NIB")} and a {italic("nucleo")} from {str(Nucleos._member_names_)}.     
    """
    
    REMOVE_COMMAND_USAGE: str = f"""
    Usage: rm [-p][-a][-l][-ani][-all] args

        [-p] \x1B[3mpasta_name\x1B[0m
            - remove a \x1B[3mpasta \x1B[0mwith \x1B[3mpasta_name\x1B[0m.
        
        [-a] \x1B[3mpasta_name \x1B[3mactivity_name\x1B[0m
            - remove an \x1B[3mactivity \x1B[0mwith \x1B[3mactivity_name\x1B[0m.
        
        [-l] \x1B[3mpasta_name activity_name line_type\x1B[0m
            - remove a \x1B[3mline \x1B[0mwith \x1B[3mline_type\x1B[0m.
        
        [-ani] {italic("name")}
            - remove a {italic("animador")} with {italic("name")}.

        [-all]\x1B[0m
            - remove everything. Carefull with this."""
    
    VIEW_COMMAND_USAGE: str = f"""
    Usage: view [-p][-a][-l][-ani][-P][-A][-all] args

        [-p] \x1B[3mpasta_name\x1B[0m
            - view a \x1B[3mpasta \x1B[0mwith \x1B[3mpasta_name\x1B[0m.
        
        [-a] \x1B[3mpasta_name \x1B[3mactivity_name\x1B[0m
            - view an \x1B[3mactivity \x1B[0mwith \x1B[3mactivity_name\x1B[0m.
        
        [-l] \x1B[3mpasta_name activity_name line_type\x1B[0m
            - view a \x1B[3mline \x1B[0mwith \x1B[3mline_type\x1B[0m.
        
        [-ani] {italic("name")}
            - view a {italic("animador")} with {italic("name")}.

        [-P]
            - view all pastas.

        [-A]
            - view all animadores.

        [-all]\x1B[0m
            - view everything.
    """

    UPDATE_COMMAND_USAGE: str = f"""
    Usage: set [-p][-pt][-a][-l][-lb][-ani][-nib][-nuc] args

        [-p] {italic("pasta_name new_pasta_name")}
            - update a {italic("pasta")} with {italic("pasta_name")} to {italic("new_pasta_name")}.
        
        [-pt] {italic("pasta_name new_pasta_type")}
            - update a {italic("pasta_type")} with {italic("pasta_name")} to {italic("new_pasta_type")}.
        
        [-a] {italic("pasta_name activity_name new_activity_name")}
            - update an {italic("activity")} with {italic("activity_name")} to {italic("new_activity_name")}.
        
        [-l] {italic("pasta_name activity_name line_type new_line_type")}
            - update a {italic("line")} with {italic("line_type")} to {italic("new_line_type")}.
        
        [-lb] {italic("pasta_name activity_name line_type new_budget")}
            - update a {italic("line_budget")} with {italic("line_type")} to {italic("new_budget")}.

        [-ani] {italic("name new_name")}
            - update a {italic("animador name")} to {italic("new name")}.  

        [-nib] {italic("name new_nib")}
            - update a {italic("animador nib")} to {italic("new_nib")}.    
            
        [-nuc] {italic("name new_nucleo")}
            - update a {italic("animador nucleo")} to {italic("new_nucleo")}.    
    """