from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from .models import Expense,Group,GroupMember,Settlement,UserBase
from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import transaction
from .managers import UserBaseManager

# UserBase = get_user_model()
# Registration of the User
class UserRegisterSerializer(serializers.ModelSerializer):
    # validate password 
    
    password = serializers.CharField(write_only = True,validators=[validate_password])
    class Meta:
        model = UserBase
        fields = ['id','email','password','mobile_number']
        
    
    def create(self, validated_data):
        password = validated_data['password']
        user = UserBase.objects.create_user(**validated_data)
        # user = UserBase.objects.create(**validated_data)
        # user.set_password(password)
        # user.save()
        # return user
        return user
class TokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    user_id = serializers.IntegerField()
    email = serializers.EmailField()

# POST /api/users/login
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']
        if email and password:
            user = authenticate(email = email, password = password)

            if user is None:
                raise serializers.ValidationError("Invalid email or password")
            if not user.is_active:
                raise serializers.ValidationError("This user is disabled")
        else:
            raise serializers.ValidationError("Must include both email and password")

        attrs['user'] = user
        return attrs

# creating Expense  (POST API)
'''data = {
  "amount": 1000,
  "`paid_by`": 1,
  "participants": [1,2,3],
  "`split_type`": "equal"
}
'''

class PercentageSplitSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    percentage = serializers.DecimalField(
        max_digits=5,
        decimal_places=2
    )

class ExpenseSerializer(serializers.Serializer):
    allowed_values = ['equal','percentage']
    amount = serializers.DecimalField(max_digits=10,decimal_places=2)
    split_type = serializers.CharField()
    paid_by = serializers.IntegerField()
    # participants = serializers.ListField(child = serializers.IntegerField())

    participants = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
    splits = PercentageSplitSerializer(
        many=True,
        required=False
    )
    # class Meta:
    #     model = Expense
        # fields = ['paid_by','group','total_amount','description','created_at']
    def validate_amount(self, amount):
        if amount < 0:  
            raise serializers.ValidationError('Negative Amount')
        return amount
    def validate_participants(self, participants):
        if len(participants) == 0:
            raise serializers.ValidationError('There must be at least one participant')
        if len(list(set(participants))) != len(participants):
            raise serializers.ValidationError('Participants are repeated')
        return participants
    def validate_split_type(self, split_type):
        allowed_values = self.allowed_values
        if split_type not in allowed_values:
            raise serializers.ValidationError("Invalid Split Type")
        return split_type
    
    # def validate(self, attrs):
    #     participants = attrs.get("participants", [])
    #     paid_by = attrs.get("paid_by")

    #     if paid_by not in participants:
    #         raise serializers.ValidationError("payer must be part of participants")

    #     return attrs

    def validate(self, attrs):

        split_type = attrs.get("split_type")
        paid_by = attrs.get("paid_by")

        if split_type == "equal":

            participants = attrs.get("participants")

            if not participants:
                raise serializers.ValidationError(
                    "participants required for equal split"
                )

            if len(set(participants)) != len(participants):
                raise serializers.ValidationError(
                    "Participants are repeated"
                )

            if paid_by not in participants:
                raise serializers.ValidationError(
                    "payer must be part of participants"
                )

        elif split_type == "percentage":

            splits = attrs.get("splits")

            if not splits:
                raise serializers.ValidationError(
                    "splits required for percentage split"
                )

            users = [item["user"] for item in splits]

            if len(set(users)) != len(users):
                raise serializers.ValidationError(
                    "duplicate users in splits"
                )

            if paid_by not in users:
                raise serializers.ValidationError(
                    "payer must be part of splits"
                )

            total_percentage = sum(
                item["percentage"]
                for item in splits
            )

            if total_percentage != 100:
                raise serializers.ValidationError(
                    "Total percentage must equal 100"
                )

        return attrs
    


#`GET /api/groups/{group_id}/expenses` Getting Group Expense
class ExpenseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id','group','paid_by','total_amount','description','created_at']


# POST /api/settlements
class SettlementSerializer(serializers.ModelSerializer):
    # can i refer to model serializer here? or do i need custom validations? 
    '''
    group = models.ForeignKey(Group,on_delete=models.PROTECT)
    payer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name= 'settlements_paid')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='settlements_received')
    amount_paid = models.DecimalField(max_digits=10,decimal_places=2)
    '''

    #This automatically validates that the incoming 'user' ID exists in UserBase (since dealing with 1 object we don't need many= True here)
    group = serializers.PrimaryKeyRelatedField(queryset = Group.objects.all())
    payer = serializers.PrimaryKeyRelatedField(queryset = UserBase.objects.all())
    receiver = serializers.PrimaryKeyRelatedField(queryset = UserBase.objects.all())
    class Meta:
        model = Settlement
        fields = ['id','group','payer','receiver','amount_paid']
    
    def validate(self, attrs):
        payer = attrs['payer']
        receiver = attrs['receiver']
        group = attrs['group']

        if payer == receiver:
            raise serializers.ValidationError('Receiver and Payer cannot be same ')
        
        if not ( GroupMember.objects.filter(_group = group,name = payer).exists() and GroupMember.objects.filter(_group = group, name = receiver).exists()):
            raise serializers.ValidationError('Both the payer and the receiver must be members of the group')
        return attrs

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'created_by', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']

    def create(self, validated_data):
        # context = {request: request}
        user = self.context['request'].user
        
        # Use an atomic transaction so both rows succeed together or fail together
        with transaction.atomic():
            # 1. Create the Group
            group = Group.objects.create(created_by=user, **validated_data)
            
            # 2. Automatically make the creator the first Admin Member!
            GroupMember.objects.create(
                _group=group,
                name=user,
                is_admin=True
            )
            
        return group

    
