import json


class ResultsBase:
    def __init__(self, client_id=None, base_file='results.json'):
        self.file = base_file
        self.client_id = str(client_id)

    def is_saved(self):
        try:
            with open(self.file, encoding='utf-8') as f:

                try:
                    data = json.load(f)

                    if self.client_id in data.keys():
                        return True

                    else:
                        return False

                except json.decoder.JSONDecodeError:
                    return False

        except FileNotFoundError:
            return False

    def is_shown(self, vk_id):
        vk_id = str(vk_id)
        try:
            with open(self.file, encoding='utf-8') as f:

                try:
                    data = json.load(f)

                    if self.client_id in data.keys():

                        if vk_id in data[self.client_id]:
                            return True

                        else:
                            return False

                    else:
                        return False

                except json.decoder.JSONDecodeError:
                    return False

        except FileNotFoundError:
            return False

    def add_shown(self, vk_id):
        vk_id = str(vk_id)
        try:
            with open(self.file, encoding='utf-8') as f1:

                try:
                    data = json.load(f1)

                    if self.client_id in data.keys():

                        if vk_id in data[self.client_id]:
                            pass

                        else:
                            with open(self.file, 'w', encoding='utf-8') as f2:
                                data[self.client_id].append(vk_id)
                                json.dump(data, f2, indent=4)

                    else:
                        with open(self.file, 'w', encoding='utf-8') as f3:
                            data[self.client_id] = [vk_id]
                            json.dump(data, f3, indent=4)

                except json.decoder.JSONDecodeError:
                    with open(self.file, 'w', encoding='utf-8') as f4:
                        data = {self.client_id: [vk_id]}
                        json.dump(data, f4, indent=4)

        except FileNotFoundError:
            with open(self.file, 'w', encoding='utf-8') as f5:
                data = {self.client_id: [vk_id]}
                json.dump(data, f5, indent=4)
