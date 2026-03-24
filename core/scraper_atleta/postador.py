import json

def organizar_visual_dev():
    try:
        with open('scraper_atleta/ofertas_academia.json', 'r', encoding='utf-8') as f:
            ofertas = json.load(f)
        
        # Ordenar por maior desconto antes de mostrar
        ofertas_ordenadas = sorted(ofertas, key=lambda x: int(x['desconto'].replace('%','')), reverse=True)

        print(f"\n{'='*80}")
        print(f"📊 RELATÓRIO DE GARIMPO - ATLETA OFERTAS | {len(ofertas)} ITENS ENCONTRADOS")
        print(f"{'='*80}\n")

        for i, item in enumerate(ofertas_ordenadas[:15], 1):
            print(f"{i:02d}. [{item['desconto']}] {item['titulo'][:50]}...")
            print(f"    💰 De: R$ {item['preco_antigo']:.2f} -> Por: R$ {item['preco_atual']:.2f}")
            print(f"    🔗 {item['link'][:60]}...\n")

    except FileNotFoundError:
        print("❌ Erro: Execute o crawler primeiro para gerar o JSON!")

if __name__ == "__main__":
    organizar_visual_dev()