from django.core.exceptions import ValidationError
from django.http import HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import serializers,status,viewsets
# Create your views here.
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from .models import UserBase,Group,GroupMember,Expense
from .serializers import ExpenseSerializer,GroupSerializer,GroupMemberSerializer,GroupDetailSerializer,SettlementSerializer,ExpenseListSerializer,UserRegisterSerializer, LoginSerializer, TokenResponseSerializer, BalanceResponseSerializer
from .services import expense_split_compute,compute_balance

from drf_spectacular.utils import extend_schema
def home(request):
    return HttpResponse("Welcome to User Base home!")

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserRegisterSerializer,
        responses=UserRegisterSerializer
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data = request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    

class UserLogin(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses=TokenResponseSerializer
    )
    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        # fetch user from validated data
        user = serializer.validated_data['user']
        # If there are no errors, add token to the User 
        token, create = Token.objects.get_or_create(user = user)
        # Return the token string to the client browser
        return Response({
            "token": token.key,
            "user_id": user.id,
            "email": user.email
        }, status=status.HTTP_200_OK)
    

# POST /api/groups/{group_id}/expenses
class ExpenseView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        request=ExpenseSerializer,
        responses=ExpenseListSerializer
    )
    # User wants to create an Expense here, send data which includes amount, participants, group 
    def post(self, request, group_id = None):
        # since this is create we don't need a query-set
        serializer = ExpenseSerializer(data = request.data) 
        serializer.is_valid(raise_exception=True)
            # TODO call create_expense_service(validated_data, group_id)

        '''
            serializer.data is the output representation (after serialization), meant for API responses. 
serializer.validated_data is the clean, validated input (Python-native), meant for creating/updating objects
        '''
        
        result = expense_split_compute(serializer.validated_data, group_id) # here i should pass validated_data of serializer object instead of data 
            # print('Validated Data')
            # serializer.create() # we don't call create here since we have business logic to handle the validation and DB write 
        # else:
        #     return Response(serializer.errors,status=400) 
        print('return of type', type(result), result) 
        # Okay the issue is i am sending result which is a model and trying to return as a JSON before converting it into Python type
        jsonify = ExpenseListSerializer(result)
        print(type(jsonify),jsonify.data)
        return Response(jsonify.data, status=201)

# `GET /api/groups/{group_id}/expenses` Getting Group Expense

    def get(self, request, group_id = None):
        group = get_object_or_404(Group, id=group_id)

        # Check if the one who request group expense is part of the group or not
        if not GroupMember.objects.filter(_group = group,name = request.user).exists():
            raise PermissionDenied('Cannot Provide Information')

        expense_list = Expense.objects.filter(group = group)
        serializer = ExpenseListSerializer(expense_list, many = True) # since we are forwarding many object / rows so we mention many - True
        return Response(serializer.data,status=status.HTTP_200_OK)
    
# GET /api/users/{user_id}/balances
class BalanceView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        responses=BalanceResponseSerializer
    )
    def get(self, request,id):
        # user = request.user
        # what do we need here? request arrives for get and computing balance, need to send data to the service layer
        # no need for serializing here since user just requests for Balance with user id
        # but first i need to check if user exists or not
        
        user = get_object_or_404(UserBase,id = request.user.id)
        get_balance = compute_balance(user)

        return Response(get_balance,status=status.HTTP_200_OK)

# POST /api/settlements settlement happens between the user 
class SettlementView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
    request=SettlementSerializer,
    responses=SettlementSerializer
)
    def post(self, request):

        # so since i am validating both payer and receiver already i can directly use serializer which performs validation of FK
        serializer = SettlementSerializer(data = request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)

# `POST /api/groups/` Creating Group. done by a user 
# class GroupView(viewsets.ViewSet):
class GroupView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        operation_id="create_group",
        request=GroupSerializer,
        responses=GroupSerializer
    )
    def post(self, request):
        # user = request.user
        # serializer = GroupSerializer(data = request.data,context = {'request':user})
        # deserializng incoming data to work with it (JSON → Python Type)
        serializer = GroupSerializer(data = request.data,context = {'request':request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save() #automatically creates the Model object (Python Type → Model Object/Row)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    '''
    serializer = GroupSerializer(data=request.data, context={'request': request.user})   
    user = self.context['request']
    '''
    @extend_schema(
        operation_id="retrieve_group",
        responses=GroupDetailSerializer
    )
    # GET /api/groups/{group_id} RETRIEVE GROUP DETAILS 
    def get(self, request, groupId):
        # user = request.user
        # user_valid = get_object_or_404(UserBase, id = user) ALREADY CHECKED IN permission_classes
        # here we are validating for group id and not user id. 
        # we cannot check directly here since group id is a model and not included in request object
        group = Group.objects.prefetch_related('groupmember_set','expense_set').get(id = groupId)
        # group_members = group.group_members_set.all()
        # group_expense = group.expenses_set.all()

        # check if user is part the group
        if not GroupMember.objects.filter(_group = group,name=request.user).exists():  # need to implement group member's API
            raise PermissionDenied("You are not a member of this group.")

        # return Response(group, status = status.HTTP_200_OK) # it's a fucking model i cannot directly return a model  dict . model -> python dict
        # serializer = GroupDetailSerializer(group,group_members,group_expense)
        serializer = GroupDetailSerializer(group)
        return Response(serializer.data,status = status.HTTP_200_OK )

# `POST /api/groups/{group_id}/members` ADDING NEW GROUP MEMBER!
class GroupMemberView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
    request=GroupMemberSerializer,
    responses=GroupMemberSerializer
)
    def post(self, request, group_id= None):

        group = get_object_or_404(Group, id = group_id)

        if not GroupMember.objects.filter(_group = group, name = request.user).exists():
            # 2. Security Check (IDOR): Is the caller actually an admin or member of this group?
        # (Only members/admins should be allowed to add new members!)
        # if not GroupMember.objects.filter(_group=group, user=request.user).exists():
            raise PermissionDenied("You do not have permission to add members to this group.")
        serializer = GroupMemberSerializer(data = request.data,context = {'group':group})
        # what does the serializer return since before saving to the model i need to verify if user is part the USER Base model
        serializer.is_valid(raise_exception=True)
        # user_id = get_object_or_404(UserBase,serializer.data.name)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # detail=True tells DRF this route looks like /api/groups/{pk}/members/
    # @action(detail=True, methods=['get'], url_path='members')
    # def get_members(self, request, pk=None):
    #         group = get_object_or_404(Group, id=pk)
            
    #         # IDOR Protection
    #         if not group.members.filter(id=request.user.id).exists():
    #             raise PermissionDenied("You cannot view this group's members.")
                
    #         # Grab the related GroupMember rows
    #         members = GroupMember.objects.filter(_group=group)
            
    #         # We reuse your member serializer! (using many=True because it is a queryset list)
    #         serializer = GroupMemberSerializer(members, many=True)
    #         return Response(serializer.data, status=status.HTTP_200_OK)