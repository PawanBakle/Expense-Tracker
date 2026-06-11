from .models import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from decimal import Decimal,ROUND_DOWN
from django.db import transaction
from rest_framework.exceptions import ValidationError, PermissionDenied

from django.db.models import Sum, Q
from django.db.models.functions import Coalesce
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied, ValidationError
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

# def expense_split_compute(data, group_id):

#     '''
#     check group id 
#     check user
#     check group members (do we check for user & group member both, checking against group or both ?)
#     '''
#     total_amount = data.get('amount',0)
#     members = [] #[user1, user2, user 3] # Fetch Users

#     try:
#         # check_group = Group.objects.get_object_or_404(id = group_id) # fetch and check group
#         check_group = get_object_or_404(Group,id = group_id) # fetch and check group
#     except:
#         raise PermissionDenied('Error :Group does not exist','status : 400')
    
#     payer = get_object_or_404(UserBase, id = data.get('paid_by',None)) #fetch user
#     participant = data.get('participants', [])
#     # for user in participant: 
#     #     user = UserBase.objects.get_object_or_404(id = participant[user]) # fetching user object and storing objects in a list
#     #     members.append(user)
#     # validate i.e ensure payer, participants E group
#     members = UserBase.objects.filter(id__in = participant)
#     try:
#         group_user = GroupMember.objects.get(name = payer, _group=check_group) 
#         # if not GroupMember.objects.filter(user=payer, _group=check_group).exists():
#     except Exception as e:
#         raise PermissionDenied('Error : Payer should be part of the group')
#     # for user in participant:
        
#         # we reverse look-up here, since each group-member is part of group. we check for group member
#         # group_member = GroupMember.objects.select_related()
#         # pass
#     member = GroupMember.objects.filter(_group = group_id,name__in = participant).count()

#     if len(participant) != len(members):  # check if users belong to the group
#         # raise Exception('One or more users do not belong to the group')
#         raise PermissionDenied('One or more users do not belong to the group') 
        
#     ## split type
#     if data.get('split_type') == 'equal':
#         equal_amount = split_by_equal(participant, payer , total_amount)

#     elif data.get('split_type') == 'percentage':
#         percentage_amount = split_by_percent(participant, payer, total_amount)
#     try:
    
#         with transaction.atomic():
#             # create Expense
#             # Expense Splits
#             splits = []

#             exp = Expense.objects.create(
#                 paid_by = payer, # Pointing out to actual payer user object
#                 group = check_group, # storing  actual group object
#                 total_amount = total_amount)
#             # for items in equal_amount: # it's a list not dict
#             for k,v in equal_amount.items():
#                 if k != payer.id:
#                     splits.append(
#                         ExpenseSplit(
#                         expense = exp,
#                         # debtor = UserBase.objects.get(id = k),
#                         debtor_id = k,
#                         creditor = payer,
#                         shared_amount = v,
#                     ))

#             ExpenseSplit.objects.bulk_create(splits)
#     except Exception as e:
#         raise Exception('Invalid Transaction')

#     return {
#         'expense' : exp,
#         'splits' : splits
#     }

# def split_by_equal(members,payer,amount):
# #     [
# #   {"user": 1, "percentage": 50},
# #   {"user": 2, "percentage": 30},
# #   {"user": 3, "percentage": 20}
# # ]
#     # amount = data.get('amount',0)
#     payer_id = payer.id
#     non_payer = []
    
#     for each in range(len(members)):
#         # members[each] == base
#         # if members[each] != payer # COMPARING WITH OBJECT !!! :
#         if members[each] != payer_id:
#             non_payer.append(members[each])
#         else:
#             continue
#     group_members = len(members) # 1 is for the payer
#     # group_split = group_members / group_split # needs changes
#     # base = Decimal('amount') / group_members # needs changes
#     # remainder = Decimal(base) % group_members
#     # payer_amount = Decimal(remainder) + base
#     # base = Decimal(str(amount)) // Decimal(group_members) 
#     base = (Decimal(str(amount)) / group_members).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
#     # 3. Use the modulo operator to find the leftover cents
#     remainder = Decimal(str(amount)) - (Decimal(base) * Decimal(group_members))
    
#     # 4. The payer gets the base amount plus whatever couldn't be split evenly
#     payer_amount = base + remainder
#     # check_round = group_split % 2
#     # if check_round == 0:
#     #     for i in 
#     split_user = {}
#     # i am not able to think for returning users here.
#     # payer = UserBase.objects.get_object_or_404(id = data.get('paid_by',None))
    
#     split_user[payer_id] = payer_amount
#     # for user in range(len(non_payer)):
#     #     split_user[non_payer[user]] = base
#     for user_id in non_payer:
#         split_user[user_id] = base
#     return [split_user]
    


# {
#   "split_type": "percentage",
#   "participants": [
#     {"user": 1, "percentage": 50},
#     {"user": 2, "percentage": 30},
#     {"user": 3, "percentage": 20}
#   ]
# }

