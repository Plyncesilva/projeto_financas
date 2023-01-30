import json
import tipos

class Tipo:

    def __init__(self, tipo: str, orcamentado: float) -> None:
        self.set_tipo(tipo)
        self.valor = 0
        self.orcamentado = orcamentado

    def set_valor(self, valor: float) -> None:
        if valor >= 0:
            self.valor = valor
        else:
            # erro!
            pass

    def add_valor(self, valor: float) -> None:
        if valor >= 0:
            self.valor += valor
        else:
            # erro
            pass

    def sub_valor(self, valor: float) -> None:
        if valor >= 0 and self.valor-valor >= 0:
            self.valor -= valor
        else:
            # erro
            pass

    def orcamentado(self) -> float:
        return self.orcamentado

    def valor(self) -> float:
        return self.valor

    def set_tipo(self, tipo: str):
        if tipo not in tipos.Tipos_de_Despesa._member_names_:
            # erro!
            pass
        else:
            self.tipo = tipo

    def __str__(self) -> str:
        return f'Tipo de despesa: {self.tipo}\t{self.valor}\t{self.orcamentado}'