from .helper import Helper


class channel:
    def __init__(self, token, channel_id):
        self.__token = token
        self.channel_id = channel_id

    async def send(self, content, component=None):
        Helper(self.__token).send_message(self.channel_id, content, component)
