class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, ws):
        await ws.accept()
        self.active_connections.append(ws)

    def disconnect(self, ws):
        self.active_connections.remove(ws)

    async def broadcast(self, data):
        for conn in self.active_connections:
            await conn.send_json(data)
