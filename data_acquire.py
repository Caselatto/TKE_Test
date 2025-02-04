import random

# The dictionary holding the elevator status, kept outside the class
elevator_status = {
    "elevator_id": None,
    "position": None,
    "door_status": None,
    "weight": None
}

class ElevatorStatus:
    def __init__(self):
        # Initialize with a reference to the status dictionary
        self.status_dict = elevator_status

    # Function to verify if all data is available
    def is_complete(self):
        return all(value is not None for value in self.status_dict.values())
    
    # Function to print the current status
    def print_status(self):
        if self.is_complete():
            for key, value in self.status_dict.items():
                print(f"{key}: {value}")
        else:
            print("Incomplete status data.")

    # Function to simulate the acquisition of new data
    def generate_data(self, id):
        self.status_dict["elevator_id"] = id
        self.status_dict["position"] = random.randint(0, 10)
        self.status_dict["door_status"] = random.choice(["open", "closed"])
        self.status_dict["weight"] = random.randint(0, 750)
