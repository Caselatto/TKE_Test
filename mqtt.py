import paho.mqtt.client as mqtt
import ssl, re

MQTT_USR = "master"
MQTT_PSW = "Abc123**"
MQTT_TOPIC = "elevator_1"
MQTT_BROKER = "3d04701073de45d6a59a96eaa0b0d39e.s1.eu.hivemq.cloud"

MQTT_COMANDOS = ["manutencao begin", "manutencao end", "go to", "get level"]

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    
    for comando in MQTT_COMANDOS:
        if comando == "go to":
            padrao = rf"{comando}\s+(\d+)"
            match = re.search(padrao, message)
            if match:
                valor = match.group(1)
                print(f"Comando: {comando}, Valor: {valor}")
            elif message.startswith("go to"):
                print("Comando 'go to' recebido sem valor numérico válido.")
        else:
            if message == comando:
                print(f"Comando recebido: {comando}")

def init():
    mqttc = mqtt.Client()

    # Definir o usuário e a senha
    mqttc.username_pw_set(MQTT_USR, MQTT_PSW)

    # Definir callbacks
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    # Definir configurações TLS
    mqttc.tls_set(certfile=None, keyfile=None, tls_version=ssl.PROTOCOL_TLSv1_2)

    # Conectar ao broker usando TLS
    mqttc.connect(MQTT_BROKER, 8883, 60)

    # Bloquear chamada que processa tráfego de rede, despacha callbacks e lida com reconexões.
    mqttc.loop_forever()
