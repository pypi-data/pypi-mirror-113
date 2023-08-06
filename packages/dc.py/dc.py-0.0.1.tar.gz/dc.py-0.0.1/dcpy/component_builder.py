class ComponentBuilder:
    def __init__(self):
        self.__action_row = 0
        self.buttons = []
        self.select_menus = []

    def add_button(self, text, custom_id, style=None, enabled=True, emoji=None):
        if type(style) == int:
            if int(style) < 1:
                # TODO andere message überlegen
                raise TypeError("Der Style kann nur blue, grey, green, red, 1, 2, 3 oder 4 sein!")
            elif int(style) > 4:
                # TODO andere message überlegen
                raise TypeError("Der Style kann nur blue, grey, green, red, 1, 2, 3 oder 4 sein!")
        elif type(style) == str:
            if style == "blue":
                style = 1
            elif style == "grey":
                style = 2
            elif style == "green":
                style = 3
            elif style == "red":
                style = 4
            elif style == "1":
                style = 1
            elif style == "2":
                style = 2
            elif style == "3":
                style = 3
            elif style == "4":
                style = 4
            else:
                # TODO andere message überlegen
                raise TypeError("Der Style kann nur blue, grey, green, red, 1, 2, 3 oder 4 sein!")
        elif style is None:
            style = 1
        else:
            # TODO andere message überlegen
            raise TypeError("Der Style kann nur blue, grey, green, red, 1, 2, 3 oder 4 sein!")
        # TODO Emoji hinzufügen
        # TODO Überprüfen ob es überhaupt geht
        self.buttons.append([str(self.__action_row), str(text), str(custom_id), str(style), bool(enabled)])
        return self

    def add_url_button(self, text, url, enabled=True, emoji=None):
        # TODO Emoji hinzufügen
        # TODO Überprüfen ob es überhaupt geht
        self.buttons.append([str(self.__action_row), str(text), str(url), "5", bool(enabled)])
        return self

    def add_new_row(self):
        # TODO besser überprüfen ob das möglich ist
        if len(self.buttons) > 0:
            self.__action_row = self.__action_row + 1
        elif len(self.select_menus) > 0:
            self.__action_row = self.__action_row + 1
        else:
            print("geht so nicht...")
            # TODO Exception ausgeben.
        return self
