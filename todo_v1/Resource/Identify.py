import falcon
import uuid
import json
from ..Helper.JsonFile import JsonFile
from falcon import errors


class IdentifyResource(object):
    """ I assure you make unique IDs and never save same IDs in your file and life :))"""

    def make_valid_json(self, dic):
        """check dic and make new valid json and return it"""
        if 'text' not in dic or type(dic['text']) is not str:  # text must be exist in req
            raise falcon.errors.HTTPBadRequest(
                'Invalid JSON',
                json.loads(
                    '{"id":"option (default use uuid.uuid4 and must be integer)",'
                    '"completed":"option (default false)","text":"is Necessary and type must be string"}')
            )
        else:
            new_json = {'text': dic['text']}
            if 'completed' in dic:
                if dic['completed'] in ['true', 'True'] or dic['completed'] is True:
                    new_json['completed'] = True
            else:
                new_json['completed'] = False

            if 'id' in dic:  # check if id exist or not , then if exist , check created before or not
                dic['id'] = self.make_id_int(dic['id'])
                exist = JsonFile.find_in_json('id', dic['id'])
                if len(exist) == 0:
                    new_json['id'] = dic['id']
                else:
                    raise falcon.errors.HTTPConflict(
                        'id : {0} was created before'.format(dic['id'])
                    )
            else:
                new_json['id'] = int(uuid.uuid4())
            return new_json

    def make_id_int(self, idd):
        try:
            return int(idd)
        except ValueError:
            raise errors.HTTPBadRequest('id must be integer type')

    def on_get(self, req, resp, identify):
        """ '*' is a spacial character  to show all json dada in file"""
        if identify is '*':
            resp.body = json.dumps(JsonFile.read_file())
            return

        identify = self.make_id_int(identify)
        exist_id = JsonFile.find_in_json('id', identify)
        if len(exist_id) == 0:
            resp.status = falcon.HTTP_NO_CONTENT
        else:
            resp.status = falcon.HTTP_OK
            resp.body = json.dumps(exist_id)

    def on_post(self, req, resp, identify):
        """in this method , id in url is not our identification for create"""
        client_req = req.media

        data = JsonFile.read_file()

        if type(client_req) is not list:  # make list for append
            client_req = [client_req]
        for item in range(len(client_req)):
            data['todo'].append(self.make_valid_json(client_req[item]))

        JsonFile.write_file(data)
        resp.status = falcon.HTTP_CREATED

    def on_put(self, req, resp, identify):
        """this method update one dictionary and can not change ID """
        identify = self.make_id_int(identify)
        client_req = req.media
        if type(client_req) is not dict:
            raise falcon.errors.HTTPBadRequest('your request body must be a dictionary')

        exist_id = False

        my_data = JsonFile.read_file()
        for i in range(len(my_data['todo'])):
            if identify == my_data['todo'][i]['id']:
                exist_id = my_data['todo'][i]
                dic = my_data['todo'][i]
                if 'completed' in client_req:
                    if client_req['completed'] in ['true', 'True'] or client_req['completed'] is True:
                        dic['completed'] = True
                    else:
                        dic['completed'] = False

                if 'text' in client_req:
                    if type(client_req['text']) is not str:
                        raise errors.HTTPBadRequest('Invalid text', 'text\' type must be string ')
                    else:
                        dic['text'] = client_req['text']

        JsonFile.write_file(my_data)

        if exist_id is False:
            resp.status = falcon.HTTP_NO_CONTENT
        else:
            resp.status = falcon.HTTP_OK
            resp.body = json.dumps(exist_id)

    def on_delete(self, req, resp, identify):
        identify = self.make_id_int(identify)
        exist_id = False
        data = JsonFile.read_file()
        for item in range(len(data['todo'])):
            if identify == data['todo'][item]['id']:
                data['todo'].pop(item)
                exist_id = True
                break  # if use return , we get of def

        JsonFile.write_file(data)

        if exist_id is False:  # it's mean id is't available
            resp.status = falcon.HTTP_NO_CONTENT  # todo
            resp.body = json.dumps({"message": "{0} does not exist".format(identify)})
            return

        resp.status = falcon.HTTP_OK
        resp.body = json.dumps({'message': '{0} is deleted successful!'.format(identify)})
