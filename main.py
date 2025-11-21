import network
import time
from machine import Pin
import dht
import ujson
from umqtt.simple import MQTTClient

# ---------------- CONFIGURAÇÕES ----------------
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASS = ""

MQTT_BROKER = "mqtt-dashboard.com"
MQTT_TOPIC = "vacina/dados"

DHT_PIN = 15
LED_VERDE = 4
LED_VERMELHO = 2

#temperatura min e máx de temperatura ideal da maioria das vacinas
TEMP_MIN = 2.0
TEMP_MAX = 8.0

#Umidade ideal para armazenamento da maioria vacinas
HUM_MIN = 30.0
HUM_MAX = 50.0


# ---------- Função para conectar ao WiFi ----------
def connect_wifi():
    print("Conectando ao WiFi...", end="")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)

    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.3)
    print(" conectado!")
    print("IP:", wlan.ifconfig()[0])


# ---------- Função para conectar ao servidor MQTT ----------
def connect_mqtt():
    print("Conectando ao MQTT...", end="")
    client = MQTTClient("esp32_vacina", MQTT_BROKER)
    client.connect()
    print(" conectado!")
    return client


# ---------------- INICIALIZAÇÃO ----------------
dht_sensor = dht.DHT22(Pin(DHT_PIN))
led_verde = Pin(LED_VERDE, Pin.OUT)
led_vermelho = Pin(LED_VERMELHO, Pin.OUT)

connect_wifi()
mqtt = connect_mqtt()

# ---------------- LOOP PRINCIPAL ----------------
while True:
    try:
        # Medir temperatura e umidade
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()

        print("Temperatura:", temp, "°C")
        print("Umidade:", hum, "%")

        # Verificação das condições ideais
        temperatura_ok = TEMP_MIN <= temp <= TEMP_MAX
        umidade_ok = HUM_MIN <= hum <= HUM_MAX

        if temperatura_ok and umidade_ok:
            led_verde.value(1)
            led_vermelho.value(0)
            print("Status: Ambiente ideal ✅")
        else:
            led_verde.value(0)
            led_vermelho.value(1)
            print("Status: ⚠️ ALARME – Ambiente fora dos padrões")

        # Monta JSON para enviar ao MQTT
        payload = ujson.dumps({
            "temperatura": temp,
            "umidade": hum,
        })

        print("Enviando MQTT:", payload)
        mqtt.publish(MQTT_TOPIC, payload)

    except Exception as e:
        print("Erro:", e)
        time.sleep(2)
        mqtt = connect_mqtt()

    print("--------------------")
    time.sleep(60)
