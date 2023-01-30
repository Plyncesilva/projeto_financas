from tipo_de_despesa import Tipo

class Atividade: # investigar sobre heritage in python

    def __init__(self, nome) -> None:
        self.nome = nome
        self.tipos_de_despesa = []

    def nome(self) -> str:
        return self.nome

    def set_nome(self, nome: str) -> str:
        self.nome = nome
    
    def adicionar_tipo_de_despesa(self, t: Tipo) -> None:
        self.tipos_de_despesa.append(t)

    def tipos_de_despesa(self) -> list:
        return self.tipos_de_despesa

    def remover__tipo_de_despesa(self, t: Tipo) -> None:
        for i in range(len(self.tipos_de_despesa)):
            if self.tipos_de_despesa[i].equals(t):
                del(self.tipos_de_despesa[i])
                break

    def __str__(self) -> str:
        out = f'Atividade: {self.nome}\n'
        for t in self.tipos_de_despesa:
            out += f'\t{str(t)}\n'
        return out