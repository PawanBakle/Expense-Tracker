from django.test import TestCase

from user_base.serializers import ExpenseSerializer
class ExpenseSerializerTests(TestCase):

    def test_valid_equal_split(self):

        data = {
            "amount": "900.00",
            "paid_by": 1,
            "participants": [1, 2, 3],
            "split_type": "equal"
        }

        serializer = ExpenseSerializer(data=data)

        self.assertTrue(serializer.is_valid())
    def test_duplicate_participants_fail(self):

        data = {
            "amount": "900.00",
            "paid_by": 1,
            "participants": [1, 1, 2],
            "split_type": "equal"
        }

        serializer = ExpenseSerializer(data=data)

        self.assertFalse(serializer.is_valid())
    def test_valid_percentage_split(self):

        data = {
            "amount": "1000.00",
            "paid_by": 1,
            "split_type": "percentage",
            "splits": [
                {"user": 1, "percentage": 50},
                {"user": 2, "percentage": 30},
                {"user": 3, "percentage": 20},
            ]
        }

        serializer = ExpenseSerializer(data=data)

        self.assertTrue(serializer.is_valid())

    def test_percentage_not_100_fails(self):

        data = {
            "amount": "1000.00",
            "paid_by": 1,
            "split_type": "percentage",
            "splits": [
                {"user": 1, "percentage": 40},
                {"user": 2, "percentage": 40},
                {"user": 3, "percentage": 10},
            ]
        }

        serializer = ExpenseSerializer(data=data)

        self.assertFalse(serializer.is_valid())