import tipos
from messages import Message

class Line:

    def __init__(self, line_type: str, budget: str) -> None:
        self.set_type(line_type)
        self.budget = self.get_budget_from_string(budget)
            
    def get_budget_from_string(self, budget: str) -> float:
        income = False
        if budget[0] == '+':
            income = True
            budget = budget[1:]
        if not budget.replace('.', '', 1).isdigit():
            raise TypeError(Message.INVALID_BUDGET)
        if income:
            return float(budget)
        return -float(budget)
        
    def get_budget(self) -> float:
        return self.budget
    def set_budget(self, budget: str) -> None:
        self.budget = self.get_budget_from_string(budget)
    def get_line_type(self) -> str:
        return self.line_type
    def set_type(self, line_type: str) -> None:
        if line_type not in tipos.Tipos_de_Despesa._member_names_:
            raise TypeError(Message.INVALID_LINE_TYPE)
        else:
            self.line_type = line_type
    def __str__(self) -> str:
        return f'\t{self.line_type}\t{self.budget} \N{euro sign}'