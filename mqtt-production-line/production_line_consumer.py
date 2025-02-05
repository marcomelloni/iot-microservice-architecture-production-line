import paho.mqtt.client as mqtt
import json
import time
from production_line_producer import deactivate_production_line  # Importa la production line dal producer

# Configurazione variabili
client_id = "ProductionLine-Consumer"
broker_ip = "127.0.0.1"  # Indirizzo IP del broker
broker_port = 1883  # Porta del broker
target_topic_filter = "production_line/control/stop"  # Topic per il comando di stop

# Crea un nuovo client MQTT
mqtt_client = mqtt.Client(client_id)

# Definisci il callback per quando il client riceve una risposta CONNACK dal server
def on_connect(client, userdata, flags, rc):
    """Chiamato quando il client si connette al broker."""
    print(f"Connesso con codice di risultato {rc}")
    # Iscrizione al topic dopo la connessione riuscita
    mqtt_client.subscribe(target_topic_filter)
    print(f"Iscritto a: {target_topic_filter}")

# Definisci un callback per gestire i messaggi ricevuti
def on_message(client, userdata, message):
    """Chiamato quando viene ricevuto un messaggio."""
    
    # Verifica se il messaggio ricevuto corrisponde al filtro del topic
    if mqtt.topic_matches_sub(target_topic_filter, message.topic):
        try:
            # Decodifica il payload del messaggio come stringa
            message_payload = message.payload.decode("utf-8")
            payload_data = json.loads(message_payload)  # Assumi che il payload sia in formato JSON

            # Se payload_data è un booleano, usalo direttamente
            if isinstance(payload_data, bool):  
                if payload_data:  # Verifica se è True
                    deactivate_production_line()
                    print("Linea di produzione fermata.")
            
            print(f"Messaggio ricevuto sul topic {message.topic}: {payload_data}")

        except json.JSONDecodeError:
            print("Errore nella decodifica del payload JSON.")


# Collega i metodi di callback
mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect

# Connetti al broker MQTT
mqtt_client.connect(broker_ip, broker_port)

# Avvia il loop del client MQTT (questo bloccherà l'esecuzione e manterrà il programma in esecuzione)
mqtt_client.loop_start()

# Mantieni il consumer in esecuzione per ricevere i comandi
while True:
    time.sleep(1)  # Mantieni attivo il ciclo per ascoltare i messaggi
