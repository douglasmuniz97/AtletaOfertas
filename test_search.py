from core.auth_manager import requisicao_segura
import json

def buscar_ofertas_por_categoria(categoria_id):
    print(f"🔍 Buscando as melhores ofertas na categoria {categoria_id}...")
    
    # Endpoint de busca
    url = f"https://api.mercadolibre.com/sites/MLB/search?category={categoria_id}&status=active&limit=10"
    
    # Adicionamos um User-Agent para evitar o erro 403 de segurança
    # Isso simula uma requisição vinda de um navegador comum
    headers_extras = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # Note que passamos os headers extras aqui (se sua função requisicao_segura permitir)
        # Se sua função atual NÃO aceita headers extras, vamos ajustar ela abaixo.
        response = requisicao_segura(url, metodo='GET')
        
        if response.status_code == 200:
            dados = response.json()
            resultados = dados.get('results', [])
            print(f"✅ Encontrados {len(resultados)} produtos.\n")
            
            for item in resultados:
                nome = item.get('title')
                preco = item.get('price')
                link = item.get('permalink')
                print(f"🛍️ {nome} - R$ {preco}")
                print(f"🔗 {link}\n")
        else:
            print(f"❌ Erro na busca: {response.status_code}")
            print(f"Mensagem da API: {response.text}") # Isso nos ajuda a debugar o motivo exato
            
    except Exception as e:
        print(f"⚠️ Erro inesperado: {e}")

if __name__ == "__main__":
    buscar_ofertas_por_categoria("MLB1430")