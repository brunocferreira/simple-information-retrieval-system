########## Buscador.py ##########
import json
import nltk


class Buscador:
    """
    A classe Buscador é responsável por realizar pesquisas em um índice invertido.

    Cada objeto da classe Buscador contém um índice invertido que é carregado de um arquivo JSON.

    Atributos:
    \n\t`inverted_index (dict)`: Um dicionário que armazena o índice invertido.

    Métodos:
    \n\t`__init__(index_file)`: O construtor da classe Buscador. Este método é chamado automaticamente quando um objeto da classe Buscador é criado. Ele inicializa o índice invertido que é carregado de um arquivo JSON.
    \n\t`deep_search(query)`: Realiza uma pesquisa em profundidade no índice invertido. Este método tokeniza a consulta de pesquisa e, para cada token na consulta de pesquisa, percorre todas as chaves no índice invertido. Se o token estiver na chave, ele percorre todos os itens na lista de valores da chave e adiciona o item ao conjunto de links relevantes.
    \n\t`width_search(query)`: Realiza uma pesquisa em largura no índice invertido. Este método tokeniza a consulta de pesquisa e, para cada chave no índice invertido, percorre todos os tokens na consulta de pesquisa. Se o token estiver na chave, ele percorre todos os itens na lista de valores da chave e adiciona o item ao conjunto de links relevantes.

    Exemplo:
    >>> buscador = Buscador("index-Root.json")
    >>> resultados = buscador.deep_search("IFMG")
    >>> print(resultados)
    {"https://www.ifmg.edu.br"}
    >>> resultados = buscador.width_search("IFMG")
    >>> print(resultados)
    {"https://www.ifmg.edu.br"}
    """

    def __init__(self, index_file) -> None:
        """
        O construtor da classe Buscador.

        Este método é chamado automaticamente quando um objeto da classe Buscador é criado. Ele inicializa o índice invertido que é carregado de um arquivo JSON.

        Parâmetros:
        \n\t`index_file (str)`: O nome do arquivo JSON que contém o índice invertido.

        Retorno:
        \n\t`None`
        """
        with open(index_file, 'r') as file:
            self.inverted_index = json.load(file)

    def deep_search(self, query) -> set:
        """
        Realiza uma pesquisa em profundidade no índice invertido.

        Este método tokeniza a consulta de pesquisa e, para cada token na consulta de pesquisa, percorre todas as chaves no índice invertido. Se o token estiver na chave, ele percorre todos os itens na lista de valores da chave e adiciona o item ao conjunto de links relevantes.

        Parâmetros:
        \n\t`query (str)`: A consulta de pesquisa.

        Retorno:
        \n\t`set`: Um conjunto de links relevantes para a consulta de pesquisa.
        """
        query_tokens = nltk.word_tokenize(query)
        relevant_links = set()
        for token in query_tokens:
            for chave in self.inverted_index.keys():
                if token in chave:
                    for item in self.inverted_index[chave].keys():
                        relevant_links.add(item)
                    break
        return relevant_links

    def width_search(self, query) -> set:
        """
        Realiza uma pesquisa em largura no índice invertido.

        Este método tokeniza a consulta de pesquisa e, para cada chave no índice invertido, percorre todos os tokens na consulta de pesquisa. Se o token estiver na chave, ele percorre todos os itens na lista de valores da chave e adiciona o item ao conjunto de links relevantes.

        Parâmetros:
        \n\t`query (str)`: A consulta de pesquisa.

        Retorno:
        \n\t`set`: Um conjunto de links relevantes para a consulta de pesquisa.
        """
        query_tokens = nltk.word_tokenize(query)
        relevant_links = set()
        for chave in self.inverted_index.keys():
            for token in query_tokens:
                if token in chave:
                    for item in self.inverted_index[chave].keys():
                        relevant_links.add(item)
                    break
        return relevant_links
