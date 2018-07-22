import falcon
from todo_v1.Resource.Completed import CompletedResource
from todo_v1.Resource.Identify import IdentifyResource
from todo_v1.Resource.Search import SearchResource

api = application = falcon.API()

api.add_route('/todos/{completed}', CompletedResource())  # allows methods : GET
api.add_route('/todo/{identify}', IdentifyResource())  # allows methods : GET POST PUT DELETE
api.add_route('/search/{query}', SearchResource())  # allows methods : GET
