# Servidor de WebSockets

Este módulo crea y documenta un servidor de WebSockets dentro de la carpeta `websockets`.
Su propósito es mantener una comunicación continua entre el servidor Flask y el front-end.

## Qué se hizo

- Se creó un servidor WebSocket en `ws://localhost:8080` para que el front-end se conecte.
- Se creó un endpoint HTTP en `http://localhost:8081/send_event` para recibir eventos desde Flask.
- Al recibir un evento desde Flask, el servidor lo reenvía a todos los clientes WebSocket activos.
- Se implementó un conjunto global `connected_clients` para gestionar las conexiones abiertas.
- Se documentó el flujo en español y se agregaron comentarios en el código.

## Requisitos

Instalar dependencias en la carpeta `websockets`:

```bash
pip install -r requirements.txt
```

## Ejecución

Iniciar el servidor de WebSockets y el puente HTTP:

```bash
python main.py
```

El servidor quedará en ejecución continua hasta que se detenga manualmente.

## Uso desde Flask

Desde Flask se puede enviar un evento con un POST JSON al endpoint:

```bash
curl -X POST http://localhost:8081/send_event \
  -H "Content-Type: application/json" \
  -d '{"message": "texto del evento"}'
```

El cuerpo debe contener un JSON con la clave `message`.

## Ejemplo en el front-end

En el front-end usar un WebSocket para conectarse y escuchar mensajes:

```javascript
const socket = new WebSocket('ws://localhost:8080');

socket.onopen = () => {
  console.log('Conectado al servidor de WebSocket');
};

socket.onmessage = (event) => {
  console.log('Evento recibido:', event.data);
};

socket.onclose = () => {
  console.log('Conexión cerrada');
};
```

## Flujo de datos

1. Flask envía un POST a `http://localhost:8081/send_event`.
2. El servidor `websockets/main.py` recibe el mensaje.
3. Se envía el mensaje a todos los clientes WebSocket conectados.
4. El front-end recibe el evento en tiempo real.
