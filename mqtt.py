import paho.mqtt.client as mqtt
import ssl, re

MQTT_USR = "master"
MQTT_PSW = "Abc123**"
MQTT_TOPIC = "elevator_1"
MQTT_BROKER = "3d04701073de45d6a59a96eaa0b0d39e.s1.eu.hivemq.cloud"

MQTT_COMANDOS = ["manutencao begin", "manutencao end", "go to", "get level"]

# Callback when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code):
    print(f"Connected with result code {reason_code}")
    try:
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(MQTT_TOPIC)
    except Exception as e:
        print(f"Error subscribing to topic: {e}")

# Callback when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
        message = msg.payload.decode()
        for comando in MQTT_COMANDOS:
            if comando == "go to":
                padrao = rf"{comando}\s+(\d+)"
                match = re.search(padrao, message)
                if match:
                    valor = match.group(1)
                    print(f"Command: {comando}, Value: {valor}")
                elif message.startswith("go to"):
                    print("Command 'go to' received without a valid numeric value.")
            else:
                if message == comando:
                    print(f"Command received: {comando}")
    except Exception as e:
        print(f"Error processing the message: {e}")

def init():
    mqttc = mqtt.Client()

    try:
        # Set username and password
        mqttc.username_pw_set(MQTT_USR, MQTT_PSW)

        # Set callbacks
        mqttc.on_connect = on_connect
        mqttc.on_message = on_message

        # Set TLS configurations
        mqttc.tls_set(certfile=None, keyfile=None, tls_version=ssl.PROTOCOL_TLSv1_2)

        # Connect to the broker using TLS
        mqttc.connect(MQTT_BROKER, 8883, 60)

        # Block the call that processes network traffic, dispatches callbacks, and handles reconnections.
        mqttc.loop_start()  # Using loop_start() to allow parallel execution
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")