# def split_by_percent(members, amount,payer): # here members is list of dicts' 
#     '''
#     so like here every percent will be given to all the user
#     we need to map percent and user here. 

    
#     '''
#     all_sum = 0
#     split_amount = {}
#     running_total = Decimal('0.00')
#     total_percentage = Decimal('0.00')
#     for member in members:
#         user_id = member['user']
#         percentage = member['percentage']
#         total_percentage  += percentage
#         percent_amount = amount * (Decimal(percentage) / Decimal(100)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
#         split_amount[user_id] = percent_amount
#         running_total += percent_amount

#     if total_percentage  != 100:
#         raise ValueError(f"Percentages sum to {total_percentage}, must be exactly 100")
#     rounding_error = amount - running_total
#     split_amount[payer] += rounding_error
#     return split_amount
#     # split_amount = {}
#     # # group_members = len(members) # 1 is for the payer
#     # # base = (Decimal(str(amount)) / group_members).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
#     # # # 3. Use the modulo operator to find the leftover cents
#     # # remainder = Decimal(str(amount)) % Decimal(group_members)
#     # for each_dict in range(len(members)):
#     #     for k,v in members[each_dict].items():
#     #         percent_amount = (Decimal(str(amount)) * (v / 100)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
#     #         split_amount[k] = percent_amount
#     # return split_amount

def expense_split_compute(data, group_id):
    # 1. Input Validation (Fail Fast)
    total_amount = Decimal(str(data.get('amount', '0')))


    # (Percentage SPLIT) participant_ids = data.get('participants', [])
    if split_type == "equal":
        participant_ids = set(data["participants"])

    else:
        participant_ids = {
            item["user"]
            for item in data["splits"]
        }

    # 2. Database Fetching (Batching)
    check_group = get_object_or_404(Group, id=group_id)
    payer = get_object_or_404(UserBase, id=data.get('paid_by'))
    
    # Check membership for EVERYONE (Payer + Participants) in ONE query
    all_involved_ids = set(participant_ids)
    # all_involved_ids.add(payer.id)
    
    member_count = GroupMember.objects.filter(
        _group=check_group, 
        name__in=all_involved_ids
    ).count()

    if member_count != len(all_involved_ids):
        raise PermissionDenied("One or more users (including payer) are not members of this group.")

    # 3. Calculate Splits (The Pure-Logic Layer)
    split_type = data.get('split_type')
    if split_type == 'equal':
        calculated_splits = split_by_equal(participant_ids, payer, total_amount)
    elif split_type == 'percentage':
        # Assumes data['participants'] is the list of {user: id, percentage: X} dicts
        # (Percentage SPLIT) calculated_splits = split_by_percent(participant_ids, total_amount, payer)
        split_data = data["splits"]
        calculated_splits = split_by_percent(split_data,total_amount,payer )


    else:
        raise ValidationError(f"Unsupported split type: {split_type}")

    # 4. Persistence (The Atomic Layer)
    try:
        with transaction.atomic():
            # Create the main expense
            exp = Expense.objects.create(
                paid_by=payer,
                group=check_group,
                total_amount=total_amount
            )

            # Build the list of Split objects (using our new standardized contract)
            split_objects = []
            for item in calculated_splits:
                # We don't create a 'debt' for the payer to themselves
                if item['user_id'] != payer.id:
                    split_objects.append(
                        ExpenseSplit(
                            expense=exp,
                            debtor_id=item['user_id'],
                            creditor=payer,
                            shared_amount=item['amount']
                        )
                    )

            # Single Database Hit for all splits
            ExpenseSplit.objects.bulk_create(split_objects)
            
            return exp # Success

    except Exception as e:
        # Log the actual error 'e' here in a real app
        raise Exception("Failed to record expense transaction.") from e


def split_by_equal(member_ids, payer, amount):
    amount = Decimal(str(amount))
    n = len(member_ids)
    
    base = (amount / n).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
    remainder = amount - (base * n)

    # Use a dict for internal calculation (fast lookups)
    results_map = {m_id: base for m_id in member_ids}
    results_map[payer.id] += remainder

    # Convert to the agreed "Contract" format
    return [{"user_id": u_id, "amount": amt} for u_id, amt in results_map.items()]

def split_by_percent(members, amount, payer):
    amount = Decimal(str(amount))
    results_map = {}
    running_total = Decimal('0.00')
    total_percentage = Decimal('0.00')

    for m in members:
        u_id = m['user']
        perc = Decimal(str(m['percentage']))
        
        share = (amount * (perc / 100)).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        
        results_map[u_id] = share
        running_total += share
        total_percentage += perc

    if total_percentage != 100:
        raise ValueError("Total percentage must be 100")

    # Reconcile rounding error to payer
    results_map[payer.id] += (amount - running_total)

    return [{"user_id": u_id, "amount": amt} for u_id, amt in results_map.items()]

# We perform ONE aggregate call on the ExpenseSplit table
# Balance View
def compute_balance(user_id):
    results = ExpenseSplit.objects.aggregate(
    total_credits=Coalesce(
        Sum('shared_amount', filter=Q(creditor=user_id)), 
        Decimal('0.00')
    ),
    total_debts=Coalesce(
        Sum('shared_amount', filter=Q(debtor=user_id)), 
        Decimal('0.00')
    )
)
    # Now results is a simple dict: {'total_credits': 500.00, 'total_debts': 200.00}
    theo_balance = results['total_credits'] - results['total_debts']
    return theo_balance
