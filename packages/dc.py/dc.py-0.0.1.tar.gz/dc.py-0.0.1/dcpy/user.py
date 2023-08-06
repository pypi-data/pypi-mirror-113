class user:
    def __init__(self, event):
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
