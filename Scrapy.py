import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import Url


class LinkSpider(scrapy.Spider):
    name = "link_spider"

    def __init__(self, urls, *args, **kwargs):
        super(LinkSpider, self).__init__(*args, **kwargs)
        self.start_urls = urls
        self.objects_url = []

    def parse(self, response):
        # Usa o BeautifulSoup para analisar o HTML da página.
        soup = BeautifulSoup(response.text, 'html.parser')
        self.objects_url += [Url(response.url, soup)]


# A lista urls contém as URLs das páginas web que serão coletadas.
urls = ["https://www.ifmg.edu.br"]

# Inicia o processo do Scrapy e configura as configurações.
process = CrawlerProcess(settings={
    "FEEDS": {
        "items.json": {"format": "json"},
    },
})

# Inicia o spider.
process.crawl(LinkSpider, urls=urls)
process.start()  # O script irá bloquear aqui até que o crawling esteja terminado
