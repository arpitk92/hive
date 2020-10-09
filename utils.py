import json


class JSON:
    def __init__(self):
        self.file = "settings.json"
        self._json_obj = self.__read_json()
        self.__set_attributes(self._json_obj)

    def __read_json(self):
        with open(self.file, 'r') as content:
            json_obj = json.load(content)
        return json_obj

    def __set_attributes(self, json_obj):
        for key in json_obj:
            setattr(self, key, json_obj[key])
