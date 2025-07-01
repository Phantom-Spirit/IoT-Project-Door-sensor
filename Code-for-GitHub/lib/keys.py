# keys.py Template

import ubinascii              # Conversions between binary data and various encodings
import machine                # To Generate a unique id from processor

WIFI_SSID = 'Your_Wifi_Name'
WIFI_PASS = 'Your_Wifi_Password'

# Adafruit IO (AIO) configuration
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USER = "Your_Adafruit_User_Name"
AIO_KEY = "Your_Adafruit_Application_Key"
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Can be anything

# Temprature and Humidity feeds from the DHT11 to Aidafruit
AIO_TEMP_FEED = "Your_Adafruit_User_Name/feeds/temp"    # Address to the feed for Temprature
AIO_HUMI_FEED = "Your_Adafruit_User_Name/feeds/humid"   # Address to the feed for Humidity

# Mesage feed for door sensor
AIO_DOOR_FEED = "Your_Adafruit_User_Name/feeds/door" # Address to the feed for the door sensor
