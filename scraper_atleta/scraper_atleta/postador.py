import json
import os

# Pega o diretório onde este arquivo (postador.py) está localizado
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
        f"📉 *Status:* {desconto} OFF\n"
        f"💰 *Preço:* R$ {preco:.2f}\n\n"
        f"🛒 *COMPRE AQUI:* {link}\n\n"
        f"⚠️ _Preço sujeito a alteração a qualquer momento._\n"
        f"------------------------------------------\n"
    )
    return mensagem

def gerar_relatorio():
    # Caminho do JSON dentro da pasta do scraper
    caminho_json = os.path.join(BASE_DIR, 'scraper_atleta', 'ofertas_academia.json')
    # Caminho do TXT de saída na raiz do projeto
    caminho_txt = os.path.join(BASE_DIR, 'POSTAGENS_WHATSAPP.txt')
    
    if not os.path.exists(caminho_json):
        print(f"❌ Erro: Arquivo não encontrado em: {caminho_json}")
        return

    with open(caminho_json, 'r', encoding='utf-8') as f:
        ofertas = json.load(f)

    if not ofertas:
        print("⚠️ O arquivo JSON está vazio. Nenhuma oferta encontrada.")
        return

    # Ordenar pelas melhores ofertas (menor preço primeiro)
    ofertas_ordenadas = sorted(ofertas, key=lambda x: x.get('preco_atual', 999))

    print(f"\n🚀 Gerando Cards para as melhores ofertas encontradas...\n")
    
    with open(caminho_txt, 'w', encoding='utf-8') as f_out:
        # Pega as 15 melhores ofertas para ter um bom volume no WhatsApp
        for i, item in enumerate(ofertas_ordenadas[:15]): 
            card = formatar_mensagem(item)
            f_out.write(card)
            print(f"✅ Card {i+1} formatado: {item.get('titulo')[:30]}...")

    print(f"\n✨ PRONTO! O arquivo foi gerado em:\n{caminho_txt}")

if __name__ == "__main__":
    gerar_relatorio()