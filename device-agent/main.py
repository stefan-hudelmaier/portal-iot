#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_outdoor_weather import BrickletOutdoorWeather
from time import sleep
from paho.mqtt import client as mqtt_client
import os
import certifi
import sys
import signal

HOST = "localhost"
PORT = 4223
UID_WEATHER = "SDM"
SENSOR_ID = 19
PASSWORD = os.environ['MQTT_PASSWORD']


def connect_via_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to Portal MQTT broker")
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_publish(client, userdata, result):
        print("Data published:", result)

    client = mqtt_client.Client('raspi')
    client.username_pw_set('raspi', PASSWORD)
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.tls_set(certifi.where())
    client.connect('mosquitto.6r55h5.p.getportal.org', 8883)
    return client


def main():
    client = connect_via_mqtt()
    client.loop_start()
    ipcon = IPConnection()
    ow = BrickletOutdoorWeather(UID_WEATHER, ipcon)

    print("Making connection to Tinkerforge")
    ipcon.connect(HOST, PORT)

    def shutdown(sig, frame):
        print("Shutting down")
        ipcon.disconnect()
        client.loop_stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)

    while True:
        client.publish('data/raspi/cellar/humidity', ow.get_sensor_data(19).humidity)
        sleep(1.0)


if __name__ == "__main__":
    main()
