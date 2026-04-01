import json
import os

def formatar_mensagem(produto):
    # Lógica de "Copywriting" para o Atleta Ofertas
    preco = produto.get('preco_atual', 0)
    titulo = produto.get('titulo', 'Produto Sem Nome')
    link = produto.get('link', '#')
    desconto = produto.get('desconto', 'Oferta!')

    # Montando o Card de Oferta com Emojis
    mensagem = (
        f"🔥 *OFERTA NO ATLETA OFERTAS* 🔥\n\n"
        f"🏆 *{titulo[:60]}...*\n"
        f"📉 *Status:* {desconto}\n"
        f"💰 *Preço:* R$ {preco:.2f}\n\n"
        f"🛒 *COMPRE AQUI:* {link}\n\n"
        f"⚠️ _Preço sujeito a alteração a qualquer momento._\n"
        f"------------------------------------------\n"
    )
    return mensagem

def gerar_relatorio():
    caminho_json = r'C:\AtletaOfertas\core\scraper_atleta\ofertas_academia.json'
    
    if not os.path.exists(caminho_json):
        print("❌ Erro: O arquivo de ofertas do ML não foi encontrado!")
        return

    with open(caminho_json, 'r', encoding='utf-8') as f:
        ofertas = json.load(f)

    # Ordenar pelas melhores ofertas (menor preço primeiro, ou critério de desconto)
    ofertas_ordenadas = sorted(ofertas, key=lambda x: x.get('preco_atual', 999))

    print(f"\n🚀 Gerando {len(ofertas_ordenadas)} Cards de Ofertas...\n")
    
    with open('POSTAGENS_WHATSAPP.txt', 'w', encoding='utf-8') as f_out:
        for i, item in enumerate(ofertas_ordenadas[:10]): # Pega as 10 melhores
            card = formatar_mensagem(item)
            f_out.write(card)
            print(f"✅ Card {i+1} gerado com sucesso!")

    print("\n✨ PRONTO! Abra o arquivo 'POSTAGENS_WHATSAPP.txt' e comece a lucrar!")

if __name__ == "__main__":
    gerar_relatorio()