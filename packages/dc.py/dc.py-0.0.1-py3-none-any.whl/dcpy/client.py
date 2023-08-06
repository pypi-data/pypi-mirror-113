from .user import user


class client:
    def __init__(self, event):
        self.user = user(event)
