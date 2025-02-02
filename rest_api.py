import requests

API_URL = "https://jsonplaceholder.typicode.com/todos"

def gerar_dados_elevador():
    import random
    return {
        "position": random.randint(0, 10),
        "door_status": random.choice(["open", "closed"]),
        "weight": random.randint(0, 1000)
    }

# Função para ler dados da nuvem
def get_data():
    response = requests.get(API_URL)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Falha ao recuperar dados: {response.status_code}")
        return None

# Function to send data to the cloud
def post_data():
    todo = {"userId": 2, "title": "Buy milk", "completed": False}
    response = requests.post(API_URL, json=todo)
    
    if response.status_code == 200:
        print(f"Dados enviados com sucesso")
        return response.json()
    else:
        print(f"Falha ao enviar dados: {response.status_code}")
        return None

# Uso
post_data()  # Envia os dados para a API
data = get_data()  # Recupera os dados da API

if data:
    print("Dados recebidos:", data)
