from .models import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from decimal import Decimal,ROUND_DOWN
from django.db import transaction
from rest_framework.exceptions import ValidationError, PermissionDenied
# from threading import tra
"""
here we build create_service_ layer()
/groups/5/expenses


retrieving group (id  = 5 ) and creating an expense. POST request
so uptill now i have got the expense data, i.e who is paying, 
- who are the participants
- amount 

what i already have is
- group id

A paid 1000
Participants: A, B, C
Split: equal
"""
data = {
  "amount": 1000,
  "`paid_by`": 1,
  "participants": [1,2,3],
  "`split_type`": "equal"
}

def expense_split_compute(data, group_id):

    '''
    check group id 
    check user
    check group members (do we check for user & group member both, checking against group or both ?)
    '''
    total_amount = data.get('amount',0)
    members = [] #[user1, user2, user 3] # Fetch Users

    try:
        # check_group = Group.objects.get_object_or_404(id = group_id) # fetch and check group
        check_group = get_object_or_404(Group,id = group_id) # fetch and check group
    except:
        return JsonResponse('Error :Group does not exist','status : 400')
    
    payer = get_object_or_404(UserBase, id = data.get('paid_by',None)) #fetch user
    participant = data.get('participant', [])
    # for user in participant: 
    #     user = UserBase.objects.get_object_or_404(id = participant[user]) # fetching user object and storing objects in a list
    #     members.append(user)
    # validate i.e ensure payer, participants E group
    members = UserBase.objects.filter(id__in = participant)
    try:
        group_user = GroupMember.objects.get(name = payer, _group=check_group) 
        # if not GroupMember.objects.filter(user=payer, _group=check_group).exists():
    except Exception as e:
        raise PermissionDenied('Error : Payer should be part of the group')
    # for user in participant:
        
        # we reverse look-up here, since each group-member is part of group. we check for group member
        # group_member = GroupMember.objects.select_related()
        # pass
    member = GroupMember.objects.filter(_group = group_id,user_id__in = participant).count()

    if member != len(members):  # check if users belong to the group
        # raise Exception('One or more users do not belong to the group')
        raise PermissionDenied('One or more users do not belong to the group') 
        
    ## split type
    if data.get('split_type') == 'equal':
        equal_amount = split_by_equal(participant, payer , total_amount)

    elif data.get('split_type') == 'percentage':
        percentage_amount = split_by_percent(participant, payer, total_amount)
    try:
    
        with transaction.atomic():
            # create Expense
            # Expense Splits
            splits = []

            exp = Expense.objects.create(
                paid_by = payer, # Pointing out to actual payer user object
                group = check_group, # storing  actual group object
                total_amount = total_amount)
            # for items in equal_amount: # it's a list not dict
            for k,v in equal_amount.items():
                if k != payer:
                    splits.append(
                        ExpenseSplit(
                        expense = exp,
                        # debtor = UserBase.objects.get(id = k),
                        debtor_id = k,
                        creditor = payer
                        shared_amount = v,
                    ))

            ExpenseSplit.objects.bulk_create(splits)
    except Exception as e:
        raise 'Invalid Transaction'

    return {
        'expense' : exp,
        'splits' : splits
    }

def split_by_equal(members,payer,amount):
#     [
#   {"user": 1, "percentage": 50},
#   {"user": 2, "percentage": 30},
#   {"user": 3, "percentage": 20}
# ]
    # amount = data.get('amount',0)
    non_payer = []
    
    for each in range(len(members)):
        # members[each] == base
        # if members[each] != payer # COMPARING WITH OBJECT !!! :
        if members[each] != payer.id:
            non_payer.append(members[each])
        else:
            continue
    group_members = len(members) # 1 is for the payer
    # group_split = group_members / group_split # needs changes
    # base = Decimal('amount') / group_members # needs changes
    # remainder = Decimal(base) % group_members
    # payer_amount = Decimal(remainder) + base
    # base = Decimal(str(amount)) // Decimal(group_members) 
    base = (Decimal(str(amount)) / group_members).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    # 3. Use the modulo operator to find the leftover cents
    remainder = Decimal(str(amount)) % Decimal(group_members)
    
    # 4. The payer gets the base amount plus whatever couldn't be split evenly
    payer_amount = base + remainder
    # check_round = group_split % 2
    # if check_round == 0:
    #     for i in 
    split_user = {}
    # i am not able to think for returning users here.
    # payer = UserBase.objects.get_object_or_404(id = data.get('paid_by',None))
    
    split_user[payer] = payer_amount
    for user in range(len(non_payer)):
        split_user[non_payer[user]] = base
    return split_user
    


{
  "split_type": "percentage",
  "participants": [
    {"user": 1, "percentage": 50},
    {"user": 2, "percentage": 30},
    {"user": 3, "percentage": 20}
  ]
}

def split_by_percent(members, amount):
    '''
    so like here every percent will be given to all the user
    we need to map percent and user here. 
    
    '''