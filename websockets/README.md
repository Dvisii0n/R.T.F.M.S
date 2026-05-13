# Servidor de WebSockets
WebSocket en `ws://localhost:8080` para el front-end
endpoint HTTP en `http://localhost:8081/send_event` para recibir eventos desde Flask.


## desde Flask
Desde Flask se puede enviar un evento con un POST JSON al endpoint:

curl -X POST http://localhost:8081/send_event \
  -H "Content-Type: application/json" \
  -d '{"message": "texto del evento"}'

debe contener un JSON con la clave `message`.

## front-end
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
