########## Expressoes.py ##########
import math


class Expressoes:
    """
    A classe Expressoes contém métodos para calcular diferentes expressões matemáticas.

    Cada método da classe Expressoes calcula uma expressão matemática específica. As expressões são definidas como (1 + log2(i)) * log2(n / ni), onde 'i' é um elemento de um conjunto 'j' ou de uma consulta 'q', 'n' é um número de documentos na coleção e 'ni' é um número de documentos em que Ki ocorre.

    Métodos:
    \n\t`calcular_wij(i: int or float, n: int or float, ni: int or float) -> float or str`: Calcula o valor de peso dos termos (TF x IDF) no documento.
    \n\t`calcular_wiq(i: int or float, n: int or float, ni: int or float) -> float or str`: Calcula o valor de peso dos termos (TF x IDF) na consulta.

    Exemplo:
    >>> i = 2
    >>> n = 10
    >>> ni = 3
    >>> print(f"O peso de 'i' no conjunto 'j' é {Expressoes.calcular_wij(i, n, ni)}")
    "O peso de 'i' no conjunto 'j' é 3.4594316186372978"
    >>> print(f"O peso de 'i' na consulta 'q' é {Expressoes.calcular_wiq(i, n, ni)}")
    "O peso de 'i' na consulta 'q' é 3.4594316186372978"
    """

    @staticmethod
    def calcular_wij(i, n, ni):
        """
        A função calcular_wij calcula o valor de peso dos termos (TF x IDF) no documento.

        A expressão é definida como (1 + log2(i)) * log2(n / ni), onde 'i' é um elemento de um conjunto 'j', 'n' é um número de documentos na coleção e 'ni' é um número de documentos em que Ki ocorre.

        A função verifica se 'i' e 'ni' são diferentes e maiores que 0. Se 'ni' for igual a 'i', a fração será sempre 1 e o log na base 2 de 1 é 0, o que tornará o produto zero. Portanto, a função garante que 'ni' e 'i' são diferentes. Além disso, o logaritmo de 'i' está definido apenas se 'i > 0'.

        Parâmetros:
        \n\t`i (int or float)`: Um elemento do conjunto 'j'.
        \n\t`n (int or float)`: Um número de documentos na coleção.
        \n\t`ni (int or float)`: Um número de documentos em que Ki ocorre.

        Retorno:
        \n\t`float`: O peso de 'i' no conjunto 'j'.
        \n\t`str`: Uma mensagem de erro se 'i' e 'ni' não forem diferentes e maiores que 0.
        """
        # Verifique se i e ni são diferentes e maiores que 0
        if i != ni and i > 0 and ni > 0:
            # Calcule a expressão
            resultado = (1 + math.log2(i)) * math.log2(n / ni)
            return resultado
        else:
            return 0  # "Erro: i e ni devem ser diferentes e maiores que 0"

    @staticmethod
    def calcular_wiq(i, n, ni):
        """
        A função calcular_wiq calcula o valor de peso dos termos (TF x IDF) na consulta.

        A expressão é definida como (1 + log2(i)) * log2(n / ni), onde 'i' é um elemento de uma consulta 'q', 'n' é um número de documentos na coleção e 'ni' é um número de documentos em que Ki ocorre.

        A função verifica se 'i' e 'ni' são diferentes e maiores que 0. Se 'ni' for igual a 'i', a fração será sempre 1 e o log na base 2 de 1 é 0, o que tornará o produto zero. Portanto, a função garante que 'ni' e 'i' são diferentes. Além disso, o logaritmo de 'i' está definido apenas se 'i > 0'.

        Parâmetros:
        \n\t`i (int or float)`: Um elemento da consulta 'q'.
        \n\t`n (int or float)`: Um número de documentos na coleção.
        \n\t`ni (int or float)`: Um número de documentos em que Ki ocorre.

        Retorno:
        \n\t`float`: O peso de 'i' na consulta 'q'.
        \n\t`str`: Uma mensagem de erro se 'i' e 'ni' não forem diferentes e maiores que 0.
        """
        # Verifique se i e ni são diferentes e maiores que 0
        if i != ni and i > 0 and ni > 0:
            # Calcule a expressão
            resultado = (1 + math.log2(i)) * math.log2(n / ni)
            return resultado
        else:
            return 0  # "Erro: i e ni devem ser diferentes e maiores que 0"
