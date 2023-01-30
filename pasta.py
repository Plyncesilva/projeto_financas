import tipos
from messages import Message

class Pasta:
    class Activity: # investigar sobre heritage in python
        class Line:

            def __init__(self, line_type: str, budget: str) -> None:
                self.set_type(line_type)
                self.value = 0
                self.set_budget(budget)

            def set_value(self, value: float) -> None:
                if value >= 0:
                    self.value = value
                else:
                    # erro!
                    pass
                
            def add_value(self, value: float) -> None:
                if value >= 0:
                    self.value += value
                else:
                    # erro
                    pass
                
            def set_budget(self, budget: str) -> None:
                if not budget.replace('.', '', 1).isdigit():
                    raise TypeError(Message.INVALID_BUDGET)
                else:
                    self.budget = float(budget)

            def sub_value(self, value: float) -> None:
                if value >= 0 and self.value-value >= 0:
                    self.value -= value
                else:
                    # erro
                    pass
                
            def get_budget(self) -> float:
                return self.budget

            def get_value(self) -> float:
                return self.value

            def get_line_type(self) -> str:
                return self.line_type

            def set_type(self, line_type: str) -> None:
                if line_type not in tipos.Tipos_de_Despesa._member_names_:
                    raise TypeError(Message.INVALID_LINE_TYPE)
                else:
                    self.line_type = line_type

            def __str__(self) -> str:
                return f'\t{self.line_type}\t{self.value}\t{self.budget}'

        def __init__(self, activity_name: str) -> None:
            self.activity_name = activity_name
            self.lines = {}

        def get_activity_name(self) -> str:
            return self.activity_name

        def set_name(self, activity_name: str) -> str:
            self.activity_name = activity_name

        def add_line_type(self, line_type: str, budget: float) -> None:
            if self.line_type_exists(line_type):
                raise Exception(Message.LINE_TYPE_ALREADY_EXIST)
            self.lines[line_type] = self.Line(line_type, budget)

        def get_lines(self) -> dict:
            return self.lines

        def line_type_exists(self, line_type: str) -> bool:
            return line_type in self.lines

        def get_line_type(self, line_type) -> Line:
            if self.line_type_exists(line_type):
                return self.get_lines()[line_type]
            raise Exception(Message.LINE_TYPE_NON_EXISTENT)

        def delete_line_type(self, line_type: str) -> None:
            if not self.line_type_exists(line_type):
                raise Exception(Message.LINE_TYPE_NON_EXISTENT)
            del(self.lines[line_type])

        def set_line_type(self, line_type, new_line_type):
            line = self.get_line_type(line_type)
            if self.line_type_exists(new_line_type):
                raise Exception(Message.LINE_TYPE_ALREADY_EXIST)
            line.set_type(new_line_type)
            self.lines[new_line_type] = line
            self.delete_line_type(line_type)

        def get_decimal_cases(self, n):
            res = 0
            while n >= 1:
                n = n/10
                res += 1
            return res

        def __str__(self) -> str:
            total_budget = 0
            total_real = 0
            out = f'Activity: {self.activity_name}\n'
            for t in self.get_lines():
                out += f'\t{str(self.get_line_type(t))}\n'
                total_budget += self.get_line_type(t).get_budget()
                total_real += self.get_line_type(t).get_value()
            out += f'\t\t{(18 + self.get_decimal_cases(total_budget))*"-"}\n'
            out += f'\t\tTotal\t{total_real}\t{total_budget}\n'
            return out

    # pasta_name: angariacao de fundos, sul, campos, ...
    # pasta_type: despesas_only, despesas e receitas, receitas_only...
    def __init__(self, pasta_name: str, pasta_type: str) -> None:
        self.pasta_name = None
        self.pasta_type = None
        self.set_name(pasta_name)
        self.set_type(pasta_type)
        self.atividades = {} # atividades e configs deviam ser acessiveis apenas pela pasta
        # timestamp da ultima data de escrita
        # timestamp de quando foi guardada na base de dados
        pass
    def get_nome(self) -> str:
        return self.pasta_name
    def get_tipo(self) -> str:
        return self.pasta_type
    def get_activities(self) -> dict:
        return self.atividades
    
    def get_activity(self, activity_name) -> Activity:
        if self.activity_exists(activity_name):
            return self.atividades[activity_name]
        raise Exception(Message.ACTIVITY_NON_EXISTENT)

    def set_name(self, pasta_name: str) -> None:
        self.pasta_name = pasta_name
    def set_type(self, pasta_type: str) -> None:
        if pasta_type not in tipos.Tipos_de_Pasta._member_names_:
            raise TypeError(Message.INVALID_PASTA_TYPE)
        else:
            self.pasta_type = pasta_type
    def add_activity(self, activity_name: str) -> None:
        if self.activity_exists(activity_name):
            raise Exception(Message.ACTIVITY_ALREADY_EXIST)
        self.atividades[activity_name] = self.Activity(activity_name)
    
    def activity_exists(self, activity_name: str) -> bool:
        return activity_name in self.get_activities()

    def delete_activity(self, activity_name: str) -> None:
        if not self.activity_exists(activity_name):
            raise Exception(Message.ACTIVITY_NON_EXISTENT)
        del(self.atividades[activity_name])

    def set_activity_name(self, activity_name, new_activity_name):
        activity = self.get_activity(activity_name)
        if self.activity_exists(new_activity_name):
            raise Exception(Message.ACTIVITY_ALREADY_EXIST)
        activity.set_name(new_activity_name)
        self.atividades[new_activity_name] = activity
        self.delete_activity(activity_name)

    def __str__(self) -> str:
        out = f'Pasta: {self.get_nome()}\n'
        for at in self.atividades:
            out += f'\t{str(self.atividades[at])}'
        return out