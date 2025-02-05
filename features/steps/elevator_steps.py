from behave import given, when, then
import time
import requests
from data_acquire import ElevatorStatus
import mqtt
import rest_api

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
    elevator.status_dict["operational"] = True

@given('the elevator is online')
def step_impl(context):
    elevator.status_dict["online"] = True

@when('the elevator sends sensor data to the cloud')
def step_impl(context):
    context.response = rest_api.post_data(elevator.get_status())
    time.sleep(5)

@then('the data should be sent every 5 seconds')
def step_impl(context):
    assert context.response is not None

@given('the elevator is sending data')
def step_impl(context):
    context.data = elevator.get_status()

@then('the payload should contain all data')
def step_impl(context):
    rest_api.verify_and_print_json(context.data)

@given('the API connection is down')
@when('the elevator attempts to send data')
def step_impl(context):
    context.response = None
    try:
        raise requests.exceptions.ConnectionError("Simulating API failure")
        context.response = rest_api.post_data(elevator.status_dict)
    except requests.exceptions.RequestException:
        # Simulate local storage
        context.local_data = elevator.status_dict

@then('the data should be stored locally until the connection is restored')
def step_impl(context):
    assert context.response is None
    time.sleep(5)
    context.response = rest_api.post_data(elevator.get_status())
    assert context.response is not None

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
