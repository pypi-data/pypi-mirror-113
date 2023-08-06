import requests
import json
from .component_builder import ComponentBuilder
from .message_embed import MessageEmbed


class Helper:
    def __init__(self, token):
        self.token = token
        self.send_message_endpoint = "https://discord.com/api/v8/channels/%ChannelID%/messages"
        self.create_dm_endpoint = "https://discord.com/api/v8/users/@me/channels"
        self.interaction_callback_endpoint = "https://discord.com/api/v8/interactions/%InteractionID%/%InteractionToken%/callback"

    def send_message(self, channel_id, content, component=None):
        headers = {
            "Authorization": f"Bot {self.token}",
            "Content-Type": "application/json"
        }
        message = {}
        if content is not None:
            if type(content) == str:
                message = {
                    "content": content,
                    "components": []
                }
            elif type(content) == MessageEmbed:
                message = {
                    "content": content.content,
                    "embeds": [
                        {
                            "title": content.title,
                            "description": content.description,
                            "color": content.color,
                            "thumbnail": {
                                "url": None
                            },
                            "image": {
                                "url": None
                            },
                            "footer": {
                                "text": content.footer,
                                "icon_url": None
                            },
                            "fields": []
                        }
                    ],
                    "components": []
                }
                if len(content.fields) > 0:
                    for list in content.fields:
                        message["embeds"][0]["fields"].append({"name": list[0], "value": list[1], "inline": bool(list[2])})
            else:
                # TODO andere message überlegen
                raise TypeError("content darf nur ein String oder MessageEmbed sein!")
        else:
            # TODO andere message überlegen
            raise TypeError("content darf nicht None sein!")

        if component is not None:
            if type(component) == ComponentBuilder:
                if len(component.buttons) > 0:
                    message["components"].append({"type": 1, "components": []})
                    is_on = 0
                    for list in component.buttons:
                        if is_on < int(list[0]):
                            message["components"].append({"type": 1, "components": []})
                            is_on = int(list[0])
                        if int(list[3]) == 5:
                            if bool(list[4]):
                                message["components"][int(list[0])]["components"].append({"type": 2, "label": str(list[1]), "url": list[2], "style": list[3], "disabled": False})
                            else:
                                message["components"][int(list[0])]["components"].append({"type": 2, "label": str(list[1]), "url": list[2], "style": list[3], "disabled": True})
                        else:
                            if bool(list[4]):
                                message["components"][int(list[0])]["components"].append({"type": 2, "label": str(list[1]), "custom_id": list[2], "style": list[3], "disabled": False})
                            else:
                                message["components"][int(list[0])]["components"].append({"type": 2, "label": str(list[1]), "custom_id": list[2], "style": list[3], "disabled": True})
            else:
                # TODO andere message überlegen
                raise TypeError("component darf nur ein ComponentBuilder sein!")
        requests.post(self.send_message_endpoint.replace("%ChannelID%", channel_id), headers=headers, json=message)

    def send_dm_message(self, user_id, content, component=None):
        headers = {
            "Authorization": f"Bot {self.token}",
            "Content-Type": "application/json"
        }
        recipient = {
            "recipient_id": user_id
        }
        request = requests.post(self.create_dm_endpoint, headers=headers, json=recipient)
        data = json.loads(request.text)
        message = {}
        if content is not None:
            if type(content) == str:
                message = {
                    "content": content,
                    "components": []
                }
            elif type(content) == MessageEmbed:
                message = {
                    "content": content.content,
                    "embeds": [
                        {
                            "title": content.title,
                            "description": content.description,
                            "color": content.color,
                            "thumbnail": {
                                "url": None
                            },
                            "image": {
                                "url": None
                            },
                            "footer": {
                                "text": content.footer,
                                "icon_url": None
                            },
                            "fields": []
                        }
                    ],
                    "components": []
                }
                if len(content.fields) > 0:
                    for list in content.fields:
                        message["embeds"][0]["fields"].append({"name": list[0], "value": list[1], "inline": bool(list[2])})
            else:
                # TODO andere message überlegen
                raise TypeError("content darf nur ein String oder MessageEmbed sein!")
        else:
            # TODO andere message überlegen
            raise TypeError("content darf nicht None sein!")

        if component is not None:
            if type(component) == ComponentBuilder:
                if len(component.buttons) > 0:
                    message["components"].append({"type": 1, "components": []})
                    is_on = 0
                    for list in component.buttons:
                        if is_on < int(list[0]):
                            message["components"].append({"type": 1, "components": []})
                            is_on = int(list[0])
                        if int(list[3]) == 5:
                            if bool(list[4]):
                                message["components"][int(list[0])]["components"].append({"type": 2, "label": str(list[1]), "url": list[2], "style": list[3], "disabled": False})
                            else:
                                message["components"][int(list[0])]["components"].append({"type": 2, "label": str(list[1]), "url": list[2], "style": list[3], "disabled": True})
                        else:
                            if bool(list[4]):
                                message["components"][int(list[0])]["components"].append({"type": 2, "label": str(list[1]), "custom_id": list[2], "style": list[3], "disabled": False})
                            else:
                                message["components"][int(list[0])]["components"].append({"type": 2, "label": str(list[1]), "custom_id": list[2], "style": list[3], "disabled": True})
            else:
                # TODO andere message überlegen
                raise TypeError("component darf nur ein ComponentBuilder sein!")
        requests.post(self.send_message_endpoint.replace("%ChannelID%", data["id"]), headers=headers, json=message)

    # TODO Methode verbessern.
    def send_interaction_callback(self, interaction_id, interaction_token, content):
        headers = {
            "Authorization": f"Bot {self.token}",
            "Content-Type": "application/json"
        }
        if content is not None:
            if type(content) == str:
                callback = {
                    "type": 4,
                    "data": {
                        "content": content,
                        "components": []
                    }
                }
                requests.post(self.interaction_callback_endpoint.replace("%InteractionID%", interaction_id).replace("%InteractionToken%", interaction_token), headers=headers, json=callback)
            elif type(content) == MessageEmbed:
                callback = {
                    "type": 4,
                    "data": {
                        "content": content.content,
                        "embeds": [
                            {
                                "title": content.title,
                                "description": content.description,
                                "color": content.color,
                                "thumbnail": {
                                    "url": None
                                },
                                "image": {
                                    "url": None
                                },
                                "footer": {
                                    "text": content.footer,
                                    "icon_url": None
                                },
                                "fields": []
                            }
                        ],
                        "components": []
                    }
                }
                if len(content.fields) > 0:
                    for list in content.fields:
                        callback["data"]["embeds"][0]["fields"].append({"name": list[0], "value": list[1], "inline": bool(list[2])})
                requests.post(self.interaction_callback_endpoint.replace("%InteractionID%", interaction_id).replace("%InteractionToken%", interaction_token), headers=headers, json=callback)
            else:
                raise TypeError("content darf nur MessageEmbed oder ein String sein.")
        else:
            raise TypeError("content darf nicht None sein!")
