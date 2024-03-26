########## Url.py ##########
class Url:
    """
    A classe Url representa uma página web.

    Cada objeto da classe Url contém a URL da página web, o título da página, todos os subtítulos da página, todos os links da página, todos os parágrafos da página, todas as imagens da página, todas as listas da página e todas as tabelas da página.

    Atributos:
    \n\t`url (str)`: A URL da página web.
    \n\t`page (bs4.element.Tag)`: O título da página web.
    \n\t`titles (bs4.element.ResultSet)`: Todos os subtítulos da página web.
    \n\t`links (bs4.element.ResultSet)`: Todos os links da página web.
    \n\t`paragrafos (bs4.element.ResultSet)`: Todos os parágrafos da página web.
    \n\t`imagens (bs4.element.ResultSet)`: Todas as imagens da página web.
    \n\t`listas (bs4.element.ResultSet)`: Todas as listas da página web.
    \n\t`tabelas (bs4.element.ResultSet)`: Todas as tabelas da página web.

    Exemplo:
    >>> from bs4 import BeautifulSoup
    >>> import requests
    >>> response = requests.get("https://www.ifmg.edu.br")
    >>> soup = BeautifulSoup(response.text, 'html.parser')
    >>> url_obj = Url("https://www.ifmg.edu.br", soup)
    >>> print(url_obj.url)
    "https://www.ifmg.edu.br"
    >>> print(url_obj.page.text)
    "IFMG - Instituto Federal de Minas Gerais"
    >>> print(len(url_obj.titles))
    5
    >>> print(len(url_obj.links))
    128
    >>> print(len(url_obj.paragrafos))
    12
    >>> print(len(url_obj.imagens))
    20
    >>> print(len(url_obj.listas))
    10
    >>> print(len(url_obj.tabelas))
    2
    """

    def __init__(self, url, soup) -> None:
        """
        O construtor da classe Url.

        Este método é chamado automaticamente quando um objeto da classe Url é criado. Ele inicializa a URL da página web, o título da página, todos os subtítulos da página, todos os links da página, todos os parágrafos da página, todas as imagens da página, todas as listas da página e todas as tabelas da página.

        Parâmetros:
        \n\t`url (str)`: A URL da página web.
        \n\t`soup (bs4.BeautifulSoup)`: Um objeto BeautifulSoup que contém o conteúdo da página web.

        Retorno:
        \n\t`None`
        """
        self.url = url
        self.page = soup.find('title')
        self.titles = soup.find_all('h2')
        self.links = soup.find_all('a', href=True)
        self.paragrafos = soup.find_all('p')
        self.imagens = soup.find_all('img')
        self.listas = soup.find_all(['ul', 'ol'])
        self.tabelas = soup.find_all('table')
