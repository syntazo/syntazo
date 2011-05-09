from django import http

def checkPlayerLoggedInHttp(player):
    if not player:
        return http.HttpResponseForbidden('You must be an signed in.')

def checkPlayerLoggedInJson(player):
    if not player:
        return {'error': 'No player logged in',}
