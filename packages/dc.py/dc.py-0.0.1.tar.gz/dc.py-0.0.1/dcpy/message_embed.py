class MessageEmbed:
    def __init__(self):
        self.title = None
        self.description = None
        self.content = None
        self.timestamp = False
        self.footer = None
        self.color = None
        self.fields = []

    def set_title(self, title):
        self.title = str(title)
        return self

    def set_description(self, description):
        self.description = str(description)
        return self

    def set_content(self, content):
        self.content = content
        return self

    def set_timestamp(self, timestamp=True):
        self.timestamp = bool(timestamp)
        return self

    def set_footer(self, footer):
        self.footer = str(footer)
        return self

    def set_color(self, color):
        if color.lower() == "red":
            self.color = "16711680"
        elif color.lower() == "blue":
            self.color = ""
        elif color.lower() == "green":
            self.color = ""
        elif color.lower() == "purple":
            self.color = ""
        elif color.lower() == "yellow":
            self.color = "16773120"
        # TODO Color hinzufügen
        return self

    def add_field(self, name, value, inline=False):
        self.fields.append([str(name), str(value), bool(inline)])
        return self
