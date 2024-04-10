########## SistemaRI.py ##########
from Coletor import Coletor
from Indexador import Indexador
from Buscador import *

"""
O script SistemaRI.py é um sistema de recuperação de informações que realiza as seguintes etapas:

1. Cria um objeto da classe Coletor.
2. Adiciona URLs ao coletor.
3. Extrai as informações das URLs adicionadas ao coletor.
4. Cria um objeto da classe Indexador com o coletor.
5. Gera um índice invertido.
6. Salva o índice invertido em um arquivo JSON.
7. Solicita ao usuário que insira uma consulta de pesquisa.
8. Cria um objeto da classe Buscador com o nome do arquivo do índice invertido.
9. Pesquisa a consulta de pesquisa no índice invertido.
10. Imprime os resultados da pesquisa.

Exemplo de uso:
>>> python SistemaRI.py
O que você deseja pesquisar? IFMG
https://www.ifmg.edu.br/portal
"""

# A lista urls contém as URLs das páginas web que serão coletadas.
urls = ["https://g1.globo.com",
        "https://www.r7.com",
        "https://band.uol.com.br",
        "https://fatoreal.com.br",
        "https://jornalvozativa.com",
        "https://www.ribeiraodasneves.net",
        "https://www.ribeiraodasneves.net",
        "https://redeminas.tv",
        "http://brunosites.app.br",
        "http://brunosites.app.br/admin/"]

# Um objeto da classe Coletor é criado com o código "Root".
coletor = Coletor("Root")

# Para cada URL na lista urls, a URL é adicionada ao coletor.
for url in urls:
    coletor.addUrl(url)

# As informações das URLs adicionadas ao coletor são extraídas.
# coletor.extrair_informacoes(5.0)
coletor.extrair_em_profundidade(0, 5.0)

# Um objeto da classe Indexador é criado com o coletor.
indexer = Indexador(coletor)

# O índice invertido é gerado.
indexer.inverted_index_generator()

# O índice invertido é salvo em um arquivo JSON.
indexer.save_index()

# # Um objeto da classe Buscador é criado com o nome do arquivo do índice invertido.
searcher = Buscador("index-Root.json")

buscar = "sim"

while (buscar == "sim" or buscar == "" or buscar == "s" or buscar == "y" or buscar == "yes"):
    # O usuário é solicitado a inserir uma consulta de pesquisa.
    query = input("O que você deseja pesquisar? ")

    # A consulta de pesquisa é pesquisada no índice invertido.
    results = searcher.rank(query)

    # Os resultados da pesquisa são impressos.
    for result in results:
        print(result)

    buscar = input("Deseja realizar uma nova busca? ")
