from celery.result import AsyncResult
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class TaskStatusView(APIView):
    """
    Return status of a Celery task.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        result = AsyncResult(task_id)

        response_data = {
            'task_id': task_id,
            'status': result.status,
        }

        if result.ready():
            if result.successful():
                response_data['result'] = result.result
            else:
                response_data['error'] = str(result.result)

        return Response(response_data, status=status.HTTP_200_OK)
