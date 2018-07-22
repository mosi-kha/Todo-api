from ..Helper.JsonFile import JsonFile
import json
import re


class SearchResource(object):
    def on_get(self, req, resp, query):
        """we use regex for search """
        data = JsonFile.read_file()

        new_json = []
        for i in range(len(data['todo'])):
            if re.search(query, data['todo'][i]['text']):
                new_json.append(data['todo'][i])
        resp.body = json.dumps(new_json)
