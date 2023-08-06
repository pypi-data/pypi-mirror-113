from .helper import Helper
from .author import author
from .button_interaction import button_interaction


class interaction:
    def __init__(self, token, event):
        self.__token = token
        self.__event = event
        self.id = event["id"]
        try:
            self.user = author(token, event["member"]["user"])
        except KeyError:
            self.user = author(token, event["user"])
        self.type = None
        self.button_interaction = None
        if event["type"] == 2:
            self.type = "slash_command_interaction"
        elif event["type"] == 3:
            self.type = "button_interaction"
            self.button_interaction = button_interaction(event)
        else:
            self.type = "unknown_interaction"

    def send_callback(self, content):
        Helper(self.__token).send_interaction_callback(self.id, self.__event["token"], content)
