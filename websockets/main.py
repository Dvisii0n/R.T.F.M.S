"""
Servidor de WebSockets y puente HTTP para la comunicación entre Flask y el front-end.

Este módulo mantiene una conexión WebSocket abierta con el front-end en
ws://localhost:8080 y expone un endpoint HTTP en
http://localhost:8081/send_event para que el servidor Flask envíe eventos.

Cuando Flask hace un POST a /send_event, este servidor reenvía el mensaje a
todos los clientes WebSocket conectados.
"""

import asyncio
import websockets
from aiohttp import web
import json

# Conjunto global de clientes WebSocket conectados
connected_clients = set()

async def websocket_handler(websocket):
    """Maneja la conexión entrante del cliente WebSocket.

    Añade el cliente al conjunto de clientes conectados y espera hasta que se
    cierre la conexión.
    """
    connected_clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)

async def send_event(request):
    """Recibe eventos desde Flask y los reenvía al front-end.

    Endpoint HTTP POST que espera un JSON con la clave 'message'.
    """
    try:
        data = await request.json()
        message = data.get('message', '')
        print(f"Evento recibido desde Flask: {message}")

        # Reenviar mensaje a todos los clientes WebSocket conectados
        for client in connected_clients.copy():
            try:
                await client.send(json.dumps(message))
                print(f"Mensaje enviado al cliente: {message}")
            except Exception:
                connected_clients.discard(client)

        return web.Response(text='Evento enviado a los clientes')
    except Exception as e:
        return web.Response(text=f'Error: {str(e)}', status=400)

async def main():
    """Inicializa los servidores HTTP y WebSocket."""
    # Servidor HTTP para recibir eventos desde Flask
    app = web.Application()
    app.router.add_post('/send_event', send_event)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8081)
    await site.start()

    # Servidor WebSocket para conexiones desde el front-end
    await websockets.serve(websocket_handler, 'localhost', 8080)

    print("Servidor WebSocket ejecutándose en ws://localhost:8080")
    print("Servidor HTTP ejecutándose en http://localhost:8081/send_event")

    # Mantener el bucle corriendo indefinidamente
    await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())