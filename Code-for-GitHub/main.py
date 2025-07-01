import time                   # Allows use of time.sleep() for delays
from mqtt import MQTTClient   # For use of MQTT protocol to talk to Adafruit IO
import machine                # Interfaces with hardware components
import micropython            # Needed to run any MicroPython code
import random                 # Random number generator
from machine import Pin       # Define pin
import keys                   # Contain all keys used here
import wifiConnection         # Contains functions to connect/disconnect from WiFi 
import dht                    # For temprature sensor

print("\t > Running: Main # v1.05 \n")

# Project_code_v1.05
# Update: Fixed door state to know when open/close. Sends only when opend.       

"""Door Handeling"""
switch_state = False  # Starting state of the switch: off/closed door/closed curcuit ?
time_elapsed_door = 0
TIME_INTERVAL_DOOR = 1000    # milliseconds

def switch_handler(pin):
    global switch_state
    global time_elapsed_door
    global TIME_INTERVAL_DOOR

    if ((time.ticks_diff(time.ticks_ms(), time_elapsed_door)) < TIME_INTERVAL_DOOR):
        #time.ticks_ms() - time_elapsed_door
        return

    switch_state = True
    time_elapsed_door = time.ticks_ms()

# Core 1 loop IRQ, looks foor a shange in state.
switch_pin = Pin(15, Pin.IN, Pin.PULL_UP)
switch_pin.irq(trigger=Pin.IRQ_RISING, handler=switch_handler)

""" Door Sending """
print(switch_pin.value()) # closed door = 0

def send_door():
    door_message = "open"   
    print("Door pin value: {}".format(switch_pin.value()))

    # Door is open when pin value is 1
    if switch_pin.value() == 1:
        print("Publishing: {} to {} ... ".format(door_message, keys.AIO_DOOR_FEED))
        try:
            client.publish(topic=keys.AIO_DOOR_FEED, msg=str(door_message))
            print("DONE")
        except Exception as error:
            print("Exception occurred", error)
    else:
        return

""" Temprature & Humidity """
time_elapsed_temp = 0
TIME_INTERVAL_TEMP = 30000

tempSensor = dht.DHT11(machine.Pin(27))     # Defining pin for DHT11 Temp&Humid sensor


def send_temp():
    global time_elapsed_temp
    global TIME_INTERVAL_TEMP

    if ((time.ticks_diff(time.ticks_ms(), time_elapsed_temp)) < TIME_INTERVAL_TEMP):
        return

    tempSensor.measure()
    temperature = tempSensor.temperature()
    humidity = tempSensor.humidity()
    print("Publishing: {0}C to {2} and {1}% to {3} ... ".format(
        temperature, humidity, keys.AIO_TEMP_FEED, keys.AIO_HUMI_FEED), end=''
        )

    try:
        client.publish(topic=keys.AIO_TEMP_FEED, msg=str(temperature))
        client.publish(topic=keys.AIO_HUMI_FEED, msg=str(humidity))
        print("DONE")
    except Exception as error:
        print("Exception occurred", error)
    finally:
        time_elapsed_temp = time.ticks_ms()

""" Wifi & MQTT  """
# Connecting to WiFi
try:    
    ip = wifiConnection.connect()   
except KeyboardInterrupt:
    print("Keyboard interrupt")

# Connecting to MQTT Broker/Client
client = MQTTClient(keys.AIO_CLIENT_ID, keys.AIO_SERVER, keys.AIO_PORT, keys.AIO_USER, keys.AIO_KEY)
client.connect()
print("Connected to: {} as {}.".format(keys.AIO_SERVER, keys.AIO_USER))


""" Main program loop """
while True:
    send_temp()
    if switch_state is True:
        send_door()
        switch_state = False