class GroupMemberSerializer(serializers.ModelSerializer):
    # REMOVED many=True because Postman sends a single ID per request
    name = serializers.PrimaryKeyRelatedField(queryset=UserBase.objects.all())

    class Meta:
        model = GroupMember
        # fields = ['id', 'name', '_group', 'is_admin', 'joined_at']
        fields = '__all__'
        # Make '_group' read_only so Postman doesn't have to provide it in the raw JSON body
        # read_only_fields = ['id', '_group', 'joined_at']

    def validate(self, attrs):
        # DRF automatically resolves 'name' to a clean, single UserBase instance here!
        user_instance = attrs['name']
        group_obj = self.context['group'] # Grabbing the group instance from view context

        # Safe, clean ORM duplicate member check
        if GroupMember.objects.filter(_group=group_obj, name=user_instance).exists():
            raise serializers.ValidationError("This user is already a member of this group.")

        return attrs

    def create(self, validated_data):
        # Snatch the context group instance
        group_obj = self.context['group']
        
        # Explicitly combine them to create the clean row safely
        return GroupMember.objects.create(_group=group_obj, **validated_data)
   
class GroupDetailSerializer(serializers.ModelSerializer):
    # here we serialize both members and groups which we have passed inside the GroupDetailSerializer
    members = GroupMemberSerializer(source = 'groupmember_set',many = True, read_only = True)
    expense = ExpenseListSerializer(source = 'expense_set',many = True, read_only = True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'created_by', 'created_at','members','expense']
        read_only_fields = ['id', 'created_at']


class BalanceResponseSerializer(serializers.Serializer):
    you_are_owed = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    you_owe = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    balance = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )

 # SETTLEMENT SERIALIZER (WRONG SERIALIZER)

# `POST /api/groups/{group_id}/members` ADDING GROUP MEMBER
# class GroupMemberSerializer(serializers.ModelSerializer):
#     name = serializers.PrimaryKeyRelatedField(many = True, queryset = UserBase.objects.all())
#     # am i doing any validation here? 
#     class Meta:
#         model = GroupMember
#         fields = ['id','name','_group','is_admin','joined_at']
#         read_only_fields = ['id','joined_at']
#     def create(self,validated_data): # cannot pass user-id in here 
#         user_id = validated_data['name'] # retrieve name row for FK to User
#         # for joined at i do need the user id 
#         g_id = self.context['group_id'] # retrieve group row for FK to Group


#         # TO prevent duplicates we check if user exists in the Group already as a Member!
#         # for that we need to retreive all member FROM the group i.e holding Group retrieve Members (1-m)
#         # if Group.objects.filter(id = g_id, members__name = user_id).exists():
#         if GroupMember.objects.filter(_group = g_id,name = user_id).exists():
#             raise serializers.ValidationError("This user is already a member of this group.")
#         return GroupMember.objects.create(group= g_id, **validated_data)

# class GroupSerializer(serializers.Serializer):
#     '''
#     name = models.CharField(max_length=25,null=False, blank=True)
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
#     created_at = models.DateTimeField(auto_now_add=True)
#     '''
#     name = serializers.CharField(max_length = 25)

#     def create(self, validated_data):
#         user = self.context['request']
#         return Group.objects.create(created_by = user, **validated_data)


# class GroupMembersSerializer(serializers.ModelSerializer):
#     # to convert all member objects into PYTHON
#     class Meta:
#         model = GroupMember
        


# SETTLEMENT SERIALIZER (WRONG SERIALIZER)
class GroupDetailSerializer(serializers.ModelSerializer):
    # here we serialize both members and groups which we have passed inside the GroupDetailSerializer
    members = GroupMemberSerializer(source = 'groupmember_set',many = True, read_only = True)
    expense = ExpenseListSerializer(source = 'expense_set',many = True, read_only = True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'created_by', 'created_at','members','expense']
        read_only_fields = ['id', 'created_at']



    # def create(self, validated_data):
    #     payer = validated_data['payer']
    #     receiver = validated_data['receiver']
    #     group = validated_data['group']
    #     if not ( GroupMember.objects.filter(group = group,name = payer).exists() and GroupMember.objects.filter(group = group, name = receiver).exists()):
    #         raise serializers.ValidationError('Either Receiver or Payer are not part of the Group')
        
    #     return Settlement.objects.create(**validated_data)
    



