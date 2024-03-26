########## SistemaRI.py ##########
from Coletor import Coletor
from Indexador import Indexador
from Buscador import *

"""
Este script realiza as seguintes etapas:

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

Exemplo:
>>> python SistemaRI.py
O que você deseja pesquisar? IFMG
https://www.ifmg.edu.br/portal
"""

# A lista urls contém as URLs das páginas web que serão coletadas.
urls = ["https://www.ifmg.edu.br/portal",
        "https://www.ifmg.edu.br/portal/sobre-o-ifmg/contato",
        "https://www.google.com/search?q=unidades+do+ifmg&ie=UTF-8",
        "https://www.google.com/maps/search?q=unidades+do+ifmg&ie=UTF-8",
        "https://brunosites.app.br",
        "https://brunosites.app.br/admin/"]

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

# O índice invertido é atualizado os pesos.
indexer.weight_tokenize()

# O índice invertido é atualizado os pesos.
indexer.add_attr_inverted_index()

# O índice invertido é salvo em um arquivo JSON.
indexer.save_index()

# O usuário é solicitado a inserir uma consulta de pesquisa.
query = input("O que você deseja pesquisar? ")

# Um objeto da classe Buscador é criado com o nome do arquivo do índice invertido.
searcher = Buscador("index-Root.json")

# A consulta de pesquisa é pesquisada no índice invertido.
results = searcher.deep_search(query)

# Os resultados da pesquisa são impressos.
for result in results:
    print(result)
