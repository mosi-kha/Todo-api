from ..Helper.JsonFile import JsonFile
import json
from falcon import errors


class CompletedResource(object):

    def on_get(self, req, resp, completed):
        """check completed is a valid word """
        _true_list = ['true', 'True']
        _false_test = ['false', 'False']
        if completed in _true_list:
            completed = True
        elif completed in _false_test:
            completed = False
        else:
            raise errors.HTTPBadRequest('Invalid URI', {'Valid URI': [_true_list, _false_test]})

        resp.body = json.dumps(JsonFile.find_in_json('completed', completed))
