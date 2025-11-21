# Transporte Inteligente de Vacinas
O objetivo deste estudo é demonstrar a viabilidade e a eficácia de um sistema de IoT para o transporte seguro de imunobiológicos. Ao assegurar que as vacinas mantenham sua qualidade desde a fabricação até o ponto de aplicação, a solução proposta não apenas reduz o desperdício, mas também fortalece a infraestrutura de saúde, promovendo um acesso mais seguro e equitativo à imunização em larga escala. Dessa forma, o projeto se alinha diretamente aos princípios do Objetivo de Desenvolvimento Sustentável (ODS) 3, que busca garantir saúde e bem-estar para todos.

O projeto foi pensado para ser simples, acessível e de baixo custo, podendo ser reproduzido por estudantes, pesquisadores e profissionais que desejem criar um sistema básico de monitoramento IoT

Este protótipo realiza o monitoramento de temperatura e umidade utilizando um ESP32 e o sensor DHT22. O ESP32 lê os dados do sensor, verifica se estão dentro dos limites ideais para transporte de vacinas e aciona LEDs indicadores:

- LED verde: condições adequadas
- LED vermelho: alerta de temperatura/umidade fora do ideal

Após processar as leituras, o ESP32 envia os dados em formato JSON para o broker MQTT público test.mosquitto.org, utilizando o tópico vacina/dados. As informações podem ser visualizadas em qualquer cliente MQTT, sendo o MQTT Explorer o mais prático para testes.

O envio dos dados é periódico — configurado no código para ocorrer a cada 1 minuto, mas pode ser ajustado conforme a necessidade.

✔ Como reproduzir o projeto
<br />Qualquer pessoa pode replicar seguindo estes passos:
1. Acessar o simulador Wokwi (gratuito e sem instalação).
2. Importar o código em MicroPython e adicionar os componentes:
  <br />- ESP32
  <br />- Sensor DHT22
  <br />- LED verde
  <br />- LED vermelho
  <br />- Resistores
3. Configurar os pinos conforme o diagram.json do projeto.
4. Executar a simulação — o console do Wokwi exibirá as leituras.
5. Abrir o MQTT Explorer, conectar no broker mqtt-dashboard.com e assinar o tópico vacina/dados para visualizar os dados em tempo real
6. Caso queira rodar em hardware real, basta usar um ESP32 físico e alimentar o circuito com 5V/USB

Envia os dados via Wi-Fi (TCP/IP) para o broker MQTT no tópico: dados/vacina.
Cada publicação é enviada em formato JSON, contendo:
```
{ "temperatura": XX.X, "umidade": XX.X }
```

# 📌 Software desenvolvido + documentação do código
<br />O code do firmware está no arquivo: main.py
<br />O código:
- Conecta ao Wi-Fi
- Conecta ao servidor MQTT
- Lê temperatura e umidade
- Verifica limites (2–8°C e 30–50%)
- Aciona LEDs
- Monta JSON
- Publica no tópico vacina/dados
- Aguarda 1 minuto 

# 📌 Descrição do hardware utilizado
<br />🖥 Plataforma
ESP32 DevKit V1
- Wi-Fi + Bluetooth
- Dual-core 240 MHz
- 520 KB RAM

🌡 Sensores
<br />BME280 - temperatura, umidade e pressão (utilizado durante o projeto teórico)
- Alimentação: 3.3V
- comunicação I2C/SPI

DHT22 – temperatura e umidade (utilizado no simulador Wokwi)
- Alimentação: 3.3V
- Precisão: Temperatura ±0.5°C e Umidade ±2%
- Comunicação digital (protocolo próprio de um fio)

🔔 Atuadores
- LED Verde (ambiente ideal)
- LED Vermelho (alarme de risco)

🛠 Montagem
O projeto foi montado em:
- Ambiente simulado Wokwi (sem uso de breadboard real)
- Os pinos utilizados foram:
<br />Sensor DHT22 → GPIO 15
<br />LED verde → GPIO 4
<br />LED vermelho → GPIO 2

# 📌 Documentação das interfaces, protocolos e comunicação
📶 Comunicação Wi-Fi

O ESP32 conecta-se ao roteador usando TCP/IP:
```
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASS = ""
```
🟦 Protocolo MQTT

Foi escolhido o broker público:
```
mqtt-dashboard.com 
```

💬 Fluxo de comunicação
ESP32 → Wi-Fi → Broker MQTT → Cliente MQTT Explorer

# Comunicação/controle via Internet (TCP/IP) + MQTT
O projeto atende totalmente esse requisito:

<br />✔ O ESP32 se conecta via Wi-Fi (TCP/IP)
<br />✔ Envia mensagens para o servidor MQTT
<br />✔ As mensagens são acessadas via internet por qualquer dispositivo conectado
<br />✔ Testado no MQTT Explorer

