Feature: Automated Testing for Smart Elevator System

  Background:
    Given the elevator simulator is configured
    And the cloud service is available

  Scenario: Verify that elevator sensor data is sent to the cloud via REST API every 5 seconds
    Given the elevator is operational
    When the elevator sends sensor data to the cloud
    Then the data should be sent every 5 seconds

  Scenario: Validate that all required fields are included in the data payload
    Given the elevator is sending data
    Then the payload should contain all data

  Scenario: Simulate API failure and ensure data is stored locally
    Given the API connection is down
    When the elevator attempts to send data
    Then the data should be stored locally until the connection is restored

  Scenario: Test reception of maintenance command via MQTT
    Given the elevator is online
    When the cloud sends a maintenance command via MQTT
    Then the elevator should switch to maintenance mode

  Scenario: Test reception of move command via MQTT
    Given the elevator is online
    When the cloud sends a command to move to floor 5
    Then the elevator should move to floor 5 and update its position
