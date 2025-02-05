import threading
import mqtt

core_mqtt = threading.Thread(target=mqtt.init)
core_mqtt.start()

