from messages import Message
from line import Line

class Activity: # investigar sobre heritage in python
        
    def __init__(self, activity_name: str) -> None:
        self.activity_name = activity_name
        self.lines = {}

    def get_activity_name(self) -> str:
        return self.activity_name

    def set_name(self, activity_name: str) -> str:
        self.activity_name = activity_name

    def add_line_type(self, line_type: str, budget: str) -> None:
        if self.line_type_exists(line_type):
            raise Exception(Message.LINE_TYPE_ALREADY_EXIST)
        self.lines[line_type] = Line(line_type, budget)

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

    def delete_all_lines(self) -> None:
        self.lines.clear()

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
        out = f'Activity: {self.activity_name}\n'
        for t in self.get_lines():
            out += f'\t{str(self.get_line_type(t))}\n'
            total_budget += self.get_line_type(t).get_budget()
            # total_real += self.get_line_type(t).get_value()
        out += f'\t\t{(16 + self.get_decimal_cases(total_budget))*"-"}\n'
        out += f'\t\tTotal\t{total_budget} \N{euro sign}\n'
        self.total_budget = total_budget
        return out
