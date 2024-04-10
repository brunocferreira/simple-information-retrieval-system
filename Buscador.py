########## Buscador.py ##########
import json
import nltk
from Expressoes import Expressoes


class Buscador:
    """
    A classe Buscador realiza buscas em um índice invertido.

    Atributos:
    \n\t`inverted_index (dict)`: O índice invertido onde a busca será realizada.

    Métodos:
    \n\t`__init__(self, index_file: str)`: Inicializa um objeto Buscador com o índice invertido contido no arquivo especificado.
    \n\t`deep_search(self, query: str) -> set`: Realiza uma busca em profundidade no índice invertido.
    \n\t`width_search(self, query: str) -> set`: Realiza uma busca em largura no índice invertido.
    \n\t`rank(self, query: str) -> list`: Realiza um ranqueamento dos documentos com base na consulta de pesquisa.

    Exemplo de uso:
    \n\tbuscador = Buscador("index_file.json")
    \n\tresult = buscador.deep_search("consulta de pesquisa")
    \n\tprint(result)
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

    def rank(self, query) -> set:
        """
        Realiza um ranqueamento dos documentos com base na consulta de pesquisa.

        Este método tokeniza a consulta de pesquisa e, para cada token no índice invertido, verifica se o token está na consulta. Se estiver, ele percorre cada URL associada ao token no índice invertido, obtém a frequência do token na URL (i), o número total de documentos (n) e o número de documentos em que o token ocorre (ni). Em seguida, calcula o peso do token na consulta (wiq) e adiciona o peso do token à pontuação da URL. Finalmente, classifica as URLs com base em suas pontuações em ordem decrescente.

        Parâmetros:
        \n\t`query (str)`: A consulta de pesquisa.

        Retorno:
        \n\t`list`: Uma lista de URLs classificadas em ordem decrescente de pontuação.
        """
        query_tokens = nltk.word_tokenize(query)

        scores = {}

        for token in self.inverted_index.keys():
            if token in query_tokens:
                for url in self.inverted_index[token].keys():
                    i, n, ni, _ = self.inverted_index[token][url]

                    wiq = Expressoes.calcular_wiq(i, n, ni)

                    if url not in scores:
                        scores[url] = 0

                    scores[url] += wiq

        ranked_urls = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        return ranked_urls
