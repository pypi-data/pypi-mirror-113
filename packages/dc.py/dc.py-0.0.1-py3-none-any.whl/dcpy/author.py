from .helper import Helper


class author:
    def __init__(self, token, event):
        self.__token = token
        self.__event = event
        self.username = event["username"]
        self.discriminator = event["discriminator"]
        self.id = event["id"]

    def is_bot(self):
        try:
            if self.__event["bot"]:
                return True
            else:
                return False
        except:
            return False

    async def send(self, content, component=None):
        Helper(self.__token).send_dm_message(self.id, content, component)
