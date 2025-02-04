import requests

API_URL = "https://jsonplaceholder.typicode.com/todos"  # Replace with the real API URL

# Function to read data from the cloud
def get_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raises exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving data: {e}")
        return None

# Function to send data to the cloud
def post_data(dados):
    try:
        response = requests.post(API_URL, json=dados)
        print(f"Response from server after POST: {response.status_code} - {response.text}")
        response.raise_for_status()  # Raises exception for HTTP errors

        if response.status_code in [200, 201]:
            print("Data sent successfully")
            return response.json()
        else:
            print(f"Failed to send data: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")
        return None

# Function to verify and print data
def verify_and_print_json(data):
    expected_keys = ["elevator_id", "position", "door_status", "weight"]

    if isinstance(data, dict):
        if all(key in data for key in expected_keys):
            for key, value in data.items():
                print(f"{key}: {value}")
        else:
            print("Incomplete data.", end=" ")
    elif isinstance(data, list):  # If it's a list, iterate through the items
        for item in data:
            verify_and_print_json(item)
