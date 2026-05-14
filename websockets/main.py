"""
mantiene conexión WebSocket abierta con el front-end en
ws://localhost:8080 y expone un endpoint HTTP en
http://localhost:8081/send_event para el servidor Flask
"""

import asyncio
import websockets
from aiohttp import web
import json

connected_clients = set()


async def websocket_handler(websocket):
    """maneja la conexión entrante del cliente WebSocket
    añade el cliente al conjunto de clientes conectados y espera hasta que se
    cierre la conexión.
    """
    connected_clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)


async def send_event(request):
    """recibe eventos desde Flask y los reenvía al front,
    espera un JSON con la clave 'message'.
    """
    try:
        data = await request.json()
        message = data.get("message", "")
        print(f"Evento recibido desde Flask: {message}")

        # reenviar mensaje al cliente
        for client in connected_clients.copy():
            try:
                await client.send(json.dumps(message))
                print(f"Mensaje enviado al cliente: {message}")
            except Exception:
                connected_clients.discard(client)

        return web.Response(text="Evento enviado a los clientes")
    except Exception as e:
        return web.Response(text=f"Error: {str(e)}", status=400)


async def main():
    app = web.Application()
    app.router.add_post("/send_event", send_event)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", 8081)
    await site.start()

    await websockets.serve(websocket_handler, "localhost", 8080)

    print("Servidor WebSocket ejecutándose en ws://localhost:8080")
    print("Servidor HTTP ejecutándose en http://localhost:8081/send_event")

    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
