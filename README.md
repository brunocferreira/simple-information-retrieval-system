# Especialização em Inteligência Artificial – IFMG

# Atividade Final da disciplina de Recuperação da Informação

**Aluno**: Bruno da Cunha Ferreira
**Professor**: Dr. Moisés Henrique Ramos Pereira - IFMG

## Objetivo

Elaborar um sistema simples de recuperação da informação

## Descritivo de cada classe do sistema

### Url.py

A classe Url representa uma página web.

Cada objeto da classe Url contém a URL da página web, o título da página, todos os subtítulos da página, todos os links da página, todos os parágrafos da página, todas as imagens da página, todas as listas da página e todas as tabelas da página.

Atributos:

> - `url (str)`: A URL da página web.
> - `page (bs4.element.Tag)`: O título da página web.
> - `titles (bs4.element.ResultSet)`: Todos os subtítulos da página web.
> - `links (bs4.element.ResultSet)`: Todos os links da página web.
> - `paragrafos (bs4.element.ResultSet)`: Todos os parágrafos da página web.
> - `imagens (bs4.element.ResultSet)`: Todas as imagens da página web.
> - `listas (bs4.element.ResultSet)`: Todas as listas da página web.
> - `tabelas (bs4.element.ResultSet)`: Todas as tabelas da página web.

Exemplo:

> > > from bs4 import BeautifulSoup
> > > import requests
> > > response = requests.get("https://www.ifmg.edu.br")
> > > soup = BeautifulSoup(response.text, 'html.parser')
> > > url_obj = Url("https://www.ifmg.edu.br", soup)
> > > print(url_obj.url)
> > > "https://www.ifmg.edu.br"
> > > print(url_obj.page.text)
> > > "IFMG - Instituto Federal de Minas Gerais"
> > > print(len(url_obj.titles))
> > > 5
> > > print(len(url_obj.links))
> > > 128
> > > print(len(url_obj.paragrafos))
> > > 12
> > > print(len(url_obj.imagens))
> > > 20
> > > print(len(url_obj.listas))
> > > 10
> > > print(len(url_obj.tabelas))
> > > 2

### Coletor.py

A classe Coletor é responsável por coletar páginas web.

Cada objeto da classe Coletor contém um código, um dicionário de URLs a serem coletadas e uma lista de objetos da classe Url que foram criados a partir das URLs coletadas.

Atributos:

> - `codigo (str)`: Um código fornecido quando um objeto da classe Coletor é criado.
> - `urls (dict)`: Um dicionário que armazena as URLs que serão coletadas. As chaves são as URLs e os valores são booleanos que indicam se a URL já foi coletada (True) ou não (False).
> - `objects_url (list)`: Uma lista que armazena objetos da classe Url que foram criados a partir das URLs coletadas.

Métodos:

> - `addUrl(url)`: Adiciona uma nova URL ao dicionário self.urls, se ela ainda não estiver presente.
> - `extrair_informacoes(params=None)`: Extrai informações das URLs que ainda não foram visitadas e que são permitidas pelo arquivo robots.txt.
> - `can_fetch(url)`: Verifica se a coleta é permitida para a URL especificada pelo arquivo robots.txt.
> - `extrair_em_profundidade(profundidade=0, params=None)`: Extrai informações das URLs até a profundidade especificada. Quando a profundidade é 0, este método extrai informações de todas as URLs do mesmo domínio que a primeira URL adicionada ao Coletor. Quando a profundidade é um valor diferente de 0, ele extrai informações das URLs até essa profundidade.

Exemplo:

> > > coletor = Coletor("Root")
> > > coletor.addUrl("https://www.ifmg.edu.br")
> > > coletor.extrair_em_profundidade()
> > > print(len(coletor.objects_url))
> > > 1

### SistemaRI.py

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

> > > python SistemaRI.py
> > > O que você deseja pesquisar? IFMG
> > > https://www.ifmg.edu.br/portal

### Indexador.py

A classe Indexador é responsável por gerar um índice invertido a partir das páginas web coletadas por um objeto da classe Coletor.

Cada objeto da classe Indexador contém um objeto da classe Coletor, uma lista de títulos tokenizados das páginas web coletadas, um conjunto de stop words em português e um dicionário que armazena o índice invertido.

Atributos:

> - `coletor (Coletor)`: Um objeto da classe Coletor.
> - `tokenized_titles (list)`: Uma lista de títulos tokenizados das páginas web coletadas.
> - `stop_words (set)`: Um conjunto de stop words em português.
> - `inverted_index (dict)`: Um dicionário que armazena o índice invertido.

Métodos:

> - `inverted_index_generator()`: Gera o índice invertido a partir dos títulos tokenizados.
> - `save_index()`: Salva o índice invertido em um arquivo JSON.
> - `weight_tokenize()`: Atualiza os pesos dos tokens no índice invertido.
> - `add_attr_inverted_index(params=None)`: Adiciona um ou mais atributos da Url ao índice invertido.
> - `update_index()`: Atualiza o índice invertido com novos dados coletados.
> - `remove_key_stop_words()`: Remove as stop words da lista de tokens.

Exemplo:

> > > coletor = Coletor("Root")
> > > coletor.addUrl("https://www.ifmg.edu.br")
> > > coletor.extrair_informacoes()
> > > indexer = Indexador(coletor)
> > > indexer.inverted_index_generator()
> > > indexer.weight_tokenize()
> > > indexer.add_attr_inverted_index()
> > > indexer.update_index()
> > > indexer.remove_key_stop_words()
> > > indexer.save_index()
> > > index-Root.json = 128

### Buscador.py

A classe Buscador é responsável por realizar pesquisas em um índice invertido.

Cada objeto da classe Buscador contém um índice invertido que é carregado de um arquivo JSON.

Atributos:

> - `inverted_index (dict)`: Um dicionário que armazena o índice invertido.

Métodos:

> - `__init__(index_file)`: O construtor da classe Buscador. Este método é chamado automaticamente quando um objeto da classe Buscador é criado. Ele inicializa o índice invertido que é carregado de um arquivo JSON.
> - `deep_search(query)`: Realiza uma pesquisa em profundidade no índice invertido. Este método tokeniza a consulta de pesquisa e, para cada token na consulta de pesquisa, percorre todas as chaves no índice invertido. Se o token estiver na chave, ele percorre todos os itens na lista de valores da chave e adiciona o item ao conjunto de links relevantes.
> - `width_search(query)`: Realiza uma pesquisa em largura no índice invertido. Este método tokeniza a consulta de pesquisa e, para cada chave no índice invertido, percorre todos os tokens na consulta de pesquisa. Se o token estiver na chave, ele percorre todos os itens na lista de valores da chave e adiciona o item ao conjunto de links relevantes.

Exemplo:

> > > buscador = Buscador("index-Root.json")
> > > resultados = buscador.deep_search("IFMG")
> > > print(resultados)
> > > {"https://www.ifmg.edu.br"}
> > > resultados = buscador.width_search("IFMG")
> > > print(resultados)
> > > {"https://www.ifmg.edu.br"}
