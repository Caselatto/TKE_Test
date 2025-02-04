import random

# Dicionário de informações a serem medidas
chaves = ["elevator_id", "position", "door_status", "weight"]   # Caso deseje adicionar mais informações,
                                                                # necessário apenas adicionar o nome aqui
                                                                # e fazer a aquisição abaixo

# Caso algum valor esteja vazio, retorna um sinal False
def verificar_dados(dados):
    return all(value is not None for value in dados.values())

# Função para realizar as medições e montar no dicionário
def gerar_dados(keys=chaves, valores=None):
    valores = valores or {  # Substituir por chamadas de funções para os sensores ou fonte das informações
        "elevator_id": lambda: random.randint(1, 100),
        "position": lambda: random.randint(0, 10),
        "door_status": lambda: random.choice(["open", "closed"]),
        "weight": lambda: random.randint(0, 750),
    }
    
    dados = {key: valores.get(key, lambda: None)() for key in keys}
    completo = all(value is not None for value in dados.values())
    
    return dados, completo
