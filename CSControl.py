import asyncio
import telnetlib3


class CSControl:
    def __init__(self, host="127.0.0.1", port=2121):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None

    async def connect(self):
        """Establece conexión Telnet de forma asíncrona"""
        try:
            self.reader, self.writer = await telnetlib3.open_connection(self.host, self.port, encoding='utf-8')
            print("✅ Conectado a CS:GO Telnet")
            return True
        except ConnectionRefusedError:
            print("❌ Error: No se pudo conectar a CS:GO. Agrega '-netconport 2121' parámetros de lanzamiento del juego.")
            return False

    async def send_command(self, command):
        """Envía un comando al servidor Telnet de CS:GO"""
        if self.writer:
            self.writer.write(command + "\n")
            await self.writer.drain()
            print(f"📩 Comando enviado: {command}")
        else:
            print("⚠️ No hay conexión activa.")

    async def move_forward(self):
        await self.send_command("+forward")
        await asyncio.sleep(0.2)
        await self.send_command("-forward")

    async def move_backwards(self):
        await self.send_command("+back")
        await asyncio.sleep(0.2)
        await self.send_command("-back")

    async def move_right(self):
        await self.send_command("+moveright")
        await asyncio.sleep(0.2)
        await self.send_command("-moveright")

    async def move_left(self):
        await self.send_command("+moveleft")
        await asyncio.sleep(0.2)
        await self.send_command("-moveleft")

    async def jump(self):
        await self.send_command("+jump")
        await asyncio.sleep(0.2)  # Simula una pulsación rápida
        await self.send_command("-jump")

    async def crouch(self):
        await self.send_command("+duck")
        await asyncio.sleep(0.2)
        await self.send_command("-duck")

    async def shoot(self):
        await self.send_command("+attack")
        await asyncio.sleep(0.1)
        await self.send_command("-attack")

    async def aim(self):
        await self.send_command("+attack2")
        await asyncio.sleep(0.1)
        await self.send_command("-attack2")

    async def close_connection(self):
        """Cierra la conexión Telnet de forma segura"""
        try:
            if self.writer:
                self.writer.close()
                await asyncio.sleep(0.5)
                print("🔌 Conexión cerrada.")
            else:
                print("⚠️ No hay conexión activa para cerrar.")
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")