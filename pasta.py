import tipos
from messages import Message
from activity import Activity

class Pasta:
    # pasta_name: angariacao de fundos, sul, campos, ...
    # pasta_type: despesas_only, despesas e receitas, receitas_only...
    def __init__(self, pasta_name: str) -> None:
        self.pasta_name = None
        self.set_name(pasta_name)
        self.atividades = {} # atividades e configs deviam ser acessiveis apenas pela pasta
        # timestamp da ultima data de escrita
        # timestamp de quando foi guardada na base de dados
        pass
    def get_nome(self) -> str:
        return self.pasta_name
    def get_activities(self) -> dict:
        return self.atividades
    
    def get_activity(self, activity_name) -> Activity:
        if self.activity_exists(activity_name):
            return self.atividades[activity_name]
        raise Exception(Message.ACTIVITY_NON_EXISTENT)

    def set_name(self, pasta_name: str) -> None:
        self.pasta_name = pasta_name
    def add_activity(self, activity_name: str) -> None:
        if self.activity_exists(activity_name):
            raise Exception(Message.ACTIVITY_ALREADY_EXIST)
        self.atividades[activity_name] = Activity(activity_name)
    
    def activity_exists(self, activity_name: str) -> bool:
        return activity_name in self.get_activities()

    def delete_activity(self, activity_name: str) -> None:
        if not self.activity_exists(activity_name):
            raise Exception(Message.ACTIVITY_NON_EXISTENT)
        del(self.atividades[activity_name])

    def delete_all_activities(self) -> None:
        self.atividades.clear()

    def set_activity_name(self, activity_name, new_activity_name):
        activity = self.get_activity(activity_name)
        if self.activity_exists(new_activity_name):
            raise Exception(Message.ACTIVITY_ALREADY_EXIST)
        activity.set_name(new_activity_name)
        self.atividades[new_activity_name] = activity
        self.delete_activity(activity_name)

    def get_decimal_cases(self, n):
        res = 0
        while n >= 1:
            n = n/10
            res += 1
        return res

    def __str__(self) -> str:
        out = f'Pasta: {self.get_nome()}\n'
        total_budget = 0
        for at in self.atividades:
            out += f'\t{str(self.atividades[at])}'
            total_budget += self.atividades[at].total_budget
        out +=  f'\t{(16 + self.get_decimal_cases(total_budget))*"-"}\n'
        out += f'\tTotal\t{total_budget} \N{euro sign}\n'
        return out
    
