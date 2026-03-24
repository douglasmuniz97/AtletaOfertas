import scrapy

class AtletaOfertasSpider(scrapy.Spider):
    name = 'atleta_spider'
    start_urls = ['https://www.mercadolivre.com.br/ofertas?category=MLB1276']

    def parse(self, response):
        # Pegamos todos os blocos que parecem um card de produto
        for produto in response.xpath('//div[contains(@class, "promotion-item")] | //div[contains(@class, "poly-card")]'):
            # Busca o título em qualquer tag de texto dentro do card
            titulo = produto.xpath('.//a[contains(@class, "title")]/text() | .//p/text()').get()
            link = produto.xpath('.//a/@href').get()
            
            # Pegamos TODOS os números que aparecem no card (preço antigo e novo)
            precos = produto.xpath('.//span[contains(@class, "fraction")]/text()').getall()
            
            if len(precos) >= 2 and link:
                try:
                    p1 = float(precos[0].replace('.', '').replace(',', '.'))
                    p2 = float(precos[1].replace('.', '').replace(',', '.'))
                    
                    v_antigo = max(p1, p2)
                    v_atual = min(p1, p2)
                    
                    desconto = (1 - (v_atual / v_antigo)) * 100

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

        # Paginação: Vamos tentar o seletor padrão do ML para "Próximo"
        proxima = response.css('a.andes-pagination__button--next::attr(href)').get()
        if proxima:
            yield response.follow(proxima, self.parse)