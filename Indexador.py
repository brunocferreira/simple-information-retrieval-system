########## Indexador.py ##########
import json
import nltk  # natural language tokenize
from bs4 import BeautifulSoup, element
# stop words
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')


class Indexador:
    """
    A classe Indexador é responsável por gerar um índice invertido a partir das páginas web coletadas por um objeto da classe Coletor.

    Cada objeto da classe Indexador contém um objeto da classe Coletor, uma lista de títulos tokenizados das páginas web coletadas, um conjunto de stop words em português e um dicionário que armazena o índice invertido.

    Atributos:
    \n\t`coletor (Coletor)`: Um objeto da classe Coletor.
    \n\t`tokenized_titles (list)`: Uma lista de títulos tokenizados das páginas web coletadas.
    \n\t`stop_words (set)`: Um conjunto de stop words em português.
    \n\t`inverted_index (dict)`: Um dicionário que armazena o índice invertido.

    Métodos:
    \n\t`inverted_index_generator()`: Gera o índice invertido a partir dos títulos tokenizados.
    \n\t`save_index()`: Salva o índice invertido em um arquivo JSON.
    \n\t`weight_tokenize()`: Atualiza os pesos dos tokens no índice invertido.
    \n\t`add_attr_inverted_index(params=None)`: Adiciona um ou mais atributos da Url ao índice invertido.
    \n\t`update_index()`: Atualiza o índice invertido com novos dados coletados.
    \n\t`remove_key_stop_words()`: Remove as stop words da lista de tokens.

    Exemplo:
    >>> coletor = Coletor("Root")
    >>> coletor.addUrl("https://www.ifmg.edu.br")
    >>> coletor.extrair_informacoes()
    >>> indexer = Indexador(coletor)
    >>> indexer.inverted_index_generator()
    >>> indexer.weight_tokenize()
    >>> indexer.add_attr_inverted_index()
    >>> indexer.update_index()
    >>> indexer.remove_key_stop_words()
    >>> indexer.save_index()
    index-Root.json = 128
    """

    def __init__(self, coletor) -> None:
        """
        O construtor da classe Indexador.

        Este método é chamado automaticamente quando um objeto da classe Indexador é criado. Ele inicializa o objeto da classe Coletor, a lista de títulos tokenizados, o conjunto de stop words e o dicionário do índice invertido.

        Parâmetros:
        \n\t`coletor (Coletor)`: Um objeto da classe Coletor.

        Retorno:
        \n\t`None`
        """
        self.coletor = coletor
        self.tokenized_titles = []
        self.stop_words = set(stopwords.words('portuguese'))
        self.inverted_index = {}

    def inverted_index_generator(self) -> None:
        """
        Gera o índice invertido.

        Este método percorre cada objeto Url na lista de objetos Url do coletor. Para cada título no objeto Url, ele tokeniza o texto do título, converte cada token para minúsculas, e adiciona o token à lista self.tokenized_titles se o token for alfanumérico e não for uma stop word. Em seguida, para cada token na lista self.tokenized_titles, ele adiciona o token ao índice invertido, apontando para a URL do objeto Url.

        Parâmetros:
        \n\t`None`

        Retorno:
        \n\t`None`
        """
        for object in self.coletor.objects_url:
            self.tokenized_titles = []  # reset the list for each Url object
            for title in object.titles:
                tokens = [token.lower() for token in nltk.word_tokenize(
                    title.text) if token.isalnum() and token.lower() not in self.stop_words]
                self.tokenized_titles.extend(tokens)

            for token in self.tokenized_titles:
                self.inverted_index.setdefault(
                    token, {}).update({object.url: 1.0})

    def save_index(self):
        """
        Salva o índice invertido em um arquivo JSON.

        Este método salva o índice invertido em um arquivo JSON com o nome "index-{codigo}.json", onde {codigo} é o código do coletor. Em seguida, ele imprime o nome do arquivo e o número de chaves no índice invertido.

        Parâmetros:
        \n\t`None`

        Retorno:
        \n\t`None`
        """
        filename = self.coletor.codigo
        with open(f"index-{filename}.json", 'w') as file:
            json.dump(self.inverted_index, file, indent=4)
        print(f"index-{filename}.json = {len(self.inverted_index.keys())}")

    def weight_tokenize(self) -> None:
        """
        Atualiza os pesos dos tokens no índice invertido.

        Este método percorre cada token no índice invertido e atualiza seu peso com base no número de links que ele possui. O token com o maior número de links recebe um peso de 1.0, e todos os outros tokens recebem um peso proporcional ao número de links que possuem em relação ao token com o maior número de links.

        Parâmetros:
        \n\t`None`

        Retorno:
        \n\t`None`
        """
        max_links = max(len(self.inverted_index[token])
                        for token in self.inverted_index)
        for token in self.inverted_index:
            self.inverted_index[token] = {url: len(
                self.inverted_index[token]) / max_links for url in self.inverted_index[token]}

    def add_attr_inverted_index(self, params=None) -> None:
        """
        Adiciona um ou mais atributos da Url ao índice invertido.

        Este método percorre cada objeto Url na lista de objetos Url do coletor. Para cada objeto Url, ele adiciona os atributos especificados em `params` ao índice invertido, apontando para a URL do objeto Url.

        Parâmetros:
        \n\t`params (list or None)`: Uma lista de atributos da Url a serem adicionados ao índice invertido. Se None, adiciona todos os atributos.

        Retorno:
        \n\t`None`
        """
        if params is None:
            params = ['page', 'titles', 'links', 'paragrafos',
                      'imagens', 'listas', 'tabelas']

        for object in self.coletor.objects_url:
            for attr in params:
                attribute = getattr(object, attr, None)
                if attribute is not None:
                    # Convert the attribute to a string if it's a BeautifulSoup Tag, ResultSet or NavigableString
                    if isinstance(attribute, (element.Tag, element.ResultSet, element.NavigableString)):
                        attribute = [str(item) for item in attribute]
                    self.inverted_index.setdefault(
                        attr, {}).update({object.url: attribute})

    def update_index(self, new_data) -> None:
        """
        Atualiza o índice invertido com novos dados coletados.

        Este método recebe novos dados na forma de um dicionário e atualiza o índice invertido existente com esses novos dados.

        Parâmetros:
        \n\t`new_data (dict)`: Um dicionário contendo os novos dados a serem adicionados ao índice invertido.

        Retorno:
        \n\t`None`
        """
        for key, value in new_data.items():
            if key in self.inverted_index:
                self.inverted_index[key].update(value)
            else:
                self.inverted_index[key] = value

    def remove_key_stop_words(self) -> None:
        """
        Remove as stop words da lista de tokens.

        Este método percorre todas as chaves no índice invertido e remove qualquer chave que seja uma stop word (e seu valor associado a ela).

        Parâmetros:
        \n\t`None`

        Retorno:
        \n\t`None`
        """
        for stop_word in self.stop_words:
            if stop_word in self.inverted_index:
                del self.inverted_index[stop_word]
