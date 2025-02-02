import requests

API_URL = "https://jsonplaceholder.typicode.com/todos"

def gerar_dados_elevador(id):
    import random
    id = int(id)
    return {
        "elevator_id": id,
        "position": random.randint(0, 10),
        "door_status": random.choice(["open", "closed"]),
        "weight": random.randint(0, 1000)
    }

# Função para ler dados da nuvem
def get_data():
    response = requests.get(API_URL)
    
    if response.status_code == 200:
        # Se a resposta for uma lista, você pode pegar o primeiro item ou iterar.
        return response.json()
    else:
        print(f"Falha ao recuperar dados: {response.status_code}")
        return None

# Function to send data to the cloud
def post_data(dados):
    response = requests.post(API_URL, json=dados)
    print(f"Resposta do servidor após POST: {response.status_code} - {response.text}")  # Verifique a resposta do servidor
    
    if response.status_code in [200, 201]:
        print(f"Dados enviados com sucesso")
        return response.json()
    else:
        print(f"Falha ao enviar dados: {response.status_code}")
        return None

# Função para verificar os dados
def verificar_e_printer_json(dados):
    chaves_esperadas = ["elevator_id", "position", "door_status", "weight"]
    
    # Verificar se o item é um dicionário (único objeto)
    if isinstance(dados, dict):
        if all(chave in dados for chave in chaves_esperadas):
            for chave, valor in dados.items():
                print(f"{chave}: {valor}")
        else:
            print(".", end="")
    elif isinstance(dados, list):  # Se for uma lista, itere pelos itens
        for item in dados:
            verificar_e_printer_json(item)

# Uso
post_data(gerar_dados_elevador(1))  # Envia os dados para a API
data = get_data()  # Recupera os dados da API

# if data:
#     verificar_e_printer_json(data)  # Verifica e imprime os dados
