import aiohttp
import asyncio
from .events import Events
from .message import message
from .interaction import interaction
from .client import client
from datetime import datetime


class Bot(Events):
    def __init__(self, token, api_version=8):
        self.__token = token
        self.__api_version = api_version

    async def start(self):
        asyncio.get_event_loop().run_until_complete(await instance(self.trigger, self.__token, self.__api_version).start())


class instance:
    def __init__(self, trigger, token, api_version):
        self.trigger = trigger
        self.token = token
        self.api_version = api_version
        self.ws = None

    async def start(self):
        self.ws = await aiohttp.ClientSession().ws_connect(f'wss://gateway.discord.gg/?v={self.api_version}&encoding=json')
        msg = await self.ws.receive()
        event = msg.json()
        if event:
            loop = asyncio.get_event_loop()
            try:
                loop.create_task(self.check(event['d']['heartbeat_interval'] / 1000))
                payload = {
                    'op': 2,
                    "d": {
                        "token": self.token,
                        "intents": 513,
                        "properties": {
                            "$os": "windows",
                            "$browser": "chrome",
                            "$device": 'pc'
                        },
                        "compress": "true",
                        "presence": {
                            "activities": [{
                                "name": "Der Status funktioniert!",
                                "type": 0  # 0 = Spielt ... | 1 = Live auf Twitch | 2 = Hört ... zu | 3 = Schaut ...
                            }],
                            "status": "online",
                            # online = Online | dnd = Bitte nicht stören | invisible = Unsichtbar | idle = Abwesend
                            "afk": "false"
                        }
                    }
                }
                await self.ws.send_json(payload)
                await self.action()
            except KeyboardInterrupt:
                print("Bot stoppt")

    async def check(self, interval):
        while True:
            await asyncio.sleep(interval)
            heartbeatJSON = {
                "op": 1,
                "d": "null"
            }
            await self.ws.send_json(heartbeatJSON)

    async def action(self):
        async for msg in self.ws:
            event = msg.json()
            if event:
                if event["t"] is not None:
                    if event["t"] == "READY":
                        print("[Ready]")
                        print(f"Username: {event['d']['user']}")
                        # TODO verbessern und mit der user klasse verknüpfen
                        await self.trigger("ready", client(event["d"]["user"]))
                        # Ready Event ausführen!
                    if event["t"] == "MESSAGE_CREATE":
                        print("[Message Create]")
                        await self.trigger("message", message(self.token, event['d']))
                        # Message Create Event ausführen!
                    if event["t"] == "MESSAGE_UPDATE":
                        print("[Message Update]")
                        # Message Update Event ausführen!
                    if event["t"] == "MESSAGE_DELETE":
                        print("[Message Delete]")
                        # Message Delete Event ausführen!
                    if event["t"] == "MESSAGE_DELETE_BULK":
                        print("[Message Delete Bulk]")
                        # Message Delete Bulk Event ausführen!
                    if event["t"] == "GUILD_CREATE":
                        print("[Guild Create]")
                        if datetime.now().isoformat() == event["d"]["joined_at"]:
                            print("Neue guild betreten!")
                        else:
                            print("alte guild erkannt")
                            print(datetime.now().isoformat() + "\n" + event["d"]["joined_at"])
                        # print("Current Time: " + datetime.now().isoformat() + "\nGuild Joined Time: " + event["d"]["joined_at"])
                        # Guild Create Event ausführen!
                    if event["t"] == "GUILD_UPDATE":
                        print("[Guild Update]")
                        # Guild Update Event ausführen!
                    if event["t"] == "GUILD_DELETE":
                        print("[Guild Delete]")
                        # Guild Delete Event ausführen!
                    if event["t"] == "GUILD_ROLE_CREATE":
                        print("[Guild Role Create]")
                        # Guild Role Create Event ausführen!
                    if event["t"] == "GUILD_ROLE_UPDATE":
                        print("[Guild Role Update]")
                        # Guild Role Update Event ausführen!
                    if event["t"] == "GUILD_ROLE_DELETE":
                        print("[Guild Role Delete]")
                        # Guild Role Delete Event ausführen!
                    if event["t"] == "CHANNEL_CREATE":
                        print("[Channel Create]")
                        # Channel Create Event ausführen!
                    if event["t"] == "CHANNEL_UPDATE":
                        print("[Channel Update]")
                        # Channel Update Event ausführen!
                    if event["t"] == "CHANNEL_DELETE":
                        print("[Channel Delete]")
                        # Channel Delete Event ausführen!
                    if event["t"] == "INTERACTION_CREATE":
                        print("[Interaction Create]")
                        await self.trigger("interaction", interaction(self.token, event["d"]))
                    if event["t"] == "APPLICATION_COMMAND_CREATE":
                        print("[Application Command Create]")
                        # Application Command Create Event ausführen!
                    if event["t"] == "APPLICATION_COMMAND_DELETE":
                        print("[Application Command Delete")
                        # Application Command Delete Event ausführen!
                    # print(event["t"])
