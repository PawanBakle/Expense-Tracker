from django.core.exceptions import ValidationError

from .views import *
from .models import Expense
from rest_framework import serializers

class ExpenseSerializer(serializers.ModelSerializer):
    allowed_values = ['equal','percentage']
    amount = serializers.DecimalField(max_digits=10,decimal_places=2)
    split_type = serializers.CharField()
    paid_by = serializers.IntegerField()
    participants = serializers.ListField(serializers.IntegerField)
    class Meta:
        model = Expense
        fields = ['paid_by','group','total_amount','description','created_at']
    def validate_amount(self, amount):
        if amount < 0:  
            raise serializers.ValidationError('Negative Amount')
        return amount
    def validate_participants(self, participants):
        if len(participants) == 0:
            raise serializers.ValidationError('There must be at least one participant')
    def split_type(self, split_type):
        if self.split_type not in self.allowed_values:
            raise serializers.ValidationError("Invalid Split Type")

    def validate(self, attrs):
        return super().validate(attrs)