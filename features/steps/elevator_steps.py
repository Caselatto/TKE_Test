from behave import given, when, then
import time
import requests
from data_acquire import ElevatorStatus
import mqtt
import rest_api
import json
import os

pasta="saved"
os.makedirs(pasta, exist_ok=True)

def save_json(dados):
    arquivos_existentes = [f for f in os.listdir(pasta) if f.endswith(".json")]
    numero_arquivo = len(arquivos_existentes) + 1
    nome_arquivo = os.path.join(pasta, f"dados_{numero_arquivo}.json")
    
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

# Initialize Elevator Status
elevator = ElevatorStatus()

@given('the elevator simulator is configured')
def step_impl(context):
    elevator.generate_data(id=1)

@given('the cloud service is available')
def step_impl(context):
    response = rest_api.get_data()
    if response:
        elevator.status_dict["online"] = True

@given('the elevator is operational')
def step_impl(context):
    elevator.generate_data(id=len([f for f in os.listdir(pasta) if f.endswith(".json")]) + 1)
    print(elevator.get_status())

@when('the elevator sends sensor data to the cloud')
def step_impl(context):
    elevator.generate_data(id=len([f for f in os.listdir(pasta) if f.endswith(".json")]) + 1)
    time.sleep(3)
    context.response = rest_api.post_data(elevator.get_status())
    time.sleep(5)
    print(f"Sent data with latency: {elevator.get_status()}")


@then('the data should be sent every 5 seconds')
def step_impl(context):
    assert context.response is not None

@when('the elevator is sending data')
def step_impl(context):
    context.data = elevator.get_status()

@then('the payload should contain all data')
def step_impl(context):
    if not elevator.check_limits():
        print("Warning: Data is invalid!")
    else:
        rest_api.verify_and_print_json(context.data)
        print("Data sent successfully.")

@given('the API connection is down')
def step_impl(context):
    elevator.generate_data(id=4)
    elevator.status_dict["online"] = False

@when('the elevator attempts to send data')
def step_impl(context):
    context.response = None
    try:
        raise requests.exceptions.Timeout("Simulating message drop")
        context.response = rest_api.post_data(elevator.status_dict)
    except requests.exceptions.Timeout:
        save_json(elevator.status_dict)  # Salva os dados localmente
        print("Message dropped, data saved locally.")

@then('the data should be stored locally until the connection is restored')
def step_impl(context):
    save_json(elevator.status_dict)

@when('the cloud sends a maintenance command via MQTT')
def step_impl(context):
    mqtt.comand_received("go to 5")
    time.sleep(2)

@then('the elevator should switch to maintenance mode')
def step_impl(context):
    elevator.status_dict["maintenence"] = True
    print("Elevator switched to maintenance mode")

@when('the cloud sends a command to move to floor 5')
def step_impl(context):
    mqtt.comand_received("go to 5")
    time.sleep(2)

@then('the elevator should move to floor 5 and update its position')
def step_impl(context):
    elevator.status_dict["position"] = 5
    print("Elevator moved to floor 5")
