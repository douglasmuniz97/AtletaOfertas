from core import requisicao_segura

def consultar_meu_perfil():
    print("🚀 Iniciando requisição ao Mercado Livre...")
    
    # Endpoint para ver os dados da sua própria conta
    url = "https://api.mercadolibre.com/users/me"
    
    # Chamamos a função que cuida do token e do refresh automático
    response = requisicao_segura(url, metodo='GET')
    
    if response.status_code == 200:
        dados = response.json()
        print("\n✅ CONEXÃO ESTABELECIDA!")
        print(f"Usuário: {dados['nickname']}")
        print(f"ID da Conta: {dados['id']}")
        print(f"E-mail: {dados['email']}")
    else:
        print(f"\n❌ Falha na conexão: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    consultar_meu_perfil()