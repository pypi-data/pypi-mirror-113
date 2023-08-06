from .channel import channel
from .author import author


class message:
    def __init__(self, token, event):
        self.content = event["content"]
        self.channel = channel(token, event["channel_id"])
        self.author = author(token, event["author"])
