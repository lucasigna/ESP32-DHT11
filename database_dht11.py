import urequests
import json
import ujson
import dht
import network
from machine import Pin
from time import sleep

sensor = dht.DHT11(Pin(14))

ssid = 'XXXXX'
password = 'XXXXX'
api_key = 'XXXXX'
url = 'https://api.ioteris.com.ar/api/data'

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print('Conectando a WiFi...')
        sleep(1)
    print('Conectado a WiFi')

def send_data(value, unit, variable, device_id):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'deviceId': device_id,
        'variable': variable,
        'value': value,
        'unit': unit
    }
    
    # Imprimir el payload a enviar
    print('Payload a enviar:', ujson.dumps(payload))

    response = urequests.post(url, data=ujson.dumps(payload), headers=headers)

    
    print('Respuesta:', response.status_code)
    print('Cuerpo de la respuesta:', response.text)
    
    response.close()

connect_wifi()

while True:
    sensor.measure()  # Mido los valores
    #temp = sensor.temperature()
    humidity = sensor.humidity()
    
    # Imprimimos los valores de temperatura y humedad en la consola
    print(f"Humedad: {humidity}%")
    send_data(humidity, "%", "Humedad ESP32", "XXXXXX")
    
    sleep(5)  # Espera 5 segundos antes de la próxima medición
