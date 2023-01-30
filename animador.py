from tipos import Nucleos
from messages import Message
import string

class Animador:

    def __init__(self, name: str, NIB: str, nucleo: str) -> None:
        self.name = name
        self.NIB = NIB
        self.set_nucleo(nucleo)

    def get_name(self) -> str:
        return self.name

    def get_NIB(self) -> str:
        return self.NIB

    def set_name(self, name: str) -> None:
        self.name = name

    def set_NIB(self, NIB: str) -> None:
        if self.valid_iban(NIB) or self.valid_nib(NIB):
            self.NIB = NIB
        else:
            raise TypeError(Message.INVALID_NIB_IBAN)

    def set_nucleo(self, nucleo: str) -> None:
        if nucleo in Nucleos._member_names_:
            self.nucleo = nucleo            
        else:
            raise TypeError(Message.INVALID_NUCLEO)

    def format_nib(self, nib: str):
        
        out = ''
        for i in range(len(nib)):
            out += nib[i]
            if (i+1)%4 == 0:
                out += ' '
        return out

    def __str__(self) -> str:
        return f'-> {self.name}\t{self.format_nib(self.NIB)}\t{self.nucleo}'

    def _toIntList(self, numstr, acceptX=0):
        """
        Converte string passada para lista de inteiros,
        eliminando todos os caracteres inválidos.
        Recebe string com nmero a converter.
        Segundo parÃ¢metro indica se 'X' e 'x' devem ser
        convertidos para '10' ou não.
        """
        res = []

        # converter todos os dígitos
        for i in numstr:
            if i in string.digits:
                res.append(int(i))

        # converter dígito de controlo no ISBN
        if acceptX and (numstr[-1] in 'Xx'):
            res.append(10)
        return res

    def _sumLists(self, a, b):
        """
        Devolve soma dos produtos, membro a membro, das listas.
        Recebe duas listas de tamanho igual.
        """
        val = 0
        for i in map(lambda a, b: a * b, a, b):
            val += i
        return val

    def valid_nib(self, nib: str):
        """
        Verifica validade de número de identificação bancária.
        Recebe string com NIB.
        """
        LEN_NIB = 21
        table = (73, 17, 89, 38, 62, 45, 53, 15, 50,
                 5, 49, 34, 81, 76, 27, 90, 9, 30, 3)

        # converter para lista de inteiros
        nib = self._toIntList(nib)

        # verificar tamanho do número passado
        if len(nib) != LEN_NIB:
            return False

        # ultimos dois dígitos são o valor de verificação
        return nib[-2] * 10 + nib[-1] == 98 - self._sumLists(table, nib[:-2]) % 97

    def valid_iban(self, iban):
        """
        Verifica validade de número de identificação bancária
        internacional (apenas Portugal).
        Recebe string com IBAN.
        """

        # verificar código IBAN para Portugal
        if iban[:4] == 'PT50':
            return self.valid_nib(iban[4:])
        else:
            raise ValueError("Código IBAN não suportado: %s" % iban[:4])