import json

directory = 'todo_v1/todo.json'


class JsonFile:
    bass = dic = {
        "todo": [
        ]
    }

    @classmethod
    def write_file(cls, dic):  # input is dictionary object and path is a string
        with open(directory, 'w') as f:
            json.dump(dic, f, indent=2, sort_keys=True)
        f.close()

    @classmethod
    def read_file(cls):
        try:
            with open('todo_v1/todo.json', 'r') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            cls.write_file(cls.bass)

    @classmethod
    def find_in_json(cls, key, value):
        """in this method , if key and value will be match,return the dic """
        data = JsonFile.read_file()
        new_json = []
        for i in range(len(data['todo'])):
            if data['todo'][i][key] == value:
                if key is 'id':
                    return data['todo'][i]  # because id is unique and when find  it we don't need keep processing
                else:
                    new_json.append(data['todo'][i])
        return new_json
