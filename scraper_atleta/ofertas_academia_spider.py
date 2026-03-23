import scrapy

class AtletaOfertasSpider(scrapy.Spider):
    name = 'atleta_spider'
    # URL da categoria Esportes e Fitness no Mercado Livre
    start_urls = ['https://www.mercadolivre.com.br/ofertas?category=MLB1276']

    def parse(self, response):
        for produto in response.css('div.andes-card'):
            # Seletores CSS para capturar os dados
            titulo = produto.css('p.promotion-item__title::text').get()
            preco_atual = produto.css('span.andes-money-amount__fraction::text').get()
            preco_antigo = produto.css('s.andes-money-amount__item span.andes-money-amount__fraction::text').get()
            link = produto.css('a.promotion-item__link-container::attr(href)').get()

            if preco_antigo and preco_atual:
                # Lógica de QA: Calcular o desconto real
                valor_antigo = float(preco_antigo.replace('.', '').replace(',', '.'))
                valor_atual = float(preco_atual.replace('.', '').replace(',', '.'))
                desconto = (1 - (valor_atual / valor_antigo)) * 100

                # Só envia para o Atleta Ofertas se for >= 25%
                if desconto >= 25:
                    yield {
                        'titulo': titulo,
                        'preco_antigo': valor_antigo,
                        'preco_atual': valor_atual,
                        'desconto': f"{desconto:.0f}%",
                        'link': link
                    }

        # Lógica para ir para a próxima página automaticamente
        proxima_pagina = response.css('li.andes-pagination__button--next a::attr(href)').get()
        if proxima_pagina:
            yield response.follow(proxima_pagina, self.parse)