from django.db import models

from django.contrib.auth.models import User,AbstractBaseUser,BaseUserManager,AbstractUser
from django.conf import settings
'''
Group
GroupMember
Expense
ExpenseSplit
Settlement
'''

# For user we use Django's built in User model, but for simplicity we will create our own User model here.

class UserBase(AbstractUser):
    # name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # password = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length= 15)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.email

class Group(models.Model):
    name = models.CharField(max_length=25,null=False, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

class GroupMember(models.Model):
    name = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    _group = models.ForeignKey(Group,on_delete=models.PROTECT)
    is_admin = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)
 
class Expense(models.Model):
    paid_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    # since a group has MANY settlements over time
    group = models.ForeignKey(Group,on_delete=models.PROTECT) 
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    description  = models.TextField(max_length=100, null = True, blank= True)
    created_at = models.DateTimeField(auto_now_add=True)

class ExpenseSplit(models.Model):
    expense = models.ForeignKey(Expense,on_delete=models.PROTECT)
    debtor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='splits_as_debtor')
    creditor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='splits_as_creditor')
    shared_amount = models.DecimalField(max_digits=10,decimal_places=2)   
    created_at = models.DateTimeField(auto_now_add=True)
    """
    B → A : 300
    C → A : 300
    """

class Settlement(models.Model):
    group = models.ForeignKey(Group,on_delete=models.PROTECT)
    payer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name= 'settlements_paid')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='settlements_received')
    amount_paid = models.DecimalField(max_digits=10,decimal_places=2)

