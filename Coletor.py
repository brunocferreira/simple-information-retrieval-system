########## Coletor.py ##########
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import urlparse, urljoin
from urllib.robotparser import RobotFileParser
import time
from Url import Url


class Coletor:
    """
    A classe Coletor é responsável por coletar páginas web.

    Cada objeto da classe Coletor contém um código, um dicionário de URLs a serem coletadas e uma lista de objetos da classe Url que foram criados a partir das URLs coletadas.

    Atributos:
    \n\t`codigo (str)`: Um código fornecido quando um objeto da classe Coletor é criado.
    \n\t`urls (dict)`: Um dicionário que armazena as URLs que serão coletadas. As chaves são as URLs e os valores são booleanos que indicam se a URL já foi coletada (True) ou não (False).
    \n\t`objects_url (list)`: Uma lista que armazena objetos da classe Url que foram criados a partir das URLs coletadas.

    Métodos:
    \n\t`addUrl(url)`: Adiciona uma nova URL ao dicionário self.urls, se ela ainda não estiver presente.
    \n\t`extrair_informacoes(params=None)`: Extrai informações das URLs que ainda não foram visitadas e que são permitidas pelo arquivo robots.txt.
    \n\t`can_fetch(url)`: Verifica se a coleta é permitida para a URL especificada pelo arquivo robots.txt.
    \n\t`extrair_em_profundidade(profundidade=0, params=None)`: Extrai informações das URLs até a profundidade especificada. Quando a profundidade é 0, este método extrai informações de todas as URLs do mesmo domínio que a primeira URL adicionada ao Coletor. Quando a profundidade é um valor diferente de 0, ele extrai informações das URLs até essa profundidade.

    Exemplo:
    >>> coletor = Coletor("Root")
    >>> coletor.addUrl("https://www.ifmg.edu.br")
    >>> coletor.extrair_em_profundidade()
    >>> print(len(coletor.objects_url))
    1
    """

    def __init__(self, codigo) -> None:
        """
        O construtor da classe Coletor.

        Este método é chamado automaticamente quando um objeto da classe Coletor é criado. Ele inicializa o código, o dicionário de URLs a serem coletadas e a lista de objetos da classe Url.

        Parâmetros:
        \n\t`codigo (str)`: Um código fornecido quando um objeto da classe Coletor é criado.

        Retorno:
        \n\t`None`
        """
        self.codigo = codigo
        self.urls = {}
        self.objects_url = []

    def addUrl(self, url) -> None:
        """
        Adiciona uma nova URL ao dicionário self.urls, se ela ainda não estiver presente.

        Parâmetros:
        \n\t`url (str)`: A URL a ser adicionada.

        Retorno:
        \n\t`None`
        """
        if url not in self.urls.keys():
            self.urls[url] = False

    def can_fetch(self, url) -> bool:
        """
        Verifica se é permitido extrair a URL de acordo com o arquivo "/robots.txt".

        Este método parseia a URL para obter o esquema e o netloc (por exemplo, 'http', 'www.ifmg.edu.br'). Em seguida, constrói a URL do arquivo robots.txt (por exemplo, 'http://www.ifmg.edu.br/robots.txt') e usa o RobotFileParser para analisar o arquivo robots.txt. Finalmente, verifica se é permitido extrair a URL de acordo com as regras especificadas no arquivo robots.txt.

        Parâmetros:
        \n\t`url (str)`: A URL a ser verificada.

        Retorno:
        \n\t`bool`: Retorna True se for permitido extrair a URL, False caso contrário.
        """
        parsed_url = urlparse(url)
        robots_url = urljoin(parsed_url.scheme + "://" +
                             parsed_url.netloc, "/robots.txt")
        rp = RobotFileParser()
        rp.set_url(robots_url)
        # rp.read()
        # return rp.can_fetch("*", url)
        try:
            rp.read()
            return rp.can_fetch("*", url)
        except:
            print(f"Não foi possível ler o arquivo robots.txt de {url}")
            return False

    def extrair_informacoes(self, params_page=None) -> None:
        """
        Extrai as informações das URLs que ainda não foram coletadas.

        Este método cria uma lista de URLs que ainda não foram coletadas. Em seguida, para cada URL na lista de URLs não coletadas, ele verifica se é permitido extrair a URL de acordo com o arquivo "/robots.txt". Se for permitido, ele tenta fazer uma requisição GET para a URL e, dependendo do tipo de `params_page`, ele usa diferentes métodos para processar a resposta.

        Parâmetros:
        \n\t`params_page (str, float, int or None)`: Um parâmetro que determina como processar a resposta da requisição GET. Se for uma `str`, ele usa o Selenium para carregar a página web e o BeautifulSoup para analisar o HTML da página. Se for um número do tipo `float`, ele aguarda esse número de segundos após a requisição antes de usar o BeautifulSoup para analisar o HTML da página. Se for None ou 0, ele usa o BeautifulSoup para analisar o HTML da página imediatamente após a requisição.

        Retorno:
        \n\t`None`
        """
        good_urls = [url for url in self.urls.keys() if not self.urls[url]]
        for url in good_urls:
            if self.can_fetch(url):
                if isinstance(params_page, str) and params_page == str:
                    self.driver = webdriver.Chrome()
                    self.driver.get(url)
                    soup = BeautifulSoup(
                        self.driver.page_source, 'html.parser')  # 'html.parser', 'lxml', 'html5lib'
                    self.objects_url += [Url(url, soup)]
                    self.urls[url] = True
                    self.driver.quit()
                elif isinstance(params_page, float):
                    response = requests.get(url, timeout=2000)
                    time.sleep(params_page)
                    if response.status_code == 200:
                        self.objects_url += [
                            Url(url, BeautifulSoup(response.text, 'html.parser'))]  # 'html.parser', 'lxml', 'html5lib'
                        self.urls[url] = True
                    else:
                        print(
                            f"Falha ao carregar a página: {response.status_code}")
                else:
                    response = requests.get(url, timeout=2000)
                    if response.status_code == 200:
                        self.objects_url += [Url(url,
                                                 BeautifulSoup(response.text, 'html.parser'))]  # 'html.parser', 'lxml', 'html5lib'
                        self.urls[url] = True
                    else:
                        print(
                            f"Falha ao carregar a página: {response.status_code}")
            else:
                print(
                    f"A coleta da URL {url} é proibida pelo arquivo robots.txt.")

    def extrair_em_profundidade(self, profundidade=0, params=None) -> None:
        """
        Extrai informações das URLs até a profundidade especificada.

        Quando a profundidade é 0, este método extrai informações de todas as URLs do mesmo domínio que a primeira URL adicionada ao Coletor. Quando a profundidade é um valor diferente de 0, ele extrai informações das URLs até essa profundidade.

        Parâmetros:
        \n\t`profundidade (int)`: A profundidade até a qual as informações das URLs devem ser extraídas. O valor padrão é 0, o que significa que as informações de todas as URLs do mesmo domínio que a primeira URL serão extraídas.
        \n\t`params`: Parâmetros adicionais que podem ser passados para o método `extrair_informacoes`. O valor padrão é None.

        Retorno:
        \n\t`None`
        """
        if profundidade == 0:
            # Extrair todos os links do mesmo domínio que o URL inicial
            url_inicial = list(self.urls.keys())[0]
            dominio = urlparse(url_inicial).netloc
            good_urls = [url for url in self.urls.keys() if urlparse(
                url).netloc == dominio and not self.urls[url]]
            for url in good_urls:
                self.extrair_informacoes(params)
        else:
            # Extrair links até a profundidade especificada
            for i in range(profundidade):
                good_urls = [url for url in self.urls.keys()
                             if not self.urls[url]]
                if not good_urls:
                    break
                self.extrair_informacoes(params)
