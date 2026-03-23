from core.auth_manager import requisicao_segura

def replicar_endpoint_categorias():
    print("🚀 Iniciando teste do endpoint de categorias...")
    url = "https://api.mercadolibre.com/sites/MLB/categories"
    
    response = requisicao_segura(url, metodo='GET')
    
    if response.status_code == 200:
        dados = response.json()
        print(f"\n✅ SUCESSO! Status: {response.status_code}")
        for cat in dados[:10]:
            print(f"ID: {cat['id']} | Nome: {cat['name']}")
    else:
        print(f"\n❌ Falha: {response.status_code}")

if __name__ == "__main__":
    replicar_endpoint_categorias()