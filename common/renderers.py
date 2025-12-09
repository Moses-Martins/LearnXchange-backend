from rest_framework.renderers import JSONRenderer

class APIResponseRenderer(JSONRenderer):
   
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = {}
        message = "Request successful"
        payload = None

        if renderer_context:
            response = renderer_context.get('response')
            status_code = getattr(response, 'status_code', 200)

            if status_code >= 400:
                # Errors handled by exception handler
                response_data = data
            else:
                # Extract message from view data if it exists
                if isinstance(data, dict):
                    message = data.pop('message', message)
                    payload = data.get('data', data)
                else:
                    payload = data

                success = payload is not None
                response_data = {
                    'success': success,
                    'data': payload,
                    'error': None,
                    'message': message
                }
        else:
            response_data = {
                'success': True,
                'data': data,
                'error': None,
                'message': message
            }

        return super().render(response_data, accepted_media_type, renderer_context)
