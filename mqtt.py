import paho.mqtt.client as mqtt
import ssl

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("Elevator_1")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + ":  " + str(msg.payload.decode("utf-8")))

mqttc = mqtt.Client()

# Definir o usuário e a senha
mqttc.username_pw_set("master", "Abc123**")

# Definir callbacks
mqttc.on_connect = on_connect
mqttc.on_message = on_message

# Definir configurações TLS
mqttc.tls_set(certfile=None, keyfile=None, tls_version=ssl.PROTOCOL_TLSv1_2)

# Conectar ao broker usando TLS
mqttc.connect("3d04701073de45d6a59a96eaa0b0d39e.s1.eu.hivemq.cloud", 8883, 60)

# Bloquear chamada que processa tráfego de rede, despacha callbacks e lida com reconexões.
mqttc.loop_forever()
