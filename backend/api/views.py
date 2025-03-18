from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse
from rest_framework.response import Response
from .core.azure_chat_completion import send_chat_completion_stream
import json


@csrf_exempt
@api_view(['POST'])
def chat_completion(request):
    try:
        history = json.loads(request.POST["history"])

        def generate():
            try:
                for chunk in send_chat_completion_stream(history):
                    yield chunk
            except Exception as e:
                yield f"""An error occured:
                {e}"""

        return StreamingHttpResponse(generate(), content_type="text/plain")

    except Exception as e:
        return Response({"answer": "Something bad happened", "error": str(e)}, status=500)
