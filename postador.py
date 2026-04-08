import json
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def formatar_mensagem(produto):
    preco = produto.get('preco_atual', 0)
    titulo = produto.get('titulo', 'Produto Sem Nome')
    link = produto.get('link', '#')
    desconto = produto.get('desconto', 'Oferta!')

    return (
        f"🔥 *OFERTA NO ATLETA OFERTAS* 🔥\n\n"
        f"🏆 *{titulo[:60]}...*\n"
        f"📉 *Status:* {desconto}\n"
        f"💰 *Preço:* R$ {preco:.2f}\n\n"
        f"🛒 *COMPRE AQUI:* {link}\n\n"
        f"⚠️ _Preço sujeito a alteração a qualquer momento._\n"
        f"------------------------------------------\n"
    )

def gerar_relatorio():
    caminho_json = os.path.join(BASE_DIR, 'scraper_atleta', 'ofertas_academia.json')
    caminho_txt = os.path.join(BASE_DIR, 'POSTAGENS_WHATSAPP.txt')
    
    if not os.path.exists(caminho_json):
        print(f"❌ Erro: JSON nao encontrado.")
        return

    with open(caminho_json, 'r', encoding='utf-8') as f:
        ofertas = json.load(f)

    # --- LÓGICA DE CURADORIA (QA ANTI-RUÍDO) ---
    PALAVRAS_BLOQUEADAS = [
        'escova', 'secadora', 'botina', 'ferramentas', 'bivolt', 'carro', 
        'moto', 'pneu', 'cozinha', 'soquetes', 'furadeira', 'maquiagem',
        'bracol', 'sapato', 'botas de segurança', 'compressor'
    ]

    ofertas_unicas = []
    ids_vistos = set()

    # Ordenar por menor preço ou maior desconto
    ofertas_ordenadas = sorted(ofertas, key=lambda x: x.get('preco_atual', 999))

    for item in ofertas_ordenadas:
        titulo_limpo = item.get('titulo', '').lower()
        link = item.get('link', '')

        # 1. Teste de Filtro: Se tiver alguma palavra da lista negra, pula o item
        if any(palavra in titulo_limpo for palavra in PALAVRAS_BLOQUEADAS):
            continue

        # 2. Teste de Duplicidade (Regex MLB)
        match = re.search(r'(MLB-?\d+)', link)
        produto_id = match.group(1).replace('-', '') if match else link

        if produto_id not in ids_vistos:
            ofertas_unicas.append(item)
            ids_vistos.add(produto_id)

    # Grava o arquivo final com a nata do fitness
    with open(caminho_txt, 'w', encoding='utf-8') as f_out:
        for i, item in enumerate(ofertas_unicas[:15]): 
            f_out.write(formatar_mensagem(item))
            print(f"✅ Card {i+1} aprovado: {item.get('titulo')[:30]}...")

    print(f"\n✨ Curadoria finalizada! Ruídos removidos.")