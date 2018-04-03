import json
import string


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return sorted(list(obj))
        return json.JSONEncoder.default(self, obj)


def process(text):
    translator = str.maketrans('', '', string.punctuation + '\xa0')
    return text.translate(translator)
