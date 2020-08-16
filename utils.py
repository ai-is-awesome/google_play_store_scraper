from requests_module import Request

def get_resp_from_query(query):
    resp = Request.get('https://play.google.com/store/search', params = {'q' : query, 'c' : 'apps'})
    return resp