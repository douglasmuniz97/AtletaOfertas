import scrapy

class AtletaOfertasSpider(scrapy.Spider):
    name = 'atleta_spider'
    
    # Lista de termos estratégicos para diversificar o Atleta Ofertas
    termos_busca = [
        'creatina%20monohidratada',
        'whey%20protein',
        'smartband%20esportivo',
        'fone%20bluetooth%20corrida',
        'kit%20camiseta%20dry%20fit',
        'shorts%20treino%20masculino',
        'joelheira%20compressao',
        'balanca%20bioimpedancia',
        'pasta%20de%20amendoim%201kg'
    ]

    # Gerando as URLs de ofertas automaticamente para cada termo
    start_urls = [
        f'https://www.mercadolivre.com.br/ofertas?container_id=MLB779362-1&keyword={termo}' 
        for termo in termos_busca
    ]

    def parse(self, response):
        # Pegamos todos os blocos que parecem um card de produto
        for produto in response.xpath('//div[contains(@class, "promotion-item")] | //div[contains(@class, "poly-card")]'):
            # Busca o título
            titulo = produto.xpath('.//a[contains(@class, "title")]/text() | .//p/text() | .//h3/text()').get()
            link = produto.xpath('.//a/@href').get()
            
            # Pegamos os números que aparecem no card (preço antigo e novo)
            precos = produto.xpath('.//span[contains(@class, "fraction")]/text()').getall()
            
            if len(precos) >= 2 and link:
                try:
                    p1 = float(precos[0].replace('.', '').replace(',', '.'))
                    p2 = float(precos[1].replace('.', '').replace(',', '.'))
                    
                    v_antigo = max(p1, p2)
                    v_atual = min(p1, p2)
                    
                    desconto = (1 - (v_atual / v_antigo)) * 100

                    # Mantemos o filtro de 25% para garantir que só venha promoção boa
                    if desconto >= 25:
                        yield {
                            'titulo': titulo.strip() if titulo else "Produto Academia",
                            'preco_antigo': v_antigo,
                            'preco_atual': v_atual,
                            'desconto': f"{desconto:.0f}%",
                            'link': link
                        }
                except:
                    continue

        # Paginação para varrer mais de uma página de cada termo
        proxima = response.css('a.andes-pagination__button--next::attr(href)').get()
        if proxima:
            yield response.follow(proxima, self.parse)