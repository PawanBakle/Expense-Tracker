from django.core.exceptions import ValidationError
from django.http import HttpResponse
from rest_framework import serializers
# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .serializers import ExpenseSerializer
from .services import expense_split_compute


def home(request):
    return HttpResponse("Welcome to User Base home!")

class ExpenseView(APIView):
    def post(self, request, group_id = None):
        # since this is create we don't need a query-set
        serializer = ExpenseSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
            # TODO call create_expense_service(validated_data, group_id)

        result = expense_split_compute(serializer.data, group_id)
            # print('Validated Data')
            # serializer.create() # we don't call create here since we have business logic to handle the validation and DB write 
        # else:
        #     return Response(serializer.errors,status=400)  
        return Response(result, status=201)