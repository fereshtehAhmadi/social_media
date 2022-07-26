from rest_framework import renderers
import json


class UserRender(renderers.JSONRenderer):
    charset = 'utf_8'
    def render(self, data, accept_media_type=None, render_context=None):
        response = ''
        if 'ErrorDetail' == str(data):
            response = json.dumps({'errors': data})
        else:
            response = json.dumps(data)
            
        return response
